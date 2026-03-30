from __future__ import annotations

import sys
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from image_agent.cli import build_parser, main
from image_agent.config import AppPaths, load_config
from image_agent.utils import choose_from_list, format_response_text


class SmokeTests(unittest.TestCase):
    def test_parser_builds(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--fullscreen", "--list-prompts"])
        self.assertTrue(args.fullscreen)
        self.assertTrue(args.list_prompts)

    def test_cli_list_prompts(self) -> None:
        exit_code = main(["--list-prompts", "--fullscreen"])
        self.assertEqual(exit_code, 0)

    def test_choose_from_list_reprompts_until_valid_selection(self) -> None:
        with patch("builtins.input", side_effect=["", "abc", "4", "1"]):
            selected = choose_from_list(["first", "second"], "choose...")
        self.assertEqual(selected, "second")

    def test_cli_reports_missing_prompt_file(self) -> None:
        exit_code = main(["--prompt-file", "missing.txt", "--fullscreen", "--once"])
        self.assertEqual(exit_code, 2)

    def test_load_config_prefers_model_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.json"
            config_path.write_text('{"MODEL":"gpt-5","MODEL_NAME":"gpt-5-mini"}', encoding="utf-8")
            paths = AppPaths.discover(project_root=tmpdir)
            config = load_config(paths)
        self.assertEqual(config["MODEL"], "gpt-5")
        self.assertEqual(config["MODEL_NAME"], "gpt-5")

    def test_load_config_supports_legacy_model_name_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.json"
            config_path.write_text('{"MODEL_NAME":"gpt-5"}', encoding="utf-8")
            paths = AppPaths.discover(project_root=tmpdir)
            config = load_config(paths)
        self.assertEqual(config["MODEL"], "gpt-5")

    def test_format_response_text_renders_escaped_newlines(self) -> None:
        formatted = format_response_text("line1\\nline2\\r\\nline3\\tend")
        self.assertEqual(formatted, "line1\nline2\nline3\tend")


if __name__ == "__main__":
    unittest.main()
