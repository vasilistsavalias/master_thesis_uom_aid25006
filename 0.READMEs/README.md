# GDM Project: Synthetic Data Generation Pipeline (V3 Architecture)

## 1. Project Synopsis

This repository contains the complete research and development pipeline for generating high-fidelity synthetic data for a Gestational Diabetes Mellitus (GDM) clinical dataset. The project's core is a robust, modular pipeline that performs data preparation, cross-validation of generative models (CTGAN, TVAE), results analysis, and final unbiased evaluation on a holdout set.

The project is designed with a "pipeline-first" philosophy, emphasizing modularity, reproducibility, and clarity. The entire workflow is broken down into a series of distinct, sequential stages, where each stage is a self-contained Python script with its own inputs and outputs. This structure ensures that the research is transparent, easy to follow, and extensible.

## 2. Core Architectural Principles

- **Sequential & Modular:** The project is a strict, one-way pipeline. Each stage is an independent script that can be run on its own, provided the previous stage's outputs are present.
- **Reproducibility:** By separating dependencies, configuration, and code, the entire experiment can be reliably reproduced with a single command.
- **Centralized Configuration:** All parameters, paths, and settings are managed in a single `config/config.yaml` file.
- **Separation of Concerns:** Source code (`src/`), generated artifacts (`outputs/`), and logs (`logs/`) are kept in separate, top-level directories.
- **Extensible Model Support:** The pipeline is designed to easily test multiple classical machine learning models (e.g., RandomForest, XGBoost, LogisticRegression). It also includes Gaussian Naive Bayes as a simple, fast baseline to ensure the more complex models are providing a significant performance uplift.

For a detailed, file-by-file breakdown of the codebase, please see the **[Pipeline Documentation](0.READMEs/pipeline.md)**.

---

## 3. Dataset Requirements

**Important:** Due to patient privacy and data ownership agreements, the `pregsafe_dataset.csv` used in this research is not included in this repository.

To run the pipeline with your own data, you must:

1. **Provide a CSV file:** Your dataset must be in the CSV format.
2. **Update the Configuration:** Open the `config/config.yaml` file and modify the following sections:
    - `data_ingestion.source_path`: Change this to the path of your CSV file.
    - `global_params.target_column`: Change this to the name of the target variable (dependent variable) in your dataset.
    - `feature_params.final_predictor_list`: Update this list with the names of all the predictor columns (independent variables) from your dataset that you intend to use for modeling.
    - `feature_params.skewed_features`: Update this list with the names of any numerical features from your list that have a skewed distribution.

---

## 4. Running the Pipeline

This section describes how to run the pipeline locally for development and quick smoke tests.

### 3.1. Local Setup

```bash
# Install all required packages
pip install -r requirements.txt

# Install the project in editable mode
pip install -e .
```

### 3.2. Running a Smoke Test

For a quick verification run that uses a minimal set of parameters (e.g., few training epochs), use the `--smoke-test` flag.

```bash
python main.py --smoke-test
```

> **Note on Smoke Test Output:** A successful smoke test will finish without crashing. However, you should expect to see warnings about "mode collapse" and very low performance metrics (e.g., Balanced Accuracy near 0.5). This is normal and expected, as the generative models are not trained for enough epochs to produce meaningful synthetic data. The goal is to verify that the pipeline's components and integrations are working, not to achieve high model performance.

### 3.3. Flexible Stage Execution

You can run specific stages of the pipeline, which is useful for debugging or iterative development.

```bash
# Run ONLY Stage 1 (Data Preparation)
python main.py --stages 1

# Run ONLY a single fold (e.g., fold 4) of Stage 2
python main.py --stages 2 --fold-id 4
```

---

## 4. Full Experimental Run on GCP

For the full, parallelized experimental run, a powerful cloud server is required. A complete, step-by-step guide for setting up the environment and executing the pipeline on a Google Cloud Platform (GCP) VM is available here:

**[GCP Execution Guide](0.READMEs/gcp_execution_guide.md)**

---

## 3.Dataset Requirements

**Important:** Due to patient privacy and data ownership agreements, the `pregsafe_dataset.csv` used in this research is not included in this repository.

