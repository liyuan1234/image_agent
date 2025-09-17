from openai import OpenAI
from utils import load_config
config = load_config()
MODEL_NAME = config["MODEL_NAME"]
MAX_OUTPUT_TOKENS = config['MAX_OUTPUT_TOKENS']
REASONING_EFFORT = 'medium'
PROMPT_FILE = config["PROMPT_FILE"]


client = OpenAI()

def send_chatgpt_request(image_b64):
    with open(f'../prompt/{PROMPT_FILE}','r') as f:
        prompt = f.read()

    response = client.responses.create(model=MODEL_NAME, input = [
        {"role":"user",
        "content":[
            {
            "type":"input_text",
            "text": prompt,
            },
        
            {
            "type":"input_image",
            "image_url":f"data:image/png;base64,{image_b64}"
            } 
            ]
        }
        ],
        max_output_tokens=MAX_OUTPUT_TOKENS,
        reasoning={"effort": REASONING_EFFORT})
    return response