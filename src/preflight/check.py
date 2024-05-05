import os
import re
import json
import boto3
from botocore.exceptions import ClientError, NoRegionError, EndpointConnectionError
from urllib3.exceptions import NameResolutionError

# load env file from upper directory
from dotenv import load_dotenv
load_dotenv()

def check_claude3_availability(region):
    try:
        bedrock_client = boto3.client("bedrock", region_name=region)
        response = bedrock_client.list_foundation_models(byProvider="anthropic")
        
        claude3_pattern = re.compile(r"anthropic\.claude-3.*")
        available_models = [model["modelId"] for model in response["modelSummaries"]]
        claude3_models = [model for model in available_models if claude3_pattern.match(model)]
        
        if claude3_models:
            print(f"Claude3 models are available in configured ({region}) region.")
            # print(f"Available Claude3 models: {', '.join(claude3_models)}")
            return True
        else:
            print(f"No Claude3 models found in the {region} region.")
            return False

    except NoRegionError:
        print(f"The specified region '{region}' is invalid or not configured.")
        return False
    except EndpointConnectionError as e:
        print(f"Could not connect to the endpoint URL: {e}")
        return False
    except NameResolutionError:
        print(f"Failed to resolve the service endpoint for the {region} region.")
        return False
    except ClientError as e:
        if e.response["Error"]["Code"] == "AccessDeniedException":
            print("Access denied. Check if your credentials have the necessary permissions.")
        else:
            print(f"An error occurred: {e}")
        return False

def has_privileges_to_invoke_bedrock(region):
    try:
        bedrock = boto3.client("bedrock", region_name=region)
        bedrock.list_foundation_models()
        print("User has privileges to list foundation models.")

        messages = [{
            "role": "user",
            "content": [{"type": "text", "text": "Hello, world!"}]
        }]
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": messages,
            "system": "You are an AI assistant that generates SEO-optimized product descriptions."
        })
        # Check sonnet model availability
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        bedrock_runtime.invoke_model(body=body, modelId=model_id)
        print("User has privileges to invoke Claude3 models.")

        return True
    except NoRegionError:
        print(f"The specified region '{region}' is invalid or not configured.")
        return False
    except EndpointConnectionError as e:
        print(f"Could not connect to the endpoint URL: {e}")
        return False
    except NameResolutionError:
        print(f"Failed to resolve the service endpoint for the {region} region.")
        return False
    except ClientError as e:
        if e.response["Error"]["Code"] == "AccessDeniedException":
            print("Access denied. Check if your credentials have the necessary permissions.")
        else:
            print(f"An error occurred: {e}")
        return False

def main():
    region = os.getenv("REGION_NAME", 'us-east-1')
    if has_privileges_to_invoke_bedrock(region):
        if check_claude3_availability(region):
            # ANSI escape sequence for green color
            print("\033[92mPre-flight validation passed. You can proceed with invoking AWS Bedrock (Claude3).\033[0m")
        else:
            # ANSI escape sequence for red color
            print("\033[91mPre-flight validation failed. Claude3 models are not available in the specified region.\033[0m")
    else:
        # ANSI escape sequence for red color
        print("\033[91mPre-flight validation failed. User does not have privileges to invoke AWS Bedrock (Claude3).\033[0m")

if __name__ == "__main__":
    main()
