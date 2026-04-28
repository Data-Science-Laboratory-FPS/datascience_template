#!/usr/bin/env bash

set -euo pipefail

TEMPLATE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 /path/to/project_root"
  exit 1
fi

PROJECT_ROOT="$1"
ANALYSIS_DIR="${PROJECT_ROOT}/analysis"
SCRIPTS_DIR="${PROJECT_ROOT}/scripts"
SQL_DIR="${ANALYSIS_DIR}/sql"
REF_DIR="${ANALYSIS_DIR}/ref"
TABLES_DIR="${ANALYSIS_DIR}/tables"
MODEL_DIR="${ANALYSIS_DIR}/model"
FIGURES_DIR="${ANALYSIS_DIR}/figures"
RENDER_DIR="${ANALYSIS_DIR}/render"
RENDERED_DIR="${RENDER_DIR}/pdf"
RENDERED_HTML_DIR="${RENDER_DIR}/html"
RENDER_PARTS_DIR="${RENDER_DIR}/pdf_parts"
RENDER_LOGS_DIR="${RENDER_DIR}/logs"

mkdir -p "$PROJECT_ROOT"
mkdir -p "$ANALYSIS_DIR"
mkdir -p "$SCRIPTS_DIR"
mkdir -p "$SQL_DIR"
mkdir -p "$REF_DIR"
mkdir -p "$TABLES_DIR"
mkdir -p "$MODEL_DIR"
mkdir -p "$FIGURES_DIR"
mkdir -p "$RENDER_DIR"
mkdir -p "$RENDERED_DIR"
mkdir -p "$RENDERED_HTML_DIR"
mkdir -p "$RENDER_PARTS_DIR"
mkdir -p "$RENDER_LOGS_DIR"

if [[ -f "${TEMPLATE_ROOT}/scripts/render_pdf.py" ]]; then
  cp "${TEMPLATE_ROOT}/scripts/render_pdf.py" "${SCRIPTS_DIR}/render_pdf.py"
  chmod +x "${SCRIPTS_DIR}/render_pdf.py"
fi

if [[ -f "${TEMPLATE_ROOT}/analysis/render/pdf_preamble.tex" ]]; then
  cp "${TEMPLATE_ROOT}/analysis/render/pdf_preamble.tex" "${RENDER_DIR}/pdf_preamble.tex"
fi

cat > "${PROJECT_ROOT}/CLAUDE.md" <<'EOT'
# PROJECT CONTEXT

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
- All code must be written in English
- Prefer modular workflows over monolithic notebooks
- SQL logic should be externalized in analysis/sql/
- Scientific and protocol references should be stored in analysis/ref/
- Avoid manual edits after output generation

## Documentation
Refer to:
- README.md for project overview
- analysis/CLAUDE.md for workflow execution rules
- analysis/sql/CLAUDE.md for SQL extraction rules
EOT

cat > "${PROJECT_ROOT}/README.md" <<'EOT'
# Project Overview

This repository contains a reproducible data science workflow for clinical or health-related data analysis.

## Recommended Structure

```text
project_root/
├── CLAUDE.md
├── README.md
└── analysis/
    ├── CLAUDE.md
    ├── ref/
    ├── sql/
    │   └── CLAUDE.md
    ├── tables/
    ├── model/
    ├── figures/
    ├── render/
    ├── 01_dataset.qmd
    ├── 02_tables.qmd
    ├── 03_model.qmd
    └── 04_figures.qmd
EOT

cat > "${ANALYSIS_DIR}/CLAUDE.md" <<'EOT'
# Workflow Execution Rules

## Notebook Structure
- 01_dataset.qmd: Data extraction, cleaning, and preparation
- 02_tables.qmd: Generate tables for analysis
- 03_model.qmd: Model development and validation
- 04_figures.qmd: Generate figures

## Rules
- Use R or Python for analysis
- Store table outputs in tables/
- Store model outputs in model/
- Store final figure outputs in figures/
- Store Quarto HTML renders in render/html/
- Reference SQL files from sql/
- Store references in ref/
EOT

cat > "${SQL_DIR}/CLAUDE.md" <<'EOT'
# SQL Extraction Rules

## Rules
- Write clear, commented SQL
- Use CTEs for complex queries
- Ensure reproducibility
- Document assumptions
EOT

touch "${ANALYSIS_DIR}/01_dataset.qmd"
touch "${ANALYSIS_DIR}/02_tables.qmd"
touch "${ANALYSIS_DIR}/03_model.qmd"
touch "${ANALYSIS_DIR}/04_figures.qmd"

# Prefer the maintained template files when this script is run from the
# datascience_template repository. The heredoc blocks above remain as a minimal
# fallback if the script is copied elsewhere without the template tree.
for file in CLAUDE.md README.md; do
  if [[ -f "${TEMPLATE_ROOT}/${file}" ]]; then
    cp "${TEMPLATE_ROOT}/${file}" "${PROJECT_ROOT}/${file}"
  fi
done

for file in 01_dataset.qmd 02_tables.qmd 03_model.qmd 04_figures.qmd CLAUDE.md; do
  if [[ -f "${TEMPLATE_ROOT}/analysis/${file}" ]]; then
    cp "${TEMPLATE_ROOT}/analysis/${file}" "${ANALYSIS_DIR}/${file}"
  fi
done

for file in _quarto.yml .gitignore; do
  if [[ -f "${TEMPLATE_ROOT}/analysis/${file}" ]]; then
    cp "${TEMPLATE_ROOT}/analysis/${file}" "${ANALYSIS_DIR}/${file}"
  fi
done

if [[ -f "${TEMPLATE_ROOT}/analysis/sql/CLAUDE.md" ]]; then
  cp "${TEMPLATE_ROOT}/analysis/sql/CLAUDE.md" "${SQL_DIR}/CLAUDE.md"
fi

if [[ -f "${TEMPLATE_ROOT}/analysis/ref/note_cohort_definition.md" ]]; then
  cp "${TEMPLATE_ROOT}/analysis/ref/note_cohort_definition.md" "${REF_DIR}/note_cohort_definition.md"
fi

if [[ -f "${ANALYSIS_DIR}/03_figures.qmd" && -f "${ANALYSIS_DIR}/04_figures.qmd" ]]; then
  rm -f "${ANALYSIS_DIR}/03_figures.qmd"
fi
