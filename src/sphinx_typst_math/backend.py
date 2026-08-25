"""Backend contracts and errors for math rendering."""

from __future__ import annotations

from typing import Protocol


class MathRenderingError(RuntimeError):
    """Raised when a backend cannot render a Typst expression."""


class MathBackend(Protocol):
    """A renderer that turns Typst source into one MathML element."""

    def render(self, source: str, display: bool) -> str:
        """Return exactly one serialized MathML ``math`` element."""
        ...
