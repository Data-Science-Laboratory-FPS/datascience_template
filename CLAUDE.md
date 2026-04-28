# PROJECT CONTEXT

## Workflow Standard
The base standard pipeline is:
- 01_dataset.qmd: Build the analytical dataset
- 02_tables.qmd: Descriptive and comparative tables
- 03_model.qmd: Training, validation, metrics, performance figures
- 04_figures.qmd: Descriptive, balance, outcome, and sensitivity figures

## Language and Style
- All code and comments must be written in English only
- Default environment is Quarto + Python
- Methodological decisions must be separated by notebook and not mixed

## Imputation Rules
- Same technique per data type within a project
- Do not impute outcomes
- Do not impute cohort-defining variables unless justified

## Separation Between Stages
- Dataset construction in 01_dataset.qmd
- Descriptive tables in 02_tables.qmd
- Model metrics and performance figures in 03_model.qmd
- Descriptive figures in 04_figures.qmd

## Traceability and Reproducibility
- All assumptions must be traceable
- Avoid manual edits after output generation
- Use single source of truth between notebooks

## Objective
Define the clinical or analytical objective clearly.

Examples:
- Predict ICU mortality at 72h
- Evaluate treatment effectiveness using IPTW
- Build a clinical decision support workflow
- Generate publication-ready descriptive and analytical outputs

## Data Source
Document:
- source system or database
- temporal coverage
- unit of analysis
- main domains included

Examples:
- hospital EHR
- administrative claims
- ICU research database
- population-level registry

## Key Constraints
- Observational data may contain confounding
- Missing data must be handled explicitly
- Temporal alignment must be checked
- Cohort definition must be reproducible
- Clinical assumptions must be traceable

## Expected Outputs
- Clean analytical dataset
- Reproducible tables
- Reproducible figures
- Traceable scientific references
- Project documentation suitable for collaboration and audit

## Project Rules
- Prefer modular workflows over monolithic notebooks
- SQL logic should be externalized in analysis/sql/
- Scientific and protocol references should be stored in analysis/ref/

## Documentation
Refer to:
- README.md for project overview
- analysis/CLAUDE.md for workflow execution rules
- analysis/sql/CLAUDE.md for SQL extraction rules