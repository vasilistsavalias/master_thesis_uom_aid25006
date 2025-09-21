# Ancient Greek Artifact Restoration Pipeline (V2 Architecture)

## 1. Project Synopsis

This repository contains a complete, end-to-end deep learning pipeline for fine-tuning a Stable Diffusion model on an inpainting task, specifically for the restoration of ancient Greek artifacts. The project is a rigorous, one-to-one conversion of a stage-based research project into a robust, modular architecture inspired by professional MLOps practices.

The entire workflow is managed by a single orchestrator and is configurable via centralized YAML files, emphasizing reproducibility, scalability, and a clean separation of concerns.

## 2. Core Architectural Principles

- **Sequential & Modular:** The project is a strict, 9-stage pipeline. Each stage is an independent, class-based component that can be run on its own, provided the previous stage's outputs are present.
- **Centralized Configuration:** All parameters, paths, and settings are managed in `config/main_config.yaml` for full runs and `config/smoke_test_config.yaml` for fast, MVP test runs.
- **Reproducibility:** By using a dedicated setup script (`setup_and_run.ps1` or `.sh`), the project guarantees a consistent environment and execution process.
- **Separation of Concerns:** Source code (`src/`), generated artifacts (`outputs/`), logs (`logs/`), and configuration (`config/`) are kept in separate, top-level directories.

For a detailed, file-by-file breakdown of the codebase, please see the **[Pipeline Documentation](0.READMEs/pipeline.md)**.

---

## 3. How to Run the Pipeline

This project includes automated scripts to handle setup and execution for both Windows and Linux-based systems.

### 3.1. Running the Full End-to-End MVP (Smoke Test)

This is the recommended way to verify the entire pipeline is working. It uses minimal parameters for a quick run.

**For Windows (PowerShell):**

```powershell
.\scripts\setup_and_run.ps1 --smoke-test
```

**For macOS/Linux (Bash):**

```bash
bash scripts/setup_and_run.sh --smoke-test
```

This single command will:

1. Create a local Python virtual environment (`.venv/`).
2. Install all dependencies from `requirements.txt`.
3. Install the project's source code as a package.
4. Run the entire 9-stage pipeline using the `smoke_test_config.yaml`.

### 3.2. Running Specific Stages

You can run any individual stage or sequence of stages for development or debugging.

```powershell
# Example: Run only Stage 3 (Data Processing) and Stage 4 (Data Splitting)
.\scripts\setup_and_run.ps1 --stages 3 4
```

---

## 4. Full Experimental Run on GCP

For a full run with production-level parameters (e.g., full dataset, many epochs), a powerful cloud server with a GPU is required. A complete, step-by-step guide is available here:

**[GCP Execution Guide](0.READMEs/gcp_execution_guide.md)**
