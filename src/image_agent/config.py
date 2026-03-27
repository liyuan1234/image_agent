from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = {
    "APPNAME": "",
    "MODEL_NAME": "gpt-5-mini",
    "MAX_OUTPUT_TOKENS": 16000,
    "PROMPT_FILE": "prompt_dota2.txt",
    "SIMILARITY_THRESHOLD": 0.98,
    "POLL_INTERVAL_SECONDS": 0.01,
}


@dataclass
class AppPaths:
    project_root: Path
    config_file: Path
    prompts_dir: Path
    images_dir: Path
    responses_dir: Path
    chat_completions_dir: Path

    @classmethod
    def discover(cls, project_root: str | Path | None = None, config_file: str | Path | None = None) -> "AppPaths":
        root = _discover_project_root(project_root, config_file)
        return cls(
            project_root=root,
            config_file=Path(config_file).expanduser().resolve() if config_file else root / "config.json",
            prompts_dir=root / "prompt",
            images_dir=root / "images",
            responses_dir=root / "responses",
            chat_completions_dir=root / "chat_completions",
        )

    def ensure_directories(self) -> None:
        for path in (self.prompts_dir, self.images_dir, self.responses_dir, self.chat_completions_dir):
            path.mkdir(parents=True, exist_ok=True)



def _discover_project_root(project_root: str | Path | None, config_file: str | Path | None) -> Path:
    if project_root:
        return Path(project_root).expanduser().resolve()

    candidates: list[Path] = []
    if config_file:
        candidates.append(Path(config_file).expanduser().resolve().parent)

    env_root = os.getenv("IMAGE_AGENT_PROJECT_ROOT")
    if env_root:
        candidates.append(Path(env_root).expanduser().resolve())

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    for candidate in candidates:
        if (candidate / "config.json").exists() or (candidate / "prompt").exists() or (candidate / "pyproject.toml").exists():
            return candidate

    return cwd



def load_config(paths: AppPaths) -> dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    if paths.config_file.exists():
        with paths.config_file.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
        config.update(loaded)
    return config
