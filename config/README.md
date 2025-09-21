# Configuration

This directory serves as the project's central control panel. All configurable parameters should be stored here to avoid hardcoding values within the source code.

## Files
- `main_config.yaml`: The single source of truth for all project parameters. This includes file paths, dataset parameters, API keys (if any, handled via environment variables), and model hyperparameters.
- `logging_config.py`: A Python script to configure the `loguru` logger in a consistent way across all stages of the project. It can be imported by the `main.py` of each stage.
