# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```sh
uv run streamlit run streamlit_app.py
```

## Architecture

This is a single-page Streamlit app (`streamlit_app.py`) with one reference script (`recipe_polis2_statements.py`, a Colab notebook export kept for reference — not imported by the app).

### Data Flow

1. User pastes a Pol.is report URL (or pre-fills via `?report=...&lang=...` query params)
2. `val.datasets.polis.load(url, translate_to=...)` fetches the report into an [AnnData](https://anndata.readthedocs.io/) object
3. `val.tools.recipe_polis2_statements(adata)` runs the Polis2 pipeline (UMAP, clustering, etc.)
4. `datamapplot.create_interactive_plot(...)` renders the result as an interactive HTML widget

### AnnData conventions

- **Statements** live on the `.var` axis (columns), not `.obs`
- `adata.varm["content_umap"]` — 2D UMAP coordinates per statement
- `adata.varm["evoc_polis2"]` — hierarchical cluster labels (zoom levels × statements); transposed before passing to datamapplot
- `adata.var["content"]` — raw statement text used for hover tooltips

### Key dependencies

| Package | Role |
|---|---|
| `valency-anndata` | Polis data loader + recipe pipeline (GitHub dep) |
| `polismath-commentgraph` | ML backend for embeddings/clustering; **Linux-only** (no macOS x86_64 wheel) — not installed locally |
| `datamapplot` | Interactive HTML scatter plot |
| `streamlit` | UI framework |

Because `polismath-commentgraph` is gated to `sys_platform == 'linux'`, the full pipeline only runs on Streamlit Cloud (Linux). Local macOS runs will fail when `val.tools.recipe_polis2_statements` is called.
