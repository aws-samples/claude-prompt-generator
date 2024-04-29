import json
import os
import re
import threading

import gradio as gr
from dotenv import load_dotenv

from ape import APE
from metaprompt import MetaPrompt
from optimize import Alignment
from translate import GuideBased

# ape = APE()
rewrite = GuideBased()
alignment = Alignment()
metaprompt = MetaPrompt()

load_dotenv()


def generate_prompt(original_prompt, level):
    if level == "One-time Generation":
        result = rewrite(original_prompt)  # , cost
        return [
            gr.Textbox(
                label="Prompt Generated",
                value=result,
                lines=3,
                show_copy_button=True,
                interactive=False,
            )
        ] + [gr.Textbox(visible=False)] * 2

    elif level == "Multiple-time Generation":
        candidates = []
        for i in range(3):
            result = rewrite(original_prompt)
            candidates.append(result)
        judge_result = rewrite.judge(candidates)
        textboxes = []
        for i in range(3):
            is_best = "Y" if judge_result == i else "N"
            textboxes.append(
                gr.Textbox(
                    label=f"Prompt Generated #{i+1} {is_best}",
                    value=candidates[i],
                    lines=3,
                    show_copy_button=True,
                    visible=True,
                    interactive=False,
                )
            )
        return textboxes


def ape_prompt(original_prompt, user_data):
    result = ape(initial_prompt, 1, json.loads(user_data))
    return [
        gr.Textbox(
            label="Prompt Generated",
            value=result["prompt"],
            lines=3,
            show_copy_button=True,
            interactive=False,
        )
    ] + [gr.Textbox(visible=False)] * 2


