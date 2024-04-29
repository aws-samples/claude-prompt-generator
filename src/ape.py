import os
import json

import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

# Get the directory where the current script is located
current_script_path = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the file
prompt_guide_path = os.path.join(current_script_path, "PromptGuide.md")

# Open the file using the full path
with open(prompt_guide_path, 'r') as f:
    PromptGuide = f.read()

region_name = os.getenv("REGION_NAME")

session = boto3.Session()
retry_config = Config(
    region_name=region_name,
    retries={
        "max_attempts": 5,
        "mode": "standard",
    },
)
service_name = "bedrock-runtime"
bedrock_client = session.client(service_name=service_name, config=retry_config)

from rater import Rater


class APE:
    def __init__(self):
        self.rater = Rater()

    def __call__(self, initial_prompt, epoch, demo_data):
        candidates = []
        for _ in range(2):
            candidates.append(self.rewrite(initial_prompt))
        candidates_raw = candidates.copy()
        customizable_variable_list = list(demo_data.keys())
        candidates = [
            {"prompt": candidate}
            for candidate in candidates
            if all(
                [
                    customizable_variable in candidate
                    for customizable_variable in customizable_variable_list
                ]
            )
        ]
        best_candidate = self.rater(initial_prompt, candidates, demo_data)
        for _ in range(epoch):
            more_candidate = self.generate_more(
                initial_prompt, candidates[best_candidate]["prompt"]
            )
            candidates = [candidates[best_candidate]] + [{"prompt": more_candidate}]
            best_candidate = self.rater(initial_prompt, candidates, demo_data)
        return candidates[best_candidate]

    def rewrite(self, initial_prompt):
        prompt = """
You are a instruction engineer. Your task is to rewrite the initial instruction in <instruction> xml tag based on the suggestions in the instruction guide in <guide> xml tag.

Instruction guide:
<guide>
{guide}
</guide>

You are a instruction engineer. Your task is to rewrite the initial instruction in <instruction> xml tag based on the suggestions in the instruction guide in <guide> xml tag.
which is included using double pointed brackets is customizable text that will be replaced at runtime. This needs to be kept as is.
Please same language as the initial instruction for rewriting.

<instruction>
{initial}
</instruction>


Please only output the rewrite result.
""".strip()
        messages = [
            {
                "role": "user",
                "content": prompt.format(guide=PromptGuide, initial=initial_prompt),
            }  # ,{
            #   "role": "assistant",
            #   "content": "{"
            # }
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
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"  # anthropic.claude-3-sonnet-20240229-v1:0 "anthropic.claude-3-haiku-20240307-v1:0"
        accept = "application/json"
        contentType = "application/json"

        response = bedrock_client.invoke_model(
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

    def generate_more(self, initial_prompt, example):
        prompt = """
You are a instruction engineer. Your task is to rewrite the initial instruction in <instruction> xml tag based on the suggestions in the instruction guide in <guide> xml tag.

Instruction guide:
<guide>
{guide}
</guide>

You are a instruction engineer. Your task is to rewrite the initial instruction in <instruction> xml tag based on the suggestions in the instruction guide in <guide> xml tag.
which is included using double pointed brackets is customizable text that will be replaced at runtime. This needs to be kept as is.
Please same language as the initial instruction for rewriting.

<instruction>
{initial}
</instruction>

<example>
{demo}
</example>

Please only output the rewrite result.
""".strip()
        messages = [
            {
                "role": "user",
                "content": prompt.format(
                    guide=PromptGuide, initial=initial_prompt, demo=example
                ),
            }  # ,{
            #   "role": "assistant",
            #   "content": "{"
            # }
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
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"  # anthropic.claude-3-sonnet-20240229-v1:0 "anthropic.claude-3-haiku-20240307-v1:0"
        accept = "application/json"
        contentType = "application/json"

        response = bedrock_client.invoke_model(
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
