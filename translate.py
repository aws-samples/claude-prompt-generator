import json
import os

import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

with open("PromptGuide.md") as f:
    PromptGuide = f.read()
region_name = os.getenv("REGION_NAME")


class GuideBased:
    def __init__(self):
        session = boto3.Session()
        retry_config = Config(
            region_name=region_name,
            retries={
                "max_attempts": 5,
                "mode": "standard",
            },
        )
        service_name = "bedrock-runtime"
        self.bedrock_client = session.client(
            service_name=service_name, config=retry_config
        )

    def __call__(self, initial_prompt):
        lang = self.detect_lang(initial_prompt)
        if "ch" in lang:
            lang_prompt = "Please use Chinese for rewriting. The xml tag name is still in English."
        elif "en" in lang:
            lang_prompt = "Please use English for rewriting."
        else:
            lang_prompt = "Please use same language as the initial instruction for rewriting. The xml tag name is still in English."

        prompt = """
You are a instruction engineer. Your task is to rewrite the initial instruction in <initial_instruction></initial_instruction> xml tag based on the suggestions in the instruction guide in <instruction_guide></instruction_guide> xml tag.

<instruction_guide>
{guide}
</instruction_guide>

You are a instruction engineer. Your task is to rewrite the initial instruction in <initial_instruction></initial_instruction> xml tag based on the suggestions in the instruction guide in <instruction_guide></instruction_guide> xml tag.
This instruction is then sent to claude to get the expected output.

Something like `{{variable}}` is customizable text that will be replaced when sent to claude. It needs to be retained in the rewrite.

You are a instruction engineer. Your task is to rewrite the initial instruction in <initial_instruction></initial_instruction> xml tag based on the suggestions in the instruction guide in <instruction_guide></instruction_guide> xml tag.
This instruction is then sent to claude to get the expected output.

{lang_prompt}

Only output the rewrite instruction return them in <rerwited></rerwited>XML tags
If examples are already included in the initial prompt, do not remove the examples after the rewrite.

Example:
<initial_instruction>
You are a research assistant. You will answer the following question based on the document in triple quotes, if the question cannot be answered please output "Cannot answer the question from the document"
```
{{full_text}}
```
You will also need to find the original quote from the document that is most relevant to answering the question. If there is no relevant citation, output "No relevant quotes".
Your output should start by listing all the quotes, putting one quote per line and starting with a numerical index. Then answer the question by adding the index of the quote where it is needed.

The question is: 
{{question}}
</initial_instruction>

<rerwited>
You are an expert research assistant. Here is a document you will answer questions about:
<doc>
{{full_text}}
</doc>

First, find the quotes from the document that are most relevant to answering the question, and then print them in numbered order. Quotes should be relatively short.

If there are no relevant quotes, write "No relevant quotes" instead.

Then, answer the question, starting with "Answer:". Do not include or reference quoted content verbatim in the answer. Don't say "According to Quote [1]" when answering. Instead make references to quotes relevant to each section of the answer solely by adding their bracketed numbers at the end of relevant sentences.

Thus, the format of your overall response should look like what's shown between the <example></example> tags. Make sure to follow the formatting and spacing exactly.
<example>
Quotes:
[1] "Company X reported revenue of $12 million in 2021."
[2] "Almost 90% of revenue came from widget sales, with gadget sales making up the remaining 10%."

Answer:
Company X earned $12 million. [1] Almost 90% of it was from widget sales. [2]
</example>

If the question cannot be answered by the document, say "Cannot answer the question from the document".

<question>
{{question}}
</question>
</rerwited>

<initial_instruction>
{initial}
</initial_instruction>
""".strip()

        messages = [
            {
                "role": "user",
                "content": prompt.format(
                    guide=PromptGuide, initial=initial_prompt, lang_prompt=lang_prompt
                ),
            },
            {"role": "assistant", "content": "<rerwited>"},
        ]
        body = json.dumps(
            {
                "messages": messages,
                "max_tokens": 4096,
                "temperature": 0.8,
                "top_k": 50,
                "top_p": 1,
                "stop_sequences": ["</rerwited>"],
                "anthropic_version": "bedrock-2023-05-31",
            }
        )
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"  # anthropic.claude-3-sonnet-20240229-v1:0 "anthropic.claude-3-haiku-20240307-v1:0"
        accept = "application/json"
        contentType = "application/json"

        response = self.bedrock_client.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())
        result = response_body["content"][0]["text"].replace("</rewrite>", "").strip()
        if result.startswith("<instruction>"):
            result = result[13:]
        if result.endswith("</instruction>"):
            result = result[:-14]
        result = result.strip()
        return result

    def detect_lang(self, initial_prompt):
        lang_example = json.dumps({"lang": "ch"})
        prompt = """
Please determine what language the document below is in? English (en) or Chinese (ch)?

<document>
{document}
</document>
    
Use JSON format with key `lang` when return result. Please only output the result in json format, and do the json format check and return, don't include other extra text! An example of output is as follows:
Output example: {lang_example}
""".strip()
        messages = [
            {
                "role": "user",
                "content": prompt.format(
                    document=initial_prompt, lang_example=lang_example
                ),
            },
            {"role": "assistant", "content": "{"},
        ]
        body = json.dumps(
            {
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.8,
                "top_k": 50,
                "top_p": 1,
                "stop_sequences": ["\n\nHuman:"],
                "anthropic_version": "bedrock-2023-05-31",
            }
        )
        modelId = modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
        accept = "application/json"
        contentType = "application/json"

        response = self.bedrock_client.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())
        try:
            lang = json.loads("{" + response_body["content"][0]["text"])["lang"]
        except:
            lang = ""
        return lang

    def judge(self, candidates):
        Instruction_prompts = []
        for idx, candidate in enumerate(candidates):
            Instruction_prompts.append(
                f"Instruction {idx+1}:\n<instruction>\n{candidate}\n</instruction>"
            )
        example = json.dumps({"Preferred": "Instruction 1"})
        prompt = """
You are a instruction engineer. Your task is to evaluate which of the three instructions given below is better based on guide in <guide> xml tag.

Instruction guide:
<guide>
{guide}
</guide>

You are a instruction engineer. Your task is to evaluate which of the three instructions given below is better based on guide in <guide> xml tag.

{Instruction_prompts}

Use JSON format when returning results. Please only output the result in json format, and do the json format check and return, don't include other extra text! An example of output is as follows:
{example}
""".strip()
        messages = [
            {
                "role": "user",
                "content": prompt.format(
                    guide=PromptGuide,
                    Instruction_prompts="\n\n".join(Instruction_prompts),
                    example=example,
                ),
            },
            {"role": "assistant", "content": "{"},
        ]
        body = json.dumps(
            {
                "messages": messages,
                "max_tokens": 128,
                "temperature": 0.1,
                "top_k": 50,
                "top_p": 1,
                "stop_sequences": ["\n\nHuman:"],
                "anthropic_version": "bedrock-2023-05-31",
            }
        )
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"  # anthropic.claude-3-sonnet-20240229-v1:0
        accept = "application/json"
        contentType = "application/json"

        response = self.bedrock_client.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())
        final_result = None
        try:
            result = json.loads("{" + response_body["content"][0]["text"])
            for idx in range(3):
                if str(idx + 1) in result["Preferred"]:
                    final_result = idx
                    break
        except:
            pass
        return final_result
