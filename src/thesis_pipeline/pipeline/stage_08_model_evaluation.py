# src/thesis_pipeline/pipeline/stage_08_model_evaluation.py
import logging
from pathlib import Path
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.components.model_evaluation import ModelEvaluator

class ModelEvaluationStage:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_model_evaluation_config()
        self.paths = config_manager.get_data_paths()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """Executes the model evaluation stage."""
        self.logger.info("="*20 + " STAGE 08: Model Evaluation " + "="*20)
        
        try:
            test_data_dir = Path(self.paths.inpainting_dataset) / "test"
            
            evaluator = ModelEvaluator(
                config=self.config,
                test_data_dir=test_data_dir
            )
            
            evaluator.evaluate()
            
            self.logger.info("="*20 + " STAGE 08 COMPLETED " + "="*20 + "\n")

        except Exception as e:
            self.logger.exception(f"An error occurred during the Model Evaluation stage: {e}")
            raise

if __name__ == '__main__':
    try:
        config_manager = ConfigManager()
        stage = ModelEvaluationStage(config_manager)
        stage.run()
    except Exception as e:
        logging.exception("Exception in Model Evaluation Stage execution")
        raise
