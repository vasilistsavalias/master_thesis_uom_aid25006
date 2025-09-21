# src/thesis_pipeline/pipeline/stage_07_model_training.py
import logging
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.components.dataset import InpaintingDataset
from thesis_pipeline.components.model_training import ModelTrainer
from thesis_pipeline.utils.common import load_yaml

class ModelTrainingStage:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_training_config()
        self.paths = config_manager.get_data_paths()
        self.dp_config = config_manager.get_data_processing_config()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """Executes the model training stage."""
        self.logger.info("="*20 + " STAGE 07: Model Training " + "="*20)
        
        try:
            # --- Load Hyperparameters ---
            hyperparams_path = Path(self.config.hyperparameters_file)
            hyperparams = load_yaml(hyperparams_path)
            self.logger.info(f"Loaded hyperparameters from: {hyperparams_path}")

            # --- Create Datasets and DataLoaders ---
            dataset_root = Path(self.paths.inpainting_dataset)
            image_size = self.dp_config.image_size
            
            train_dataset = InpaintingDataset(dataset_root, image_size, "train")
            val_dataset = InpaintingDataset(dataset_root, image_size, "validation")

            train_dataloader = DataLoader(
                train_dataset,
                batch_size=self.config.train_batch_size,
                shuffle=True
            )
            val_dataloader = DataLoader(
                val_dataset,
                batch_size=self.config.train_batch_size,
                shuffle=False
            )
            self.logger.info("Datasets and DataLoaders created.")

            # --- Initialize and Run Trainer ---
            trainer = ModelTrainer(config=self.config, hyperparams=hyperparams)
            final_unet = trainer.train(train_dataloader, val_dataloader)

            # --- Save Final Model ---
            if final_unet:
                final_model_path = Path(self.config.output_dir) / "unet_final"
                final_unet.save_pretrained(final_model_path)
                self.logger.info(f"Final UNet model saved to: {final_model_path}")
            else:
                self.logger.error("Training did not return a model. Final model not saved.")

            self.logger.info("="*20 + " STAGE 07 COMPLETED " + "="*20 + "\n")

        except Exception as e:
            self.logger.exception(f"An error occurred during the Model Training stage: {e}")
            raise

if __name__ == '__main__':
    # Guard for multiprocessing on Windows
    torch.multiprocessing.freeze_support()
    try:
        config_manager = ConfigManager()
        stage = ModelTrainingStage(config_manager)
        stage.run()
    except Exception as e:
        logging.exception("Exception in Model Training Stage execution")
        raise
