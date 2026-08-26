# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-26

### Added

- Add native Typst-to-MathML rendering for inline and display Sphinx math nodes.
- Preserve Sphinx equation numbers, IDs, references, and permalinks.
- Support math nodes produced by MyST Markdown, reStructuredText, and nbsphinx.
- Add configurable preamble, build-local rendering cache, and diagnostic modes.
- Add `typst_math_imports` for importing versioned Typst packages or local modules.
- Add sphinx-immaterial demonstration documentation with source-and-result examples
  for native Typst, `physica`, MiTeX, `quick-maths`, and Jupyter notebooks.
- Add GitHub Pages deployment and parameterized Pixi tasks for building and serving
  the documentation locally.
