from __future__ import annotations

import json
from datetime import datetime
from importlib import resources
from pathlib import Path
from typing import Iterable

from .config import AppPaths


DEFAULT_SEPARATOR = "\n\n\n" + ("=" * 100) + "\n\n\n"


def get_current_datetime() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_save_filename(paths: AppPaths, suffix: str = ".png") -> Path:
    return paths.images_dir / f"screenshot_{get_current_datetime()}{suffix}"


def save_image(image, paths: AppPaths, filename: Path | None = None) -> Path:
    target = filename or get_save_filename(paths)
    image.save(target)
    print(f"screenshot saved to {target}...")
    return target


def format_response_text(text: str) -> str:
    return text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\t", "\t")


def write_response_to_file(response, paths: AppPaths) -> tuple[Path, Path]:
    formatted_output = format_response_text(response.output_text)
    now = datetime.now()
    current_datetime = now.strftime("%Y%m%d_%H%M%S")
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    responses_log = paths.responses_dir / "responses.log"
    old_text = responses_log.read_text(encoding="utf-8") if responses_log.exists() else ""

    responses_log.write_text(
        (
            f"{DEFAULT_SEPARATOR}"
            f"log start. \n"
            f"date: {date_str}\n"
            f"time: {time_str}\n"
            f"{formatted_output}{old_text}"
            f"{DEFAULT_SEPARATOR}"
        ),
        encoding="utf-8",
    )

    completion_log = paths.chat_completions_dir / f"chat_completion_{current_datetime}.log"
    completion_log.write_text(
        (
            f"{'=' * 100}\n"
            f"log start.\n"
            f"{'=' * 100}\n"
            f"{json.dumps(response.model_dump(), indent=2, ensure_ascii=False)}\n"
            f"{'=' * 100}\n"
        ),
        encoding="utf-8",
    )
    return responses_log, completion_log


def list_prompt_files(paths: AppPaths) -> list[str]:
    names = {path.name for path in paths.prompts_dir.glob("prompt*.txt")}
    try:
        pkg_dir = resources.files("image_agent.resources.prompt")
        names.update(item.name for item in pkg_dir.iterdir() if item.name.startswith("prompt") and item.name.endswith(".txt"))
    except (ModuleNotFoundError, FileNotFoundError):
        pass
    return sorted(names)


def load_prompt_text(prompt_name: str, paths: AppPaths) -> str:
    prompt_path = paths.prompts_dir / prompt_name
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")

    try:
        return resources.files("image_agent.resources.prompt").joinpath(prompt_name).read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Prompt file not found: {prompt_name}") from exc


def choose_from_list(items: Iterable[str], prompt_text: str) -> str:
    choices = list(items)
    if not choices:
        raise ValueError("No choices available.")

    for idx, item in enumerate(choices):
        print(f"[{idx}] {item}")

    while True:
        raw_selection = input(prompt_text).strip()
        if not raw_selection:
            print("Please enter a selection.")
            continue
        if not raw_selection.isdigit():
            print("Please enter the number shown beside the option.")
            continue

        selection = int(raw_selection)
        if 0 <= selection < len(choices):
            return choices[selection]

        print(f"Please choose a number between 0 and {len(choices) - 1}.")
