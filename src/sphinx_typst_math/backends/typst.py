"""Official Typst compiler backend."""

from __future__ import annotations

import json
from collections.abc import Hashable, Sequence
from pathlib import Path
from typing import Any

import typst
from packaging.version import InvalidVersion, Version

from ..backend import MathRenderingError
from ..mathml import extract_mathml

MINIMUM_TYPST_VERSION = Version("0.15")


class TypstBackend:
    """Render math through a reusable :class:`typst.Compiler` instance."""

    def __init__(
        self,
        preamble: str = "",
        imports: Sequence[str] = (),
        cache: bool = True,
        root: str | Path | None = None,
    ) -> None:
        self.preamble = preamble
        self.imports = tuple(imports)
        self.cache_enabled = cache
        self.root = str(root) if root is not None else None
        self.version = _validated_typst_version()
        self._compiler = (
            typst.Compiler(root=self.root)
            if self.root is not None
            else typst.Compiler()
        )
        self._cache: dict[tuple[Hashable, ...], str] = {}

    @property
    def cache_size(self) -> int:
        """Return the number of rendered expressions cached by this backend."""
        return len(self._cache)

    def render(self, source: str, display: bool) -> str:
        """Compile one native Typst expression and return its MathML element."""
        key = (
            source,
            display,
            self.preamble,
            self.imports,
            self.root,
            "typst",
            self.version,
        )
        if self.cache_enabled and key in self._cache:
            return self._cache[key]

        document = _make_document(
            source,
            display=display,
            preamble=self.preamble,
            imports=self.imports,
        )
        try:
            html = self._compiler.compile(input=document.encode("utf-8"), format="html")
            if not isinstance(html, bytes):
                raise MathRenderingError(
                    "Typst returned multiple HTML outputs for one equation"
                )
            rendered = extract_mathml(html)
        except Exception as exc:
            diagnostic = getattr(exc, "diagnostic", None) or str(exc)
            raise MathRenderingError(
                "Typst failed to compile the expression\n"
                f"expression: {source!r}\n"
                f"diagnostic:\n{diagnostic}"
            ) from exc

        if self.cache_enabled:
            self._cache[key] = rendered
        return rendered


def _validated_typst_version() -> str:
    raw_version: Any = getattr(typst, "__version__", None)
    try:
        version = Version(str(raw_version))
    except InvalidVersion as exc:
        raise MathRenderingError(
            f"cannot determine the installed typst-py version: {raw_version!r}"
        ) from exc
    if version < MINIMUM_TYPST_VERSION:
        raise MathRenderingError(
            f"typst-py >= {MINIMUM_TYPST_VERSION} is required for HTML/MathML "
            f"export; found {version}"
        )
    return str(version)


def _make_document(
    source: str, *, display: bool, preamble: str, imports: Sequence[str] = ()
) -> str:
    expression = source.strip()
    math = f"$ {expression} $" if display else f"${expression}$"
    parts = [
        f"#import {json.dumps(target, ensure_ascii=False)}: *" for target in imports
    ]
    if preamble.strip():
        parts.append(preamble.rstrip())
    parts.append(math)
    return "\n".join(parts) + "\n"
