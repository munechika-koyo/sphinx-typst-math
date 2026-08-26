# sphinx-typst-math

`sphinx-typst-math` is a Sphinx HTML math renderer for **native Typst math
syntax**. It sends each equation to the official Typst compiler through
[`typst-py`](https://github.com/messense/typst-py), extracts the compiler's
MathML, and places that MathML directly into Sphinx's HTML.

There is no Typst-to-LaTeX conversion, MathJax runtime, custom math parser, or
Node.js dependency.

## Documentation and live demo

See the [GitHub Pages demo](https://munechika-koyo.github.io/sphinx-typst-math/)
for rendered examples using MyST Markdown, reStructuredText, Typst Universe
packages, and nbsphinx notebooks. The documentation source is available in the
[`docs/`](docs/) directory.

> [!IMPORTANT]
> Typst 0.15 introduced HTML equation export. This package therefore requires
> `typst-py >= 0.15`.

## Installation

```bash
pip install sphinx-typst-math
```

MyST Parser, nbsphinx, and sphinx-immaterial are optional integrations. Install
the ones used by your documentation project separately.

## Quick start

```python
# conf.py

extensions = [
    "myst_parser",
    "nbsphinx",
    "sphinx_typst_math",
]

html_math_renderer = "typst"

myst_enable_extensions = [
    "dollarmath",
]
```

Then use Typst—not LaTeX—between Markdown math delimiters:

```markdown
$sum_(i=1)^n x_i$

$$
integral_0^infinity e^(-x^2) dif x
= sqrt(pi) / 2
$$
```

The same Markdown can be placed in a Jupyter notebook Markdown cell when the
notebook is built by nbsphinx and Sphinx. JupyterLab's own live Markdown
preview is separate from a Sphinx build and may still use MathJax, so it may
not preview Typst syntax correctly.

Do not enable `sphinx.ext.mathjax`; it is not needed. If another extension has
registered a math renderer, keep `html_math_renderer = "typst"` explicit.

## Configuration

```python
html_math_renderer = "typst"

# Each entry is imported with `: *` before the preamble and equation.
typst_math_imports = [
    "@preview/physica:0.9.8",
]

# Inserted after imports and immediately before each equation. Useful for
# shared definitions and selective import statements.
typst_math_preamble = """
#let sq(x) = $x^2$
"""

# "raise" stops the build; "warn" emits a warning and escaped fallback markup.
typst_math_error_mode = "raise"

# Cache equal source/display/import/preamble/compiler combinations for this build.
typst_math_cache = True
```

Every `typst_math_imports` entry expands to `#import "…": *`. Typst packages
must include their namespace and exact version. Local import paths and relative
preamble imports resolve from the Sphinx source directory. For a selective
import, put the complete statement in `typst_math_preamble` instead:

```python
typst_math_preamble = r"""
#import "@preview/physica:0.9.8": dv, pdv
"""
```

Imports, the preamble, and equation source are evaluated by the real Typst compiler.
Sphinx source files and configuration are therefore assumed to be trusted
build inputs.

## Equation numbers and references

The primary workflow is MyST Markdown. With MyST Parser and the `dollarmath`
extension enabled as shown in the quick start, append a label in parentheses
to a display-math block and reference it with MyST's `{eq}` role:

<!-- dprint-ignore -->
```markdown
$$
E = m c^2
$$ (energy)

See {eq}`energy`.
```

The renderer retains the IDs and numbering assigned structurally by Sphinx,
so equivalent math nodes produced by reStructuredText or integrations such as
nbsphinx remain compatible even though MyST Markdown is the primary documented
input format.

Typst source is not inspected for LaTeX commands such as `\label`, `\tag`, or
`\eqref`. Labels must be represented by Sphinx/MyST nodes. In particular,
notebook labels that depend on LaTeX-internal commands are not supported in
the first release.

## HTML and theme behavior

Inline nodes use a standard Sphinx `span.math` wrapper. Display nodes use a
standard `div.math` wrapper, including Sphinx's `eqno` and `headerlink` markup
when numbered. The equation itself is native MathML, inherits the surrounding
text color, and has no hard-coded background. This also keeps the renderer
compatible with sphinx-immaterial light and dark color schemes without
theme-specific CSS.

This extension changes HTML math rendering only. Other Sphinx builders retain
their own math handling and may still expect LaTeX input.

## Alternative backends

The first release intentionally has no Kern backend. Kern is a useful
JavaScript renderer with its own Typst-like lexer, parser, and MathML emitter,
but it is not the official Typst compiler and documents parity gaps for some
constructs. Adding it would also introduce a separate compatibility surface
and potentially a Node.js workflow. It can be reconsidered later as an
explicit opt-in backend; it is not suitable as the compatibility-preserving
default.

## Development

The repository includes Pixi environments for development, documentation, testing, and
package builds. The default environment uses Python 3.14.

```bash
pixi install
pixi run lint
pixi run test
pixi run build
pixi run doc-build && pixi run doc-serve
pixi publish --path . --target-dir dist/conda
```

The `lint` task runs all configured pre-commit checks, and the `test` task runs
the full pytest suite. Python 3.11 through 3.14 are available as the `py311`,
`py312`, `py313`, and `py314` environments; for example:

```bash
pixi run --environment py311 test
```

The `build` task runs in its dedicated Pixi environment and creates the wheel
and source distribution.
The `doc-build` and `doc-serve` tasks build and serve the Sphinx documentation
locally.
`pixi publish --path . --target-dir dist/conda` uses
the Pixi build backend to create a Conda package in `dist/conda`.

The test suite compiles real Typst equations and builds real MyST, nbsphinx,
and sphinx-immaterial projects. CI invokes the same Pixi tasks used locally.
