#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 09:56:10 2025

@author: liyuan
"""

import time
import os
from utils import load_config, get_current_datetime, get_save_filename, save_image, write_response_to_file
from screenshot import screenshot, compare_images, detect_screen_change, encode_image_to_base64
from llm import send_chatgpt_request

# Ensure required folders exist
required_dirs = ['../images', '../responses', '../chat_completions', '../prompt']
for d in required_dirs:
    if not os.path.exists(d):
        os.makedirs(d)

while True:
    image = detect_screen_change()
    filepath = get_save_filename()
    save_image(image, filepath)
    b64 = encode_image_to_base64(image)
    start = time.time()
    response = send_chatgpt_request(b64)
    write_response_to_file(response)
    print(response.output_text)
    print(f'time taken: {time.time()-start:.3f}s')