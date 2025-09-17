#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 09:56:10 2025

@author: liyuan
"""

import time
import os
from utils import load_config, get_current_datetime, get_save_filename, save_image, write_response_to_file
from screenshot import print_all_windows_title, detect_screen_change, encode_image_to_base64
from llm import send_chatgpt_request


# Ensure required folders exist
required_dirs = ['../images', '../responses', '../chat_completions', '../prompt']
for d in required_dirs:
    if not os.path.exists(d):
        os.makedirs(d)

windows = print_all_windows_title()
APPNAME = "ac"
if APPNAME:
    if (APPNAME in windows) and (APPNAME != ""):
        appname = APPNAME
    else:
        n = int(input('choose window to monitor...'))
        appname = windows[n]
elif APPNAME is None:
    appname = None

while True:
    print(appname)
    image = detect_screen_change(appname)
    filepath = get_save_filename()
    save_image(image, filepath)
    b64 = encode_image_to_base64(image)
    start = time.time()
    response = send_chatgpt_request(b64)
    write_response_to_file(response)
    print(response.output_text)
    print(f'time taken: {time.time()-start:.3f}s')