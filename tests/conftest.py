from __future__ import annotations

import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest


@pytest.fixture
def build_sphinx(tmp_path: Path):  # type: ignore[no-untyped-def]
    def build(
        files: Mapping[str, str], *, warning_is_error: bool = True
    ) -> tuple[subprocess.CompletedProcess[str], Path]:
        source = tmp_path / "source"
        output = tmp_path / "html"
        source.mkdir()
        for relative, content in files.items():
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        command = [sys.executable, "-m", "sphinx", "-b", "html"]
        if warning_is_error:
            command.append("-W")
        command.extend([str(source), str(output)])
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        return result, output

    return build
