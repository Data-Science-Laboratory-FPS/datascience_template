# analysis

Main analysis workspace.

Use this folder for Quarto notebooks, shared analysis configuration, and generated analysis artifacts. The notebooks are intended to run in order:

1. `01_dataset.qmd`: build and validate the analytical dataset.
2. `02_tables.qmd`: create descriptive and comparative tables.
3. `03_model.qmd`: train, validate, and summarize models.
4. `04_figures.qmd`: create publication-ready figures.

Generated analysis outputs should stay in stable folders:

- `tables/` for exported descriptive and reporting tables.
- `model/` for model outputs, model tables, and model figures.
- `figures/` for final publication figures.
- `render/html/` for Quarto HTML renders and their `*_files/` asset folders.
- `render/pdf/`, `render/logs/`, and `render/pdf_parts/` for PDF rendering with `scripts/render_pdf.py`.
- `render/pdf_preamble.tex` for the shared PDF style.
