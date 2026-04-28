# analysis

Main analysis workspace.

Use this folder for Quarto notebooks, shared analysis configuration, and generated analysis artifacts. The notebooks are intended to run in order:

1. `01_dataset.qmd`: build and validate the analytical dataset.
2. `02_tables.qmd`: create descriptive and comparative tables.
3. `03_model.qmd`: train, validate, and summarize models.
4. `04_figures.qmd`: create publication-ready figures.

Common generated folders include `rendered/`, `render_logs/`, and `render_pdf_parts/` when `scripts/render_pdf.py` is used.
