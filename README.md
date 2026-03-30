# GPIC / image-agent

A small Python tool that watches a window or the primary display, waits for the image to change, sends the updated screenshot plus a prompt to the OpenAI Responses API, and logs the model output.

## What it does

- monitor a selected window or fullscreen
- detect scene/image changes with SSIM
- send the changed image to the OpenAI Responses API
- log text output and raw response payloads
- use prompt files for different tasks like trading or game guidance

## Project layout

```text
image_agent/
├── config.json
├── prompt/
├── src/image_agent/
├── tests/
└── pyproject.toml
```

The package code now lives under `src/image_agent` and can be run either as an installed CLI or with `python -m image_agent`.

## Requirements

- Python 3.9+
- an `OPENAI_API_KEY` environment variable
- screen capture permissions enabled for your OS when needed

## Install

### Editable install for development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

### Standard install

```bash
pip install .
```

## Configure

Set your API key:

```bash
export OPENAI_API_KEY="sk-your_api_key_here"
```

Optional settings live in `config.json`:

```json
{
  "APPNAME": "",
  "MODEL": "gpt-5-mini",
  "MAX_OUTPUT_TOKENS": 16000,
  "PROMPT_FILE": "prompt_dota2.txt",
  "SIMILARITY_THRESHOLD": 0.98,
  "POLL_INTERVAL_SECONDS": 0.01
}
```

To switch models, edit only this line:

```json
"MODEL": "gpt-5-mini"
```

For example:

```json
"MODEL": "gpt-5"
```

The app still accepts the older `MODEL_NAME` key for backward compatibility, but `MODEL` is now the preferred setting.

### Paths

By default, the app looks for `config.json`, `prompt/`, and output folders from the project root it discovers from:

1. `--project-root`
2. `--config`
3. `IMAGE_AGENT_PROJECT_ROOT`
4. the current working directory and its parents

Outputs are written to:

- `images/`
- `responses/`
- `chat_completions/`

These folders are created automatically.

## Usage

### Interactive mode

```bash
image-agent
```

This lets you choose:

- which prompt file to use
- which window to monitor, or fullscreen

### Fullscreen mode

```bash
image-agent --fullscreen
```

### Monitor a specific window

```bash
image-agent --window "Dota 2"
```

### Use a specific prompt file

```bash
image-agent --prompt-file prompt_trading.txt --fullscreen
```

### One-shot run

Useful for debugging wiring after the next visual change:

```bash
image-agent --fullscreen --once
```

### Module execution

```bash
python -m image_agent --fullscreen
```

### Helper commands

```bash
image-agent --list-prompts
image-agent --list-windows
```

## Prompts

Prompt files are loaded from the repo-level `prompt/` directory when present. Bundled fallback prompts also ship inside the package, so the CLI still works after installation.

## Legacy compatibility

The old script entry point remains as a thin wrapper:

```bash
python main/chatgpt_assistant.py
```

But the recommended way is now:

```bash
image-agent
```

## Smoke test

A tiny import/CLI smoke test is included:

```bash
python -m unittest discover -s tests
```

It does not hit OpenAI or require a network call.

## Notes / caveats

- Window discovery depends on the platform and `pywinctl` support.
- Fullscreen capture behavior depends on OS capture permissions.
- The tool waits for a detected image change before sending the next request.
