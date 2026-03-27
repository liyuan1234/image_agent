from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from image_agent.cli import build_parser, main


class SmokeTests(unittest.TestCase):
    def test_parser_builds(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--fullscreen", "--list-prompts"])
        self.assertTrue(args.fullscreen)
        self.assertTrue(args.list_prompts)

    def test_cli_list_prompts(self) -> None:
        exit_code = main(["--list-prompts", "--fullscreen"])
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
