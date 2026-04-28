# Project Overview

Template author: MAA, Data Science Lab, Progress and Health Public Foundation (FPS), Regional Ministry of Health, Andalucía, Sevilla.

This repository contains a reproducible data science workflow for clinical or health-related data analysis.

## Project Structure

```
project_root/
├── CLAUDE.md
├── README.md
├── scripts/
│   └── render_pdf.py
└── analysis/
    ├── CLAUDE.md
    ├── pdf_preamble.tex
    ├── ref/
    ├── sql/
    │   └── CLAUDE.md
    ├── tables/
    ├── figures/
    ├── 01_dataset.qmd
    ├── 02_tables.qmd
    ├── 03_model.qmd
    └── 04_figures.qmd
```

## Notebook Responsibilities

| Notebook | Purpose |
|----------|---------|
| 01_dataset.qmd | Build the analytical dataset: import, clean, cohort definition, feature engineering, imputation, QC |
| 02_tables.qmd | Generate descriptive and comparative tables: baseline, SMD, outcomes, subgroups, sensitivity |
| 03_model.qmd | Model training and validation: splitting, training, metrics, performance figures, explainability |
| 04_figures.qmd | Create descriptive figures: cohort flow, distributions, balance, outcomes, sensitivity |

## Execution Order

1. Run 01_dataset.qmd to prepare the dataset
2. Run 02_tables.qmd for tables
3. Run 03_model.qmd for modeling (if applicable)
4. Run 04_figures.qmd for figures

## Input Sources

- SQL queries (if available)
- CSV, parquet, Excel files
- Intermediate outputs from previous notebooks

## Dependencies

- Python 3.x
- Quarto
- Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn, etc.

## How to Run

1. Open in VS Code with Quarto extension
2. Execute notebooks in order
3. Outputs saved in tables/ and figures/

## Combined PDF Report

Render completed Quarto notebooks into one styled PDF:

```bash
python3 scripts/render_pdf.py all
```

Useful selections:
- `python3 scripts/render_pdf.py 1-2`
- `python3 scripts/render_pdf.py 1,3,4 --title "Project Analysis Report"`
- `python3 scripts/render_pdf.py all --strict`

## Output Artifacts

- final_dataset (parquet/CSV)
- table1_df, smd_table (dataframes)
- model_results (pickles/predictions)
- figure_paths (PNG/PDF/SVG)
- analysis/rendered/analysis_notebooks_combined.pdf

## Reference Documents

See analysis/ref/ for scientific references, protocols, and methodological notes.
