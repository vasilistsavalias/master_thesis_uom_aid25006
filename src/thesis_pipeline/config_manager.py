# src/thesis_pipeline/config_manager.py
import yaml
from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError
import logging

class ConfigManager:
    """
    Manages the loading and access of configuration parameters from a YAML file.
    """
    def __init__(self, config_filepath: Path = Path("config/main_config.yaml")):
        self.config_filepath = config_filepath
        self.config = self._load_config()
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Configuration loaded successfully from: {self.config_filepath}")

    def _load_config(self) -> ConfigBox:
        """
        Loads the YAML configuration file and returns it as a ConfigBox object.
        """
        try:
            with open(self.config_filepath, "r") as f:
                config = yaml.safe_load(f)
            return ConfigBox(config)
        except FileNotFoundError:
            logging.error(f"Configuration file not found at: {self.config_filepath}")
            raise
        except (yaml.YAMLError, BoxValueError) as e:
            logging.error(f"Error parsing the configuration file: {e}")
            raise

    def get_global_params(self) -> ConfigBox:
        return self.config.global_params

    def get_data_paths(self) -> ConfigBox:
        return self.config.data_paths

    def get_logging_config(self) -> ConfigBox:
        return self.config.logging

    def get_data_processing_config(self) -> ConfigBox:
        return self.config.data_processing

    def get_data_splitting_config(self) -> ConfigBox:
        return self.config.data_splitting

    def get_feature_engineering_config(self) -> ConfigBox:
        return self.config.feature_engineering
        
    def get_data_acquisition_config(self) -> ConfigBox:
        return self.config.data_acquisition

    def get_exploratory_data_analysis_config(self) -> ConfigBox:
        return self.config.exploratory_data_analysis

    # Add getters for other stages as they are migrated
    def get_hyperparameter_tuning_config(self) -> ConfigBox:
        return self.config.hyperparameter_tuning

    def get_training_config(self) -> ConfigBox:
        return self.config.training

    def get_model_evaluation_config(self) -> ConfigBox:
        return self.config.model_evaluation

    def get_deployment_preparation_config(self) -> ConfigBox:
        return self.config.deployment_preparation

if __name__ == '__main__':
    # This is for testing the ConfigManager independently
    try:
        config_manager = ConfigManager()
        
        # Test accessing various config sections
        global_params = config_manager.get_global_params()
        print(f"Project Name: {global_params.project_name}")
        
        paths = config_manager.get_data_paths()
        print(f"Raw Images Path: {paths.raw_images}")
        
        dp_config = config_manager.get_data_processing_config()
        print(f"Image Size: {dp_config.image_size}")
        
        print("ConfigManager test successful.")
        
    except Exception as e:
        print(f"An error occurred during ConfigManager test: {e}")
        raise
