import boto3
from botocore.config import Config
import json
import re
import os
import pandas as pd
import io
import time
import pathlib
import gradio as gr
from sklearn.metrics import confusion_matrix

with open('prompt/error_analysis_classification.prompt') as f:
    error_analysis_prompt = f.read()
with open('prompt/step_prompt_classification.prompt') as f:
    step_prompt = f.read()
with open('prompt/prompt_guide_short.prompt') as f:
    prompt_guide_short = f.read()

class CalibrationPrompt:
    def __init__(self):
        with open('metaprompt.txt') as f:
            self.metaprompt = f.read()

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
        self.bedrock_client = session.client(service_name=service_name, config=retry_config)
    def invoke_model(self, prompt, model='haiku'):
        if 'haiku' in model:
            model = "anthropic.claude-3-haiku-20240307-v1:0"
        else:
            model = "anthropic.claude-3-sonnet-20240229-v1:0"
        messages=[
            {
                "role": "user",
                "content":  prompt
            }
        ]
        body = json.dumps(
            {
                "messages": messages,
                "max_tokens": 4096,
                "anthropic_version": "bedrock-2023-05-31",
            }
        )
        modelId = "anthropic.claude-3-haiku-20240307-v1:0"  # anthropic.claude-3-sonnet-20240229-v1:0 "anthropic.claude-3-haiku-20240307-v1:0"
        accept = "application/json"
        contentType = "application/json"

        response = self.bedrock_client.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())
        message = response_body["content"][0]["text"]
        return message
    def get_output(self, prompt, dataset, postprocess_code, return_df=False):
        if isinstance(dataset, bytes):
            data_io = io.BytesIO(dataset)
            dataset = pd.read_csv(data_io)
        exec(postprocess_code, globals())
        results = []
        for row_idx, row in dataset.iterrows():
            label = row['label']
            variables = {}
            for key, value in dict(row).items():
                if key == 'label':
                    continue
                variables[key] = value
            predict = self.invoke_model(prompt.format(**variables))
            result = postprocess(predict)
            results.append(result)
        
        dataset['predict'] = results
        if return_df:
            return dataset
        timestr = time.strftime("%Y%m%d-%H%M%S")
        dataset.to_csv(f'temp/predict_{timestr}.csv', index=None)
        return gr.DownloadButton(label=f'Download predict result (predict_{timestr}.csv)',value=pathlib.Path(f'temp/predict_{timestr}.csv'),visible=True)

    def optimize(self, task_description, prompt, dataset, postprocess_code, step_num=3):
        if isinstance(dataset, bytes):
            data_io = io.BytesIO(dataset)
            dataset = pd.read_csv(data_io)
        cur_dataset = self.get_output(prompt, dataset, postprocess_code, return_df=True)
        history = []
        for _ in range(step_num):
            step_result = self.step(task_description, prompt, dataset, postprocess_code, history)
            prompt = step_result['cur_prompt']
            dataset = step_result['dataset']
            history = step_result['history']
        return prompt.strip()

    def step(self, task_description, prompt, dataset, postprocess_code, history):
        num_errors = 5
        mean_score = self.eval_score(dataset)
        errors = self.extract_errors(dataset)
        large_error_to_str = self.large_error_to_str(errors, num_errors)
        history = self.add_history(dataset, task_description, history, mean_score, errors)
        sorted_history = sorted(history, key=lambda x: x['score'],reverse=False)
        last_history = sorted_history[-3:]
        history_prompt = '\n'.join([self.sample_to_text(sample,
                                                        num_errors_per_label=num_errors,
                                                        is_score=True) for sample in last_history])
        prompt_input = {"original_instruction": history[-1]['prompt'].strip(),
        "task_description": task_description,
        'error_analysis': history[-1]['analysis'],
        'failure_cases': large_error_to_str
        }
        prompt_input["labels"] = json.dumps([str(label) for label in list(dataset['label'].unique())])
        prompt_suggestion = self.invoke_model(step_prompt.format(**prompt_input), model='sonnet')
        pattern = r"<new_prompt>(.*?)</new_prompt>"
        cur_prompt = re.findall(pattern, prompt_suggestion, re.DOTALL)[0]
        cur_dataset = self.get_output(cur_prompt, dataset, postprocess_code, return_df=True)
        score = self.eval_score(cur_dataset)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        cur_dataset.to_csv(f'temp/predict_{timestr}.csv', index=None)
        return {
            'cur_prompt': cur_prompt,
            'score': score,
            'explanation': prompt_suggestion,
            'dataset': cur_dataset,
            'history': history
        }
        
        
    def get_eval_function(self):
        def set_function_from_iterrow(func):
            def wrapper(dataset):
                dataset['score'] = dataset.apply(func, axis=1)
                return dataset
            return wrapper
        return set_function_from_iterrow(lambda record: record['label'] == record['predict'])
    def sample_to_text(self, sample: dict, num_errors_per_label: int = 0, is_score: bool = True) -> str:
        """
        Return a string that organize the information of from the step run for the meta-prompt
        :param sample: The eval information for specific step
        :param num_errors_per_label: The max number of large errors per class that will appear in the meta-prompt
        :param is_score: If True, add the score information to the meta-prompt
        :return: A string that contains the information of the step run
        """
        if is_score:
            return f"<example>\n<prompt_score>\n{sample['score']:.2f}\n</prompt_score>\n<prompt>\n{sample['prompt']}\n</prompt>\n<example>\n"
        else:
            return f"####\n##Prompt:\n{sample['prompt']}\n{self.large_error_to_str(sample['errors'], num_errors_per_label)}####\n "
    def large_error_to_str(self, error_df: pd.DataFrame, num_large_errors_per_label: int) -> str:
        """
        Return a string that contains the large errors
        :param error_df: A dataframe contains all the mislabeled samples
        :param num_large_errors_per_label: The (maximum) number of large errors per label
        :return: A string that contains the large errors that is used in the meta-prompt
        """
        required_columns = error_df.columns.tolist()
        label_schema = error_df['label'].unique()
        gt_name = 'GT'
        error_res_df_list = []
        txt_res = ''
        for label in label_schema:
            cur_df = error_df[error_df['label'] == label]
            cur_df = cur_df.sample(frac=1.0, random_state=42)[:num_large_errors_per_label]
            error_res_df_list.append(cur_df[required_columns])
        if len(error_res_df_list) > 0:
            error_res_df = pd.concat(error_res_df_list, ignore_index=True)
            error_res_df = error_res_df.sample(frac=1.0, random_state=42)
            for i, row in error_res_df.iterrows():
                label = row.label
                prediction = row.predict
                Sample = ''
                for k,v in dict(row).items():
                    if k in ('label', 'predict', 'score'):
                        continue
                    Sample += f'{k}: {v}\n'
                Sample = Sample.strip()
                txt_res += f"<Sample>\n{Sample}\n</Sample>\n<Prediction>\n{prediction}\n</Prediction>\n<GT>\n{label}\n</GT>\n"
        return txt_res.strip()

    def eval_score(self, dataset) -> float:
        score_func = self.get_eval_function()
        dataset = score_func(dataset)
        mean_score = dataset['score'].mean()
        return mean_score
    def extract_errors(self, dataset) -> pd.DataFrame:
        """
        Extract the errors from the dataset
        :return: records that contains the errors
        """
        df = dataset
        err_df = df[df['score'] < 0.5]
        err_df.sort_values(by=['score'])
        return err_df
    def add_history(self, dataset, task_description, history, mean_score, errors):
        num_errors = 5
        large_error_to_str = self.large_error_to_str(errors, num_errors)
        prompt_input = {
            'task_description': task_description,
            'accuracy': mean_score,
            'prompt': prompt,
            'failure_cases': large_error_to_str
            }
        label_schema = dataset['label'].unique()
        conf_matrix = confusion_matrix(dataset['label'], dataset['predict'], labels=label_schema)
        conf_text = f"Confusion matrix columns:{label_schema} the matrix data:"
        for i, row in enumerate(conf_matrix):
            conf_text += f"\n{label_schema[i]}: {row}"
        prompt_input['confusion_matrix'] = conf_text
        analysis = self.invoke_model(error_analysis_prompt.format(**prompt_input), model='haiku')
        pattern = r"<analysis>(.*?)</analysis>"
        analysis = re.findall(pattern, analysis, re.DOTALL)[0].strip()
        history.append({'prompt': prompt, 'score': mean_score,'errors': errors, 'confusion_matrix': conf_matrix, 'analysis': analysis})
        return history