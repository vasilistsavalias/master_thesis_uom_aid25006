# main.py
import argparse
import logging
from thesis_pipeline.config_manager import ConfigManager
from thesis_pipeline.logging_config import LoggingConfig
from thesis_pipeline.pipeline.stage_01_data_acquisition import DataAcquisitionStage
from thesis_pipeline.pipeline.stage_02_exploratory_data_analysis import ExploratoryDataAnalysisStage
from thesis_pipeline.pipeline.stage_03_data_processing import DataProcessingStage
from thesis_pipeline.pipeline.stage_04_data_splitting import DataSplittingStage
from thesis_pipeline.pipeline.stage_05_feature_engineering import FeatureEngineeringStage
from thesis_pipeline.pipeline.stage_06_hyperparameter_tuning import HyperparameterTuningStage
from thesis_pipeline.pipeline.stage_07_model_training import ModelTrainingStage
from thesis_pipeline.pipeline.stage_08_model_evaluation import ModelEvaluationStage
from thesis_pipeline.pipeline.stage_09_deployment_preparation import DeploymentPreparationStage

# ==============================================================================
# Main Pipeline Orchestrator
# ==============================================================================

def main(stages_to_run=None, smoke_test=False):
    """
    The main entry point for the thesis pipeline.
    """
    # --- 1. Initial Setup ---
    try:
        if smoke_test:
            config_path = Path("config/smoke_test_config.yaml")
        else:
            config_path = Path("config/main_config.yaml")
            
        config_manager = ConfigManager(config_filepath=config_path)
        logging_config = LoggingConfig(config_manager)
        logging_config.setup_logging()
        
        logger = logging.getLogger(__name__)
        logger.info("="*40)
        if smoke_test:
            logger.info(" Thesis Pipeline Started (SMOKE TEST) ".center(40, "="))
        else:
            logger.info(" Thesis Pipeline Started ".center(40, "="))
        logger.info("="*40)
        
    except Exception as e:
        # If setup fails, log and exit
        logging.basicConfig(level=logging.INFO) # Basic config for this message
        logging.error(f"FATAL: Pipeline setup failed: {e}", exc_info=True)
        return

    # --- 2. Define All Stages ---
    all_stages = {
        "1": DataAcquisitionStage,
        "2": ExploratoryDataAnalysisStage,
        "3": DataProcessingStage,
        "4": DataSplittingStage,
        "5": FeatureEngineeringStage,
        "6": HyperparameterTuningStage,
        "7": ModelTrainingStage,
        "8": ModelEvaluationStage,
        "9": DeploymentPreparationStage,
    }

    # --- 3. Determine Which Stages to Run ---
    if stages_to_run:
        stages = stages_to_run
    else:
        # If no stages are specified via CLI, run all defined stages
        stages = list(all_stages.keys())

    logger.info(f"Pipeline will execute the following stages: {', '.join(stages)}")

    # --- 4. Execute Pipeline Stages ---
    for stage_num in stages:
        if stage_num in all_stages:
            StageClass = all_stages[stage_num]
            try:
                stage_instance = StageClass(config_manager)
                stage_instance.run()
            except Exception as e:
                logger.error(f"FATAL: An error occurred in Stage {stage_num}.", exc_info=True)
                logger.info("="*40)
                logger.info(" Pipeline Terminated Due to Error ".center(40, "="))
                logger.info("="*40)
                return # Stop the pipeline on failure
        else:
            logger.warning(f"Stage '{stage_num}' is not defined. Skipping.")

    logger.info("="*40)
    logger.info(" Thesis Pipeline Completed Successfully ".center(40, "="))
    logger.info("="*40)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Main orchestrator for the thesis pipeline.")
    parser.add_argument(
        "--stages",
        nargs='+',
        help="Specify which stage(s) to run (e.g., --stages 1 2). If not provided, all stages will run."
    )
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Run the pipeline in smoke test mode using minimal configuration."
    )
    
    args = parser.parse_args()
    
    main(stages_to_run=args.stages, smoke_test=args.smoke_test)
