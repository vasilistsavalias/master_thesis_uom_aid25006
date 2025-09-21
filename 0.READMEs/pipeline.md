# Thesis Pipeline Codebase Documentation

This document provides a detailed, downstream explanation of every Python module in the `src/thesis_pipeline/` directory, outlining its purpose, inputs, and outputs in the logical order of execution.

---

## 1. Orchestration & Core Utilities

These modules provide the entry point, configuration, and common utilities used throughout the pipeline.

### `main.py`

- **Purpose:** The main entry point for the entire application. It provides a command-line interface to run the full pipeline, a smoke test, or specific individual stages.
- **Inputs:** Command-line arguments (`--stages`, `--smoke-test`).
- **Outputs:** Orchestrates all other modules to produce file outputs and logs.

### `src/thesis_pipeline/config_manager.py`

- **Purpose:** Serves as a single source of truth for all configuration parameters by reading and parsing the project's `.yaml` config files.
- **Inputs:** `config_filepath` (Path to a `.yaml` file).
- **Outputs:** Provides configuration `ConfigBox` objects to all other parts of the pipeline.

### `src/thesis_pipeline/logging_config.py`

- **Purpose:** Centralizes and standardizes the `loguru`-based logging configuration for the entire pipeline.
- **Inputs:** A `ConfigManager` instance.
- **Outputs:** A configured `loguru` logger instance.

### `src/thesis_pipeline/utils/common.py`

- **Purpose:** Abstracts and centralizes all common file input/output operations (JSON, YAML, binary).
- **Inputs:** File paths and data objects.
- **Outputs:** Data objects read from disk or `None` for save operations.

---

## 2. Pipeline Stages

### Stage 01: Data Acquisition

- **`pipeline/stage_01_data_acquisition.py`**: Orchestrates the data acquisition process.
- **`components/data_acquisition.py`**: Contains the `DataAcquisition` class, which handles the logic for recursively querying the Wikimedia API, finding all image URLs in a given category tree, and downloading them.
- **Inputs**: `start_category`, `download_limit` from config.
- **Outputs**: Raw image files saved to `data/01_raw/`.

### Stage 02: Exploratory Data Analysis

- **`pipeline/stage_02_exploratory_data_analysis.py`**: Orchestrates the EDA process.
- **`components/exploratory_data_analysis.py`**: Contains the `ExploratoryDataAnalyzer` class, which analyzes image metadata (dimensions, mode, filesize) and generates summary statistics and visualizations.
- **Inputs**: Raw images from `data/01_raw/`.
- **Outputs**: A CSV file with image metadata and `.png` plots saved to the `outputs/` directory.

### Stage 03: Data Processing

- **`pipeline/stage_03_data_processing.py`**: Orchestrates the image processing.
- **`components/processing.py`**: Contains the `ImageProcessor` class, which resizes images to a standard dimension and converts them to a standard format (e.g., PNG).
- **Inputs**: Raw images from `data/01_raw/`.
- **Outputs**: Processed images saved to the `outputs/` directory.

### Stage 04: Data Splitting

- **`pipeline/stage_04_data_splitting.py`**: Orchestrates the data splitting.
- **`components/splitting.py`**: Contains the `DataSplitter` class, which splits the processed images into `train`, `validation`, and `test` sets based on configured ratios.
- **Inputs**: Processed images.
- **Outputs**: `train/`, `validation/`, and `test/` subdirectories populated with images in the `outputs/` directory.

### Stage 05: Feature Engineering (Masking)

- **`pipeline/stage_05_feature_engineering.py`**: Orchestrates the mask generation.
- **`components/masking.py`**: Contains the `MaskingStrategy` class, which generates a random mask for each image in the train, validation, and test sets, creating the ground truth and mask pairs required for inpainting.
- **Inputs**: Split datasets.
- **Outputs**: `ground_truth/` and `masks/` subdirectories for each data split.

### Stage 06: Hyperparameter Tuning

- **`pipeline/stage_06_hyperparameter_tuning.py`**: Orchestrates hyperparameter selection. For the MVP, this stage is a placeholder.
- **Logic**: Writes a dummy `best_hyperparameters.yaml` file with predefined values to allow the pipeline to proceed without a lengthy tuning process.
- **Inputs**: None.
- **Outputs**: `best_hyperparameters.yaml`.

### Stage 07: Model Training

- **`pipeline/stage_07_model_training.py`**: Orchestrates the model training process.
- **`components/dataset.py`**: Contains the `InpaintingDataset` PyTorch class for loading image-mask pairs.
- **`components/model_training.py`**: Contains the `ModelTrainer` class, which handles the core training loop, including loading pretrained models from Hugging Face, setting up the optimizer, and running the training and validation steps using `accelerate`.
- **Inputs**: Inpainting datasets, `best_hyperparameters.yaml`.
- **Outputs**: Trained UNet model checkpoints saved to the `outputs/` directory.

### Stage 08: Model Evaluation

- **`pipeline/stage_08_model_evaluation.py`**: Orchestrates the model evaluation.
- **`components/model_evaluation.py`**: Contains the `ModelEvaluator` class, which loads the fine-tuned UNet, runs inference on the test set, calculates metrics (PSNR, SSIM), and saves visual comparisons.
- **Inputs**: The trained UNet model and the test set.
- **Outputs**: A CSV of metrics, a summary `.txt` report, and comparison images.

### Stage 09: Deployment Preparation

- **`pipeline/stage_09_deployment_preparation.py`**: Orchestrates the packaging of the final model.
- **`components/deployment_preparation.py`**: Contains the `DeploymentPackager` class, which copies the final trained UNet, the hyperparameters file, and a README into a clean `deployment_package/` directory.
- **Inputs**: The final UNet model and hyperparameters file.
- **Outputs**: A self-contained deployment package folder.