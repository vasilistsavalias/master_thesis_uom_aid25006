# src/thesis_pipeline/components/deployment_preparation.py
import logging
import shutil
from pathlib import Path

class DeploymentPackager:
    def __init__(self, config, model_input_dir: Path, hyperparams_input_file: Path):
        self.config = config
        self.model_input_dir = model_input_dir
        self.hyperparams_input_file = hyperparams_input_file
        self.output_dir = Path(config.output_dir)
        self.logger = logging.getLogger(__name__)

    def package(self):
        """Packages the model and necessary files for deployment."""
        if self.output_dir.exists():
            self.logger.warning(f"Output directory {self.output_dir} exists. Cleaning it.")
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
        self.logger.info(f"Created deployment package directory at: {self.output_dir}")

        # Copy UNet model
        unet_dest_dir = self.output_dir / 'unet_final'
        shutil.copytree(self.model_input_dir, unet_dest_dir)
        self.logger.info(f"Copied UNet to: {unet_dest_dir}")

        # Copy hyperparameters
        shutil.copy(self.hyperparams_input_file, self.output_dir)
        self.logger.info(f"Copied hyperparameters to: {self.output_dir}")

        # Create README
        readme_content = f"""
# Inpainting Model Deployment Package
- `/unet_final`: The fine-tuned UNet model weights.
- `{self.hyperparams_input_file.name}`: The hyperparameters.
"""
        with open(self.output_dir / "README.md", 'w') as f:
            f.write(readme_content)
        self.logger.info("Created README.md for the package.")