with gr.Blocks(
    title="Automatic Prompt Engineering",
    theme="soft",
    css="#textbox_id textarea {color: red}",
) as demo:
    gr.Markdown("# Automatic Prompt Engineering")

    with gr.Tab("Meta Prompt"):
        original_task = gr.Textbox(
            label="Task",
            lines=3,
            info="Please input your task",
            placeholder="Draft an email responding to a customer complaint",
        )
        variables = gr.Textbox(
            label="Variables",
            info="Please input your variables, one variable per line",
            lines=5,
            placeholder="CUSTOMER_COMPLAINT\nCOMPANY_NAME",
        )
        metaprompt_button = gr.Button("Generate Prompt")
        prompt_result = gr.Textbox(
            label="Prompt Template Generated",
            lines=3,
            show_copy_button=True,
            interactive=False,
        )
        variables_result = gr.Textbox(
            label="Variables Generated",
            lines=3,
            show_copy_button=True,
            interactive=False,
        )
        metaprompt_button.click(
            metaprompt,
            inputs=[original_task, variables],
            outputs=[prompt_result, variables_result],
        )

    with gr.Tab("Generate Prompt"):
        original_prompt = gr.Textbox(
            label="Please input your original prompt",
            lines=3,
            placeholder='Summarize the text delimited by triple quotes.\n\n"""{{insert text here}}"""',
        )
        gr.Markdown("Use {\{xxx\}} to express custom variable, e.g. {\{document\}}")
        with gr.Row():
            with gr.Column(scale=2):
                level = gr.Radio(
                    ["One-time Generation", "Multiple-time Generation"],
                    label="Optimize Level",
                    value="One-time Generation",
                )
                b1 = gr.Button("Revise Prompt")
            # with gr.Column(scale=2):
            #     user_data = gr.Textbox(label="Test data JSON[Deprecated]", lines=2, interactive=False)
            #     b2 = gr.Button("APE optimze prompt[Deprecated]")
        textboxes = []
        for i in range(3):
            t = gr.Textbox(
                label="Prompt Generated",
                elem_id="textbox_id",
                lines=3,
                show_copy_button=True,
                interactive=False,
                visible=False if i > 0 else True,
            )
            textboxes.append(t)
        log = gr.Markdown("")
        b1.click(generate_prompt, inputs=[original_prompt, level], outputs=textboxes)

    with gr.Tab("Prompt Evaluation"):
        with gr.Row():
            user_prompt_original = gr.Textbox(
                label="Please input your original prompt", lines=3
            )
            kv_input_original = gr.Textbox(
                label="[Optional]Input the template variable need to be replaced",
                placeholder="Ref format: key1:value1;key2:value2",
                lines=3,
            )
            user_prompt_original_replaced = gr.Textbox(
                label="Replace Result", lines=3, interactive=False
            )

            user_prompt_eval = gr.Textbox(
                label="Please input the prompt need to be evaluate", lines=3
            )
            kv_input_eval = gr.Textbox(
                label="[Optional]Input the template variable need to be replaced",
                placeholder="Ref format: key1:value1;key2:value2",
                lines=3,
            )
            user_prompt_eval_replaced = gr.Textbox(
                label="Replace Result", lines=3, interactive=False
            )
        with gr.Row():
            insert_button_original = gr.Button("Replace Variables in Original Prompt")
            insert_button_original.click(
                alignment.insert_kv,
                inputs=[user_prompt_original, kv_input_original],
                outputs=user_prompt_original_replaced,
            )
            insert_button_revise = gr.Button("Replace Variables in Revised Prompt")
            insert_button_revise.click(
                alignment.insert_kv,
                inputs=[user_prompt_eval, kv_input_eval],
                outputs=user_prompt_eval_replaced,
            )
        with gr.Row():
            # https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
            openai_model_dropdown = gr.Dropdown(
                label="Choose OpenAI Model",
                choices=[
                    "gpt-3.5-turbo",
                    "gpt-3.5-turbo-1106",
                    "gpt-4-32k",
                    "gpt-4-1106-preview",
                    "gpt-4-turbo-preview",
                ],
                value="gpt-3.5-turbo",
            )
            # aws bedrock list-foundation-models --region us-east-1 --output json | jq -r '.modelSummaries[].modelId'
            aws_model_dropdown = gr.Dropdown(
                label="Choose AWS Model",
                choices=[
                    "anthropic.claude-instant-v1:2:100k",
                    "anthropic.claude-instant-v1",
                    "anthropic.claude-v2:0:18k",
                    "anthropic.claude-v2:0:100k",
                    "anthropic.claude-v2:1:18k",
                    "anthropic.claude-v2:1:200k",
                    "anthropic.claude-v2:1",
                    "anthropic.claude-v2",
                    "anthropic.claude-3-sonnet-20240229-v1:0",
                    "anthropic.claude-3-haiku-20240307-v1:0",
                ],
                value="anthropic.claude-3-haiku-20240307-v1:0",
            )

        invoke_button = gr.Button("Execute prompt")
        with gr.Row():
            openai_output = gr.Textbox(
                label="OpenAI Output", lines=3, interactive=False, show_copy_button=True
            )
            aws_output = gr.Textbox(
                label="AWS Bedrock Output",
                lines=3,
                interactive=False,
                show_copy_button=True,
            )
        invoke_button.click(
            alignment.invoke_prompt,
            inputs=[
                user_prompt_original_replaced,
                user_prompt_eval_replaced,
                user_prompt_original,
                user_prompt_eval,
                openai_model_dropdown,
                aws_model_dropdown,
            ],
            outputs=[openai_output, aws_output],
        )
        # invoke_button.click(
        #     invoke_prompt_stream,
        #     inputs=[
        #         user_prompt_original,
        #         user_prompt_eval,
        #         openai_model_dropdown,
        #         aws_model_dropdown,
        #         openai_output,
        #         aws_output,
        #     ],
        #     outputs=[]
        # )

        with gr.Row():
            feedback_input = gr.Textbox(
                label="Evaluate the Prompt Effect",
                placeholder="Input your feedback manually or by model",
                lines=3,
                show_copy_button=True,
            )
            with gr.Column():
                eval_model_dropdown = gr.Dropdown(
                    label="Choose the Evaluation Model",
                    # Use Bedrock to evaluate the prompt, sonnet or opus are recommended
                    choices=[
                        "anthropic.claude-3-sonnet-20240229-v1:0",
                        # opus placeholder
                    ],
                    value="anthropic.claude-3-sonnet-20240229-v1:0",
                )
                evaluate_button = gr.Button("Auto-evaluate the Prompt Effect")
                evaluate_button.click(
                    alignment.evaluate_response,
                    inputs=[
                        openai_output,
                        aws_output,
                        eval_model_dropdown,
                    ],
                    outputs=[feedback_input],
                )
        revise_button = gr.Button("Iterate the Prompt")
        revised_prompt_output = gr.Textbox(
            label="Revised Prompt", lines=3, interactive=False, show_copy_button=True
        )
        revise_button.click(
            alignment.generate_revised_prompt,
            inputs=[
                feedback_input,
                user_prompt_eval,
                openai_output,
                aws_output,
                eval_model_dropdown,
            ],
            outputs=revised_prompt_output,
        )

demo.launch()
