import json

import boto3
from botocore.config import Config

region_name = "us-west-2"
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


class Rater:
    def __init__(self):
        pass

    def __call__(self, initial_prompt, candidates, demo_data):
        for candidate in candidates:
            if "output" in candidate:
                continue
            candidate_prompt = candidate["prompt"]
            for k, v in demo_data.items():
                candidate_prompt = candidate_prompt.replace(k, v)
            candidate["input"] = candidate_prompt
            candidate["output"] = self.get_output(candidate_prompt)
        for k, v in demo_data.items():
            initial_prompt = initial_prompt.replace(k, v)
        rate = self.rater(initial_prompt, candidates)
        return rate

    def get_output(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        body = json.dumps(
            {
                "messages": messages,
                "max_tokens": 4096,
                "temperature": 0.8,
                "top_k": 50,
                "top_p": 1,
                "stop_sequences": ["\n\nHuman:"],
                "anthropic_version": "bedrock-2023-05-31",
            }
        )
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"  # anthropic.claude-3-sonnet-20240229-v1:0 "anthropic.claude-3-haiku-20240307-v1:0"
        accept = "application/json"
        contentType = "application/json"

        response = bedrock_client.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())
        result = response_body["content"][0]["text"]
        return result

    def rater(self, initial_prompt, candidates):
        rater_example = json.dumps({"Preferred": "Response 1"})
        Response_prompt = []
        for candidate_idx, candidate in enumerate(candidates):
            Response_template = f"""
Response {candidate_idx+1}:
{candidate}
</response_{candidate_idx+1}>
""".strip()
            Response_prompt.append(Response_template)
        Response_prompt = "\n\n".join(Response_prompt)
        rater_prompt = """
You are an expert rater of helpful and honest Assistant responses. Given the instruction and the two responses choose the most helpful and honest response.
Please pay particular attention to the response formatting requirements called for in the instruction.

Instruction:
<instruction>
{instruction}
</instruction>

{Response_prompt}

Finally, select which response is the most helpful and honest.

Use JSON format with key `Preferred` when returning results. Please only output the result in json format, and do the json format check and return, don't include other extra text! An example of output is as follows:
Output example: {rater_example}
""".strip()
        messages = [
            {
                "role": "user",
                "content": rater_prompt.format(
                    instruction=initial_prompt,
                    Response_prompt=Response_prompt,
                    rater_example=rater_example,
                ),
            },
            {"role": "assistant", "content": "{"},
        ]
        body = json.dumps(
            {
                "messages": messages,
                "max_tokens": 4096,
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
        result_json = "{" + response_body["content"][0]["text"]
        try:
            result = None
            result_json = json.loads(result_json)
            for idx in range(len(candidates)):
                if str(idx + 1) in result_json["Preferred"]:
                    result = idx
                    break
        except:
            result = random.ranint(0, len(candidates) - 1)
        if result is None:
            result = random.ranint(0, len(candidates) - 1)
        return result
