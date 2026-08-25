"""Sphinx HTML visitors for Typst-backed MathML."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from docutils import nodes
from sphinx.errors import SphinxError
from sphinx.locale import _
from sphinx.util import logging
from sphinx.util.math import get_node_equation_number

from .backend import MathBackend, MathRenderingError
from .backends import TypstBackend

if TYPE_CHECKING:
    from sphinx.writers.html5 import HTML5Translator

logger = logging.getLogger(__name__)


class TypstMathError(SphinxError):
    """A fatal Typst math error during a Sphinx build."""

    category = "Typst math error"


def _get_backend(translator: HTML5Translator) -> MathBackend:
    builder = translator.builder
    backend = getattr(builder, "_sphinx_typst_math_backend", None)
    if backend is None:
        backend = TypstBackend(
            preamble=builder.config.typst_math_preamble,
            imports=builder.config.typst_math_imports,
            cache=builder.config.typst_math_cache,
            root=builder.srcdir,
        )
        builder.__dict__["_sphinx_typst_math_backend"] = backend
    return cast(MathBackend, backend)


def _location(node: nodes.Node) -> str:
    source = node.source or "<unknown Sphinx source>"
    return f"{source}:{node.line}" if node.line is not None else source


def _render(
    translator: HTML5Translator, node: nodes.math | nodes.math_block, *, display: bool
) -> str | None:
    source = node.astext()
    try:
        return _get_backend(translator).render(source, display=display)
    except MathRenderingError as exc:
        message = (
            f"Typst math rendering failed at {_location(node)}\n"
            f"source: {source!r}\n{exc}"
        )
        if translator.builder.config.typst_math_error_mode == "warn":
            logger.warning(message, location=node)
            return None
        raise TypstMathError(message) from exc


def _fallback(translator: HTML5Translator, source: str) -> str:
    return (
        '<code class="typst-math-error" title="Typst math rendering failed">'
        f"{translator.encode(source)}</code>"
    )


def visit_inline_math(translator: HTML5Translator, node: nodes.math) -> None:
    """Render an inline Sphinx math node as native MathML."""
    translator.body.append(
        translator.starttag(
            node,
            "span",
            "",
            CLASS="math notranslate nohighlight typst-math typst-math-inline",
        )
    )
    rendered = _render(translator, node, display=False)
    translator.body.append(
        rendered if rendered is not None else _fallback(translator, node.astext())
    )
    translator.body.append("</span>")
    raise nodes.SkipNode


def visit_block_math(translator: HTML5Translator, node: nodes.math_block) -> None:
    """Render a display Sphinx math node while retaining Sphinx numbering."""
    translator.body.append(
        translator.starttag(
            node,
            "div",
            CLASS="math notranslate nohighlight typst-math typst-math-display",
        )
    )
    if node.get("number"):
        number = get_node_equation_number(translator, node)
        translator.body.append(f'<span class="eqno">({number})')
        translator.add_permalink_ref(node, _("Link to this equation"))
        translator.body.append("</span>")

    rendered = _render(translator, node, display=True)
    translator.body.append(
        rendered if rendered is not None else _fallback(translator, node.astext())
    )
    translator.body.append("</div>\n")
    raise nodes.SkipNode
