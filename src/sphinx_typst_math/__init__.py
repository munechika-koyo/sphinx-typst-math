"""Sphinx extension for native Typst math rendered as MathML."""

from __future__ import annotations

from importlib.metadata import version as _version
from pathlib import Path
from typing import TYPE_CHECKING

from sphinx.errors import ConfigError

from .renderer import visit_block_math, visit_inline_math

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata


__version__ = _version("sphinx-typst-math")
_STATIC_DIR = Path(__file__).parent / "_static"


def _validate_config(app: Sphinx, config: Config) -> None:
    del app
    if config.typst_math_error_mode not in {"raise", "warn"}:
        raise ConfigError(
            "typst_math_error_mode must be either 'raise' or 'warn', "
            f"not {config.typst_math_error_mode!r}"
        )
    for index, target in enumerate(config.typst_math_imports):
        if not isinstance(target, str) or not target.strip():
            raise ConfigError(
                "typst_math_imports entries must be non-empty strings; "
                f"entry {index} is {target!r}"
            )
    static_dir = str(_STATIC_DIR)
    if static_dir not in config.html_static_path:
        config.html_static_path.append(static_dir)


def setup(app: Sphinx) -> ExtensionMetadata:
    """Register the ``typst`` HTML math renderer and its configuration."""
    app.add_html_math_renderer(
        "typst",
        inline_renderers=(visit_inline_math, None),
        block_renderers=(visit_block_math, None),
    )
    app.add_config_value("typst_math_preamble", "", "html", types=frozenset({str}))
    app.add_config_value(
        "typst_math_imports", [], "html", types=frozenset({list, tuple})
    )
    app.add_config_value(
        "typst_math_error_mode", "raise", "html", types=frozenset({str})
    )
    app.add_config_value("typst_math_cache", True, "html", types=frozenset({bool}))
    app.add_css_file("sphinx-typst-math.css")
    app.connect("config-inited", _validate_config)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


__all__ = ["__version__", "setup"]
