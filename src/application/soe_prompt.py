import os
import base64
import json
import boto3

from dotenv import load_dotenv

load_dotenv()

class ProductDescriptionGenerator:
    def __init__(self, model_id="anthropic.claude-3-sonnet-20240229-v1:0", system='You are an AI assistant that generates SEO-optimized product descriptions.'):
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.getenv("REGION_NAME"))
        self.model_id = model_id
        self.system = system

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def run_multi_modal_prompt(self, messages, max_tokens=4000):
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": messages
        })

        response = self.bedrock_runtime.invoke_model(
            body=body, modelId=self.model_id)
        response_body = json.loads(response.get('body').read())

        return response_body

    def generate_bedrock_response(self, prompt):
        messages = [{
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        }]
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": messages,
            "system": self.system,
        })
        response = self.bedrock_runtime.invoke_model(body=body, modelId=self.model_id)
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']

    def generate_product_description(self, product_category, brand_name, usage_description, target_customer, image_path=None):
        prompt_template = f"""
        Generate an SEO-optimized product description for a {product_category} from {brand_name}. 
        Usage: {usage_description}
        Target customer: {target_customer}
        """

        if image_path:
            encoded_image = self.encode_image(image_path)
            message = {
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": encoded_image}},
                    {"type": "text", "text": prompt_template}
                ]
            }
            messages = [message]
            response = self.run_multi_modal_prompt(messages, max_tokens=4000)
            image_description = response['content'][0]['text']
            prompt_template += f"\nImage description: {image_description}"

        product_description = self.generate_bedrock_response(prompt_template)
        return product_description

if __name__ == "__main__":
    generator = ProductDescriptionGenerator()

    product_category = input("Please provide the product category: ")
    brand_name = input("Please provide the brand name: ")
    usage_description = input("Please provide the usage description: ")
    target_customer = input("Please provide the target customer: ")
    image_path = input("Please provide the path to the product image (optional): ")

    product_description = generator.generate_product_description(
        product_category, brand_name, usage_description, target_customer, image_path
    )

    print("Generated Product Description:")
    print(product_description)
