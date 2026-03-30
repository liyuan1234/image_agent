from __future__ import annotations

import os

from openai import OpenAI

from .config import AppPaths, load_config
from .utils import load_prompt_text

REASONING_EFFORT = "medium"


def send_chatgpt_request(image_b64: str, paths: AppPaths, prompt: str | None = None):
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    config = load_config(paths)
    model_name = config["MODEL"]
    max_output_tokens = config["MAX_OUTPUT_TOKENS"]
    if prompt is None:
        prompt = load_prompt_text(config.get("PROMPT_FILE", "prompt.txt"), paths)

    client = OpenAI()
    return client.responses.create(
        model=model_name,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{image_b64}"},
                ],
            }
        ],
        max_output_tokens=max_output_tokens,
        reasoning={"effort": REASONING_EFFORT},
    )
