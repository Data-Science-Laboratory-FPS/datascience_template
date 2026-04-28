# Workflow Execution Rules

Template author: MAA, Data Science Lab, Progress and Health Public Foundation (FPS), Regional Ministry of Health, Andalucía, Sevilla.

## Notebook Structure
- 01_dataset.qmd: Dataset preparation including setup, pipeline functions, data sources, cohort definition, feature engineering, quality control, export, and session info
- 02_tables.qmd: Table generation including setup, load final dataset, cohort overview, baseline characteristics, standardized mean differences, outcome tables, subgroup analyses, sensitivity analyses, export tables, and session info
- 03_model.qmd: Model development including setup, load analytical dataset, data splitting, model training, validation, performance metrics, explainability, export model results, and session info
- 04_figures.qmd: Figure generation including setup, load analytical inputs, cohort flow figures, data completeness figures, baseline distribution figures, covariate balance figures, outcome figures, subgroup figures, sensitivity analysis figures, figure styling and annotation, export figures, and session info

## Responsibilities by Notebook
- 01_dataset.qmd: Optional SQL loading, import, source cache, merge, cohort definition, long-to-wide domain construction, feature engineering, missingness assessment, imputation, imputation report, QC, save final dataset
- 02_tables.qmd: Load exported analytical artifacts, cohort overview, baseline tables, SMD, outcome tables, subgroup tables, sensitivity tables, publication-ready exports, optional interactive review tables
- 03_model.qmd: Data splitting, training, tuning, validation, metrics, CI, model explainability, export predictions/results
- 04_figures.qmd: CONSORT, missingness plots, distributions, balance plots, outcome figures, sensitivity figures, export

## Inputs
- Inputs can come from SQL, CSV, parquet, Excel, or intermediate generated files
- Use single source of truth between notebooks
- When SQL is used, read SQL from files in `analysis/sql/` near the start of `01_dataset.qmd`
- Do not embed long SQL strings inside notebooks
- SQL should perform extraction and light source cleaning; cohort logic, outcome definitions, feature engineering, and imputation stay in `01_dataset.qmd`

## Imputation
- Deterministic rule-based imputation by data type as baseline
- Advanced imputation only when justified
- Outcomes are never imputed
- Cohort-defining variables are never imputed unless explicitly justified in the notebook narrative
- Event dates are not imputed when missingness represents absence of the event
- Missingness indicators must be created before imputation for imputed variables
- `01_dataset.qmd` must render an imputation report immediately after imputation, listing imputed variables, skipped variables, methods, thresholds, and remaining expected missingness

## 01_dataset.qmd Conventions
- All code, comments, printed output labels, and narrative must be in English
- Define the unit of analysis before merging sources
- Keep source import separate from cohort definition and feature engineering
- Prefer one source-domain object per file or SQL query
- Use cached parquet plus a manifest for large raw or harmonized sources when repeated parsing is expensive
- Keep longitudinal/event-level tables before aggregating to the wide analytical dataset
- Document aggregation rules explicitly: first, latest, ever, count, sum, min, and max
- Apply domain prefixes at final export unless the project has a stronger reason to prefix earlier
- Export `final_dataset` as the downstream single source of truth
- Export cohort counts, a column manifest or dictionary, and retained longitudinal tables when applicable

## 02_tables.qmd Conventions
- All code, comments, printed output labels, and narrative must be in English
- `02_tables.qmd` consumes artifacts from `01_dataset.qmd`; it does not rebuild the analytical dataset
- Use explicit file checks for required inputs and fail with a clear message naming the upstream producer
- Keep a central `TABLE_REGISTRY`; edit the registry to reorder or rename outputs
- Define reusable table helpers near the top: variable checks, constant-variable removal, conservative categorical inference, display labels, and export functions
- Drop variables with no non-null variance before TableOne, SMD, or formal tests
- Binary 0/1 indicator variables may be displayed as presence-only `n (%)` rows; do not apply this to variables where both levels are independently meaningful
- Continuous variables default to median [IQR] and non-parametric tests unless the project states otherwise
- Categorical variables default to n (%) and chi-square or Fisher exact tests as appropriate
- Do not show a missingness column by default unless the table is specifically about missing data
- Centralize display labels in a rename map and restore acronyms after generated title-casing
- Every manuscript-ready table must include a footnote describing summary statistics, tests, grouping, and any important display convention
- Word `.docx` export should be publication-oriented when requested: stable widths, readable font size, minimal borders, and landscape layout for wide tables
- Optional interactive HTML tables can include sections, filters, p-value coloring, and direction badges for internal review
- SMD tables are for covariate balance and must be kept separate from model performance metrics

## 03_model.qmd Conventions
- All code, comments, printed output labels, and narrative must be in English
- `03_model.qmd` consumes analytical artifacts from `01_dataset.qmd`; it does not redefine cohorts, outcomes, or feature engineering
- State the model family and scientific goal before fitting: predictive classification, predictive regression, causal/treatment-effect, time-to-event, or another explicitly justified family
- For predictive classification and regression, split before any preprocessing and fit imputation, scaling, encoding, feature selection, and resampling inside training-only pipelines
- For predictive models, evaluate final performance only on held-out data and report metrics aligned with the intended use, including calibration when probabilities are produced
- For causal or treatment-effect models, define the estimand, justify confounders, report balance with SMD, and keep effect estimates separate from predictive performance metrics
- For time-to-event models, define index date, event date, censoring date, and follow-up in `01_dataset.qmd`; verify all predictors are baseline or pre-index unless modeling time-varying effects
- Cox-specific practices must be labeled as Cox-only: hazard ratios, proportional hazards assumptions, age/sex-adjusted Cox screening, event-per-level filters, HR forest plots, adjusted survival curves, and risk-group bounds
- Do not copy Cox variable-screening rules to classification, regression, or non-Cox survival models without a documented reason
- Export model outputs needed downstream: predictions, coefficients or effect estimates, uncertainty intervals, selected variables, exclusion reports, diagnostics, model objects, and figure source data

## Outputs Naming
- final_dataset
- table1_df
- smd_table
- model_results
- figure_paths
- analysis_notebooks_combined.pdf

## Output Locations
- Machine-readable and manuscript-ready table outputs must be written under `analysis/tables/`
- Model outputs, model tables, and model figures must be written under `analysis/model/`
- Final publication figure outputs must be written under `analysis/figures/`
- Quarto HTML renders and their `*_files/` asset folders must stay under `analysis/render/html/`
- Do not leave generated `.html` files or `*_files/` folders in the top level of `analysis/`
- Use `analysis/_quarto.yml` as the source of truth for Quarto HTML output location

## Combined PDF Report
- Use `python3 scripts/render_pdf.py all` from the project root to render completed `.qmd` notebooks into one PDF
- Use selections such as `1-2`, `1,3,4`, or `analysis/02_tables.qmd` while notebooks are being developed
- Logs are written to `analysis/render/logs/`
- Individual rendered PDF parts are written to `analysis/render/pdf_parts/`
- The combined report is written to `analysis/render/pdf/analysis_notebooks_combined.pdf` by default
- The shared PDF style is controlled by `analysis/render/pdf_preamble.tex`
- Ghostscript `gs` is required for PDF merging

## Rules
- Use Python for analysis
- Store table outputs in tables/
- Store model outputs in model/
- Store final figure outputs in figures/
- Store Quarto HTML renders in render/html/
- Reference SQL files from sql/
- Store references in ref/
- Sections in .qmd must include methodological narrative, not just headings
- Model performance figures go in 03_model.qmd, not 04_figures.qmd
- 02_tables.qmd does not contain model metrics