To run the pipeline with your own data, you must:

1. **Provide a CSV file:** Your dataset must be in the CSV format.
2. **Update the Configuration:** Open the `config/config.yaml` file and modify the following sections:
    - `data_ingestion.source_path`: Change this to the path of your CSV file.
    - `global_params.target_column`: Change this to the name of the target variable (dependent variable) in your dataset.
    - `feature_params.final_predictor_list`: Update this list with the names of all the predictor columns (independent variables) from your dataset that you intend to use for modeling.
    - `feature_params.skewed_features`: Update this list with the names of any numerical features from your list that have a skewed distribution.

---

## 4.Running the Pipeline

This section describes how to run the pipeline locally for development and quick smoke tests.

## 3.1.Local Setup

```bash
# Install all required packages
pip install -r requirements.txt

# Install the project in editable mode
pip install -e .
```

### 3.2.Running a Smoke Test

For a quick verification run that uses a minimal set of parameters (e.g., few training epochs), use the `--smoke-test` flag.

```bash
python main.py --smoke-test
```

> **Note on Smoke Test Output:** A successful smoke test will finish without crashing. However, you should expect to see warnings about "mode collapse" and very low performance metrics (e.g., Balanced Accuracy near 0.5). This is normal and expected, as the generative models are not trained for enough epochs to produce meaningful synthetic data. The goal is to verify that the pipeline's components and integrations are working, not to achieve high model performance.

### 3.3.Flexible Stage Execution

You can run specific stages of the pipeline, which is useful for debugging or iterative development.

```bash
# Run ONLY Stage 1 (Data Preparation)
python main.py --stages 1

# Run ONLY a single fold (e.g., fold 4) of Stage 2
python main.py --stages 2 --fold-id 4
```

---

## 4.Full Experimental Run on GCP

For the full, parallelized experimental run, a powerful cloud server is required. A complete, step-by-step guide for setting up the environment and executing the pipeline on a Google Cloud Platform (GCP) VM is available here:

**[GCP Execution Guide](gcp_execution_guide.md)**

---

## 5. Pipeline Architecture & Stages

This section provides a comprehensive, stage-by-stage breakdown of the GDM synthetic data generation pipeline.

### Stage 01: Data Preparation

- **Purpose:** Takes the raw dataset and transforms it into clean, structured artifacts.
- **Key Logic:** Loads data, validates, cleans, engineers features, selects features, splits data into development (90%) and holdout (10%) sets, and creates 10 cross-validation folds.
- **Outputs:** `data_for_cv.csv`, `holdout_test_set.csv`, `fold_indices.pkl`.

### Stage 02: Cross-Validation

- **Purpose:** Systematically evaluates the performance of different modeling strategies across the 10 folds.
- **Key Logic:** For each fold, performs TRTR (Train-Real-Test-Real) and TSTR (Train-Synthetic-Test-Real) for both CTGAN and TVAE across all configured ML models.
- **Outputs:** A `fold_X_results.yaml` for each fold, plus detailed artifacts (datasets and synthesizers) in `fold_artifacts/`.

### Stage 03: Results Analysis

- **Purpose:** Aggregates results from all 10 folds to identify champion models.
- **Key Logic:** Parses all fold results, creates an aggregated CSV, generates comparison plots, and identifies two champions: the best performing model for CTGAN data and the best for TVAE data.
- **Outputs:** `aggregated_results.csv`, analysis plots, and `champions.json`.

### Stage 04: Final Evaluation

- **Purpose:** Provides an unbiased, definitive performance report for the two champion strategies.
- **Key Logic:** This stage is run twice. For each champion, it trains the respective synthesizer on the full development set, generates a new synthetic dataset, trains the champion classifier, and evaluates it on the untouched 10% holdout set.
- **Outputs:** Two sets of final artifacts, named by synthesizer (e.g., `final_model_CTGAN.pkl`, `final_evaluation_report_TVAE.json`).

---

## 6. Cleaning the Workspace

To remove all generated files (`outputs/`, `logs/`, etc.), use the `clean` script for your OS.

### For Windows Users

```powershell
./scripts/clean.ps1
```

### For macOS and Linux Users

```bash
./scripts/clean.sh
```
