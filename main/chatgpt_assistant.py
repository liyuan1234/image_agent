#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 09:56:10 2025

@author: liyuan
"""

import time
import os
from utils import startup, load_config, get_current_datetime, write_response_to_file
from screenshot import  detect_screen_change, encode_image_to_base64
from llm import send_chatgpt_request

appname = startup()

while True:
    image = detect_screen_change(appname)
    b64 = encode_image_to_base64(image)
    start = time.time()
    response = send_chatgpt_request(b64)
    write_response_to_file(response)
    print(response.output_text)
    print(f'time taken: {time.time()-start:.3f}s')