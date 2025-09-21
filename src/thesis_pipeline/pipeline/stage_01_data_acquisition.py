# src/thesis_pipeline/pipeline/stage_01_data_acquisition.py
import logging
from pathlib import Path
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.components.data_acquisition import DataAcquisition

class DataAcquisitionStage:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_data_acquisition_config()
        self.paths = config_manager.get_data_paths()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Executes the data acquisition stage.
        """
        self.logger.info("="*20 + " STAGE 01: Data Acquisition " + "="*20)
        
        try:
            output_dir = Path(self.paths.raw_images)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Output directory set to: {output_dir}")

            acquirer = DataAcquisition(api_url=self.config.wikimedia_api_url)
            
            acquirer.download_images_from_category(
                start_category=self.config.start_category,
                output_dir=output_dir,
                limit=self.config.download_limit
            )
            
            self.logger.info("Data acquisition process completed.")
            self.logger.info("="*20 + " STAGE 01 COMPLETED " + "="*20 + "\n")

        except Exception as e:
            self.logger.exception(f"An error occurred during the Data Acquisition stage: {e}")
            raise

if __name__ == '__main__':
    try:
        # This is for testing the stage independently
        config_manager = ConfigManager()
        stage = DataAcquisitionStage(config_manager)
        stage.run()
    except Exception as e:
        logging.exception("Exception in Data Acquisition Stage execution")
        raise