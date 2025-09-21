# src/thesis_pipeline/pipeline/stage_06_hyperparameter_tuning.py
import logging
from pathlib import Path
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.utils.common import save_yaml

class HyperparameterTuningStage:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_hyperparameter_tuning_config()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Executes the hyperparameter tuning stage.
        For the smoke test, this stage writes a dummy file with predefined values.
        """
        self.logger.info("="*20 + " STAGE 06: Hyperparameter Tuning (Dummy) " + "="*20)
        
        try:
            output_file = Path(self.config.output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # In a real run, this would come from a tuning library like Optuna.
            # For the MVP, we use the dummy values from the config.
            dummy_hyperparams = self.config.dummy_hyperparameters.to_dict()
            
            save_yaml(output_file, dummy_hyperparams)
            
            self.logger.info(f"Dummy hyperparameters saved to: {output_file}")
            self.logger.info("This stage was a dummy run for MVP purposes.")
            self.logger.info("="*20 + " STAGE 06 COMPLETED " + "="*20 + "\n")

        except Exception as e:
            self.logger.exception(f"An error occurred during the Hyperparameter Tuning stage: {e}")
            raise
