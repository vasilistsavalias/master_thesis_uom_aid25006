# src/thesis_pipeline/pipeline/stage_01_data_processing.py
import logging
from pathlib import Path
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.components.processing import ImageProcessor
from thesis_pipeline.utils.common import save_json

class DataProcessingStage:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_data_processing_config()
        self.paths = config_manager.get_data_paths()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Executes the data processing stage.
        """
        self.logger.info("="*20 + " STAGE 03: Data Processing " + "="*20)
        
        try:
            input_dir = Path(self.paths.raw_images)
            output_dir = Path(self.paths.processed_images)
            
            self.logger.info(f"Input directory: {input_dir}")
            self.logger.info(f"Output directory: {output_dir}")
            
            output_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Ensured output directory exists: {output_dir}")

            processor = ImageProcessor(
                input_dir=input_dir,
                output_dir=output_dir,
                image_size=tuple(self.config.image_size),
                output_format=self.config.format
            )
            
            self.logger.info("ImageProcessor initialized. Starting processing...")
            summary = processor.process_images()
            
            # Save the summary to the processed images directory
            summary_path = output_dir / "processing_summary.json"
            save_json(summary_path, summary)
            
            self.logger.info(f"Successfully processed {summary['processed_count']} images.")
            self.logger.info(f"Encountered {summary['error_count']} errors.")
            self.logger.info(f"Summary saved to: {summary_path}")
            self.logger.info("="*20 + " STAGE 01 COMPLETED " + "="*20 + "\n")

        except Exception as e:
            self.logger.exception(f"An error occurred during the Data Processing stage: {e}")
            raise

if __name__ == '__main__':
    try:
        # This is for testing the stage independently
        config_manager = ConfigManager()
        stage = DataProcessingStage(config_manager)
        stage.run()
    except Exception as e:
        logging.exception("Exception in Data Processing Stage execution")
        raise
