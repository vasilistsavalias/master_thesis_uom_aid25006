# src/thesis_pipeline/logging_config.py
import sys
import logging
from loguru import logger
from pathlib import Path
from thesis_pipeline.config_manager import ConfigManager

class LoggingConfig:
    """
    Centralized logging configuration for the entire pipeline.
    """

    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager.get_logging_config()
        self.log_dir = Path(self.config.log_dir)
        self.log_file = self.log_dir / self.config.main_log_file
        self.log_level = self.config.log_level.upper()

    def setup_logging(self):
        """
        Configures the loguru logger to be used throughout the application.
        """
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Remove default handler to avoid duplicate messages in console
        logger.remove()

        # Add a handler for console output
        logger.add(
            sys.stdout,
            level=self.log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )

        # Add a handler for file output with rotation
        logger.add(
            self.log_file,
            level=self.log_level,
            rotation="10 MB",  # Rotates the log file when it reaches 10 MB
            retention="7 days", # Keeps logs for 7 days
            enqueue=True,      # Makes logging thread-safe
            backtrace=True,    # Shows full stack trace on exceptions
            diagnose=True,     # Adds exception variable values
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        )

        # Intercept standard logging messages
        class InterceptHandler(logging.Handler):
            def emit(self, record):
                # Get corresponding Loguru level if it exists
                try:
                    level = logger.level(record.levelname).name
                except ValueError:
                    level = record.levelno

                # Find caller from where originated the logged message
                frame, depth = logging.currentframe(), 2
                while frame.f_code.co_filename == logging.__file__:
                    frame = frame.f_back
                    depth += 1

                logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
        
        initial_logger = logging.getLogger(__name__)
        initial_logger.info("Logging configured successfully. All logs will be sent to console and file.")

if __name__ == '__main__':
    # This is for testing the logging setup independently
    try:
        config_manager = ConfigManager()
        logging_config = LoggingConfig(config_manager)
        logging_config.setup_logging()
        
        test_logger = logging.getLogger(__name__)
        test_logger.info("This is an info message.")
        test_logger.warning("This is a warning message.")
        test_logger.error("This is an error message.")
        
        def test_function():
            try:
                1 / 0
            except ZeroDivisionError:
                test_logger.exception("Caught a ZeroDivisionError.")
        
        test_function()
        
    except Exception as e:
        print(f"An error occurred during logging setup test: {e}")
        raise
