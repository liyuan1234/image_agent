from __future__ import annotations

import argparse
import sys
import time

from .config import AppPaths, load_config
from .utils import choose_from_list, list_prompt_files, load_prompt_text, write_response_to_file



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monitor a window or full screen and send changed screenshots to OpenAI.")
    parser.add_argument("--project-root", help="Project root containing config.json, prompt/, and output folders.")
    parser.add_argument("--config", help="Path to config.json.")
    parser.add_argument("--window", help="Window title to monitor. Omit for interactive selection.")
    parser.add_argument("--fullscreen", action="store_true", help="Monitor the primary screen instead of a named window.")
    parser.add_argument("--prompt-file", help="Prompt file name from prompt/ or bundled prompts.")
    parser.add_argument("--once", action="store_true", help="Process a single changed frame and exit.")
    parser.add_argument("--list-windows", action="store_true", help="List detectable window titles and exit.")
    parser.add_argument("--list-prompts", action="store_true", help="List prompt files and exit.")
    return parser



def _list_window_titles() -> list[str]:
    from .screenshot import list_window_titles

    return list_window_titles()



def choose_window_interactively() -> str | None:
    windows = _list_window_titles()
    selected = choose_from_list(windows, "choose window to monitor...")
    return None if selected == "Fullscreen" else selected



def resolve_prompt(args, paths: AppPaths, config: dict) -> tuple[str, str]:
    prompt_name = args.prompt_file or config.get("PROMPT_FILE", "prompt.txt")
    if args.prompt_file is None and not sys.stdin.isatty():
        return prompt_name, load_prompt_text(prompt_name, paths)

    if args.prompt_file:
        return prompt_name, load_prompt_text(prompt_name, paths)

    prompt_options = list_prompt_files(paths)
    if not prompt_options:
        raise FileNotFoundError("No prompt files found.")

    selected = choose_from_list(prompt_options, "choose prompt file...") if sys.stdin.isatty() else prompt_name
    return selected, load_prompt_text(selected, paths)



def resolve_window(args, config: dict) -> str | None:
    if args.fullscreen:
        return None
    if args.window:
        return args.window

    config_appname = (config.get("APPNAME") or "").strip()
    if config_appname:
        return config_appname

    return choose_window_interactively() if sys.stdin.isatty() else None



def run(args: argparse.Namespace) -> int:
    paths = AppPaths.discover(project_root=args.project_root, config_file=args.config)
    paths.ensure_directories()
    config = load_config(paths)

    if args.list_windows:
        for index, title in enumerate(_list_window_titles()):
            print(f"[{index}] {title}")
        return 0

    if args.list_prompts:
        for name in list_prompt_files(paths):
            print(name)
        return 0

    prompt_name, prompt_text = resolve_prompt(args, paths, config)
    appname = resolve_window(args, config)
    print(f"using prompt file: {prompt_name}...")
    print(f"monitoring {appname or 'Fullscreen'}...")

    from .llm import send_chatgpt_request
    from .screenshot import detect_screen_change, encode_image_to_base64

    while True:
        image = detect_screen_change(paths, appname)
        image_b64 = encode_image_to_base64(image)
        start = time.time()
        response = send_chatgpt_request(image_b64, paths, prompt_text)
        write_response_to_file(response, paths)
        print(response.output_text)
        print(f"time taken: {time.time() - start:.3f}s")
        if args.once:
            return 0



def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(args)
