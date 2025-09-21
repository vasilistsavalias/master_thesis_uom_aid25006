# src/thesis_pipeline/pipeline/stage_03_feature_engineering.py
import logging
from pathlib import Path
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.components.masking import MaskingStrategy

class FeatureEngineeringStage:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_feature_engineering_config()
        self.paths = config_manager.get_data_paths()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Executes the feature engineering (masking) stage.
        """
        self.logger.info("="*20 + " STAGE 05: Feature Engineering (Masking) " + "="*20)
        
        try:
            # The input is the root directory of the splits (train/val/test)
            input_dir = Path(self.paths.split_data)
            output_dir = Path(self.paths.inpainting_dataset)
            
            self.logger.info(f"Input directory for masking: {input_dir}")
            self.logger.info(f"Output directory for inpainting dataset: {output_dir}")
            
            output_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Ensured output directory exists: {output_dir}")

            # Initialize the masking strategy
            masking_strategy = MaskingStrategy(
                strategy_name=self.config.mask_strategy,
                mask_config=self.config.mask_config.to_dict() # Convert ConfigBox to dict
            )
            
            self.logger.info(f"Masking strategy '{self.config.mask_strategy}' initialized.")
            
            # Process each split (train, validation, test)
            for split in ["train", "validation", "test"]:
                self.logger.info(f"--- Processing '{split}' split ---")
                split_input_dir = input_dir / split
                split_output_dir = output_dir / split
                split_output_dir.mkdir(parents=True, exist_ok=True)
                
                if not split_input_dir.exists():
                    self.logger.warning(f"Input directory for split '{split}' does not exist: {split_input_dir}")
                    continue

                masking_strategy.create_inpainting_dataset(
                    image_dir=split_input_dir,
                    output_dir=split_output_dir
                )
                self.logger.info(f"Finished processing '{split}' split.")

            self.logger.info("Successfully created inpainting datasets for all splits.")
            self.logger.info("="*20 + " STAGE 03 COMPLETED " + "="*20 + "\n")

        except Exception as e:
            self.logger.exception(f"An error occurred during the Feature Engineering stage: {e}")
            raise

if __name__ == '__main__':
    try:
        # This is for testing the stage independently
        config_manager = ConfigManager()
        stage = FeatureEngineeringStage(config_manager)
        stage.run()
    except Exception as e:
        logging.exception("Exception in Feature Engineering Stage execution")
        raise
