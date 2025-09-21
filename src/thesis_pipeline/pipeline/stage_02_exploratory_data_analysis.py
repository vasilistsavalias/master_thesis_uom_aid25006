# src/thesis_pipeline/pipeline/stage_02_exploratory_data_analysis.py
import logging
from pathlib import Path
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.components.exploratory_data_analysis import ExploratoryDataAnalyzer

class ExploratoryDataAnalysisStage:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_exploratory_data_analysis_config()
        self.paths = config_manager.get_data_paths()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Executes the exploratory data analysis stage.
        """
        self.logger.info("="*20 + " STAGE 02: Exploratory Data Analysis " + "="*20)
        
        try:
            input_dir = Path(self.paths.raw_images)
            output_dir = Path(self.config.output_dir)
            
            self.logger.info(f"Input directory for EDA: {input_dir}")
            self.logger.info(f"Output directory for reports: {output_dir}")

            analyzer = ExploratoryDataAnalyzer(
                input_dir=input_dir,
                output_dir=output_dir,
                extensions=self.config.image_extensions
            )
            
            analyzer.run()
            
            self.logger.info("EDA process completed.")
            self.logger.info("="*20 + " STAGE 02 COMPLETED " + "="*20 + "\n")

        except Exception as e:
            self.logger.exception(f"An error occurred during the EDA stage: {e}")
            raise

if __name__ == '__main__':
    try:
        config_manager = ConfigManager()
        stage = ExploratoryDataAnalysisStage(config_manager)
        stage.run()
    except Exception as e:
        logging.exception("Exception in EDA Stage execution")
        raise