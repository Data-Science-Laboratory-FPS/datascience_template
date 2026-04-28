# Workflow Execution Rules

## Notebook Structure
- 01_dataset.qmd: Dataset preparation including setup, pipeline functions, data sources, cohort definition, feature engineering, quality control, export, and session info
- 02_tables.qmd: Table generation including setup, load final dataset, cohort overview, baseline characteristics, standardized mean differences, outcome tables, subgroup analyses, sensitivity analyses, export tables, and session info
- 03_model.qmd: Model development including setup, load analytical dataset, data splitting, model training, validation, performance metrics, explainability, export model results, and session info
- 04_figures.qmd: Figure generation including setup, load analytical inputs, cohort flow figures, data completeness figures, baseline distribution figures, covariate balance figures, outcome figures, subgroup figures, sensitivity analysis figures, figure styling and annotation, export figures, and session info

## Responsibilities by Notebook
- 01_dataset.qmd: Import, merge, cohort definition, feature engineering, missingness handling, imputation, QC, save final dataset
- 02_tables.qmd: Baseline tables, SMD, outcome tables, subgroup tables, sensitivity tables, export
- 03_model.qmd: Data splitting, training, tuning, validation, metrics, CI, model explainability, export predictions/results
- 04_figures.qmd: CONSORT, missingness plots, distributions, balance plots, outcome figures, sensitivity figures, export

## Inputs
- Inputs can come from SQL, CSV, parquet, Excel, or intermediate generated files
- Use single source of truth between notebooks

## Imputation
- Deterministic rule-based imputation by data type as baseline
- Advanced imputation only when justified

## Outputs Naming
- final_dataset
- table1_df
- smd_table
- model_results
- figure_paths

## Rules
- Use Python for analysis
- Store table outputs in tables/
- Store figure outputs in figures/
- Reference SQL files from sql/
- Store references in ref/
- Sections in .qmd must include methodological narrative, not just headings
- Model performance figures go in 03_model.qmd, not 04_figures.qmd
- 02_tables.qmd does not contain model metrics