# SQL Extraction Rules

This file applies only if the project has a SQL extraction layer.

## Naming by Domains
- Use descriptive names by data domains
- Examples: demographics.sql, baseline_labs.sql, outcomes_followup.sql

## Separation of Logic
- Extraction logic: data pulling and basic cleaning
- Analysis logic: cohort definitions, derived variables (keep in notebooks)

## Rules
- Write clear, commented SQL
- Use CTEs for complex queries
- Ensure reproducibility
- Document assumptions
- Do not include analytical decisions that are not traceable outside SQL

## QC in SQL
- Check for duplicates
- Ensure key uniqueness
- Validate date filters
- Check domain plausibility

## Structure
- Flat folder or subfolders by domain, but consistent
- Reference from notebooks without embedding SQL logic