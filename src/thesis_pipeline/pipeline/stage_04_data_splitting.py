# src/thesis_pipeline/pipeline/stage_02_data_splitting.py
import logging
from pathlib import Path
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.components.splitting import DataSplitter

class DataSplittingStage:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_data_splitting_config()
        self.paths = config_manager.get_data_paths()
        self.global_params = config_manager.get_global_params()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Executes the data splitting stage.
        """
        self.logger.info("="*20 + " STAGE 04: Data Splitting " + "="*20)
        
        try:
            input_dir = Path(self.paths.processed_images)
            output_dir = Path(self.paths.split_data)
            
            self.logger.info(f"Input directory for splitting: {input_dir}")
            self.logger.info(f"Output directory for splits: {output_dir}")
            
            output_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Ensured output directory exists: {output_dir}")

            splitter = DataSplitter(
                input_dir=input_dir,
                output_dir=output_dir,
                test_size=self.config.test_size,
                validation_size=self.config.validation_size,
                random_state=self.global_params.random_state
            )
            
            self.logger.info("DataSplitter initialized. Starting splitting...")
            splitter.split_data()
            
            self.logger.info("Successfully split data into train, validation, and test sets.")
            self.logger.info("="*20 + " STAGE 02 COMPLETED " + "="*20 + "\n")

        except Exception as e:
            self.logger.exception(f"An error occurred during the Data Splitting stage: {e}")
            raise

if __name__ == '__main__':
    try:
        # This is for testing the stage independently
        config_manager = ConfigManager()
        stage = DataSplittingStage(config_manager)
        stage.run()
    except Exception as e:
        logging.exception("Exception in Data Splitting Stage execution")
        raise
