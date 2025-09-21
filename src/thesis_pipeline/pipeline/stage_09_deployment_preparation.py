# src/thesis_pipeline/pipeline/stage_09_deployment_preparation.py
import logging
from pathlib import Path
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.components.deployment_preparation import DeploymentPackager

class DeploymentPreparationStage:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_deployment_preparation_config()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """Executes the deployment preparation stage."""
        self.logger.info("="*20 + " STAGE 09: Deployment Preparation " + "="*20)
        
        try:
            model_input_dir = Path(self.config.model_input_dir)
            hyperparams_input_file = Path(self.config.hyperparams_input_file)
            
            packager = DeploymentPackager(
                config=self.config,
                model_input_dir=model_input_dir,
                hyperparams_input_file=hyperparams_input_file
            )
            
            packager.package()
            
            self.logger.info("="*20 + " STAGE 09 COMPLETED " + "="*20 + "\n")

        except Exception as e:
            self.logger.exception(f"An error occurred during the Deployment Preparation stage: {e}")
            raise

if __name__ == '__main__':
    try:
        config_manager = ConfigManager()
        stage = DeploymentPreparationStage(config_manager)
        stage.run()
    except Exception as e:
        logging.exception("Exception in Deployment Preparation Stage execution")
        raise
