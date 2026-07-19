# Capstone Project

This repository contains an end-to-end retail data lakehouse capstone implemented with synthetic data, AWS services (S3, Glue, Lake Formation, Athena), and Databricks (Bronze/Silver/Gold medallion ETL).

See the full project requirements and tasks in: `Capstone_Requirements_and_Tasks.pdf` (root).

## Project Phases

- Phase 0 — Environment Setup & Synthetic Data Generation: prepares cloud/Databricks environment and generates synthetic customer, product, order, order-item, and clickstream datasets. See `phase0.md` and `01_data_generation.ipynb`.

- Phase 1 — Data Profiling and Visualization: profiling of generated datasets, column/file-level summaries and charts. See `phase1.md` and `02_data_profiling_and_viz.ipynb`.

- Phase 2 — Data Lake Bucket Architecture: S3 Bronze/Silver/Gold layout, lifecycle, versioning, encryption, and event notifications. See `phase_3.md`.

- Phase 3 — AWS Glue Data Catalog & Query Results: Glue crawlers, discovered tables in `retailflow_raw` and example queries against those tables. See `phase-4.md`.

- Phase 5 — Lake Formation & Analytics Permissions: Lake Formation registration, LF tags, IAM roles and column-level access controls validated via Athena. See `phase_5.md`.

- Phase 8 — Databricks Medallion ETL & Validation: Bronze → Silver → Gold ETL implemented with notebooks and validation of Gold tables. See `phase8.md`, `bronze_silver_gold_pipeline.ipynb`, and `medallion_dlt.ipynb`.

## Requirements (high level)

- Cloud: AWS account with privileges to create S3 buckets, Glue Data Catalog, Lake Formation resources, KMS keys, IAM roles/policies, and Athena queries.
- Databricks: workspace with permission to run notebooks or jobs (DLT or Databricks jobs) and access to the S3 data lake.
- Local environment: Python 3.9+ to run utilities and notebooks locally (optional).
- Key Python packages (used across notebooks/scripts):
  - `boto3` (S3 ingestion helpers)
  - `pandas`, `numpy` (data handling)
  - `matplotlib`, `seaborn` (visualization)
  - `pyspark` / Databricks runtime / `delta` (Databricks ETL and Delta tables)
  - `databricks-sdk` or equivalent for workspace automation (optional)
  - `jupyter` / `notebook` to run notebooks locally (optional)

Note: `pyproject.toml` lists `boto3` as a dependency for the S3 ingest helper. Other packages are used in notebooks and should be installed in your environment as needed.

## Quick start (local)

1. Create and activate a Python virtual environment (Python 3.9+).

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt  # or install packages listed above
```

2. If you intend to run notebooks interactively, open them with Jupyter or in VS Code's Jupyter support.

3. To upload sample data to S3, follow `phase2_boto3_s3_upload.md`.

## Where to read more

- Project requirements and task list: `Capstone_Requirements_and_Tasks.pdf`.
- Phase documentation: `phase0.md`, `phase1.md`, `phase_3.md`, `phase-4.md`, `phase_5.md`, `phase8.md`.
- Notebooks and utilities: see the root notebooks.

