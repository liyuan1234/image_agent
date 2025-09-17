import json
import io
from datetime import datetime
import json
import os
import pywinctl as pwc

def startup():
    # Ensure required folders exist
    required_dirs = ['../images', '../responses', '../chat_completions', '../prompt']
    for d in required_dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    windows_mode = 1
    if windows_mode:
        windows = print_all_windows_title()
        n = int(input('choose window to monitor...'))
        appname = windows[n]
        if n == 0:
            appname = None
    else:
        appname = None #fullscreen mode
    print(f'monitoring {appname}...')
    return appname

def print_all_windows_title():
    # windows = gw.getAllTitles()
    windows = pwc.getAllTitles()
    windows = ['Fullscreen'] + windows

    for window in enumerate(windows):
        window = list(window)
        print(f'[{window[0]}] {window[1]}')

    return windows



def load_config(config_file="../config.json"):
    with open(config_file, "r") as f:
        config = json.load(f)
    return config

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")

def get_save_filename():
    current_datetime = get_current_datetime()
    filename = f'../images/screenshot_{current_datetime}.png'
    return filename

def save_image(image,filename = None):
    if not filename:
        filename = get_save_filename()
    image.save(filename)
    print(f'screenshot saved to {filename}...')
    return filename

def write_response_to_file(response):
    now = datetime.now()
    current_datetime = now.strftime("%Y%m%d_%H%M%S")
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    if os.path.exists('../responses/responses.log'):
        with open('../responses/responses.log', 'r') as f:
            old_text = f.read()
    else:
        old_text = ""

    with open('../responses/responses.log', 'w') as f:
        f.write(f"\n\n\n{'='*100}\n\n\n")
        f.write(f'log start: [{current_datetime}]\n')
        f.write(f'date: {date_str}\n')
        f.write(f'time: {time_str}\n')
        f.write(response.output_text + old_text)
        f.write(f"\n\n\n{'='*100}\n\n\n")

    with open(f'../chat_completions/chat_completion_{current_datetime}.log','w') as f:
        f.write(f"{'='*100}\n")
        f.write(f'log start.\n')
        f.write(f"{'='*100}\n")
        f.write(json.dumps(response.model_dump(),
                        indent = 2,
                        ensure_ascii=False))
        f.write(f"{'='*100}\n")
