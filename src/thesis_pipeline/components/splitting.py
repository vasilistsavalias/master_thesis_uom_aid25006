# src/thesis_pipeline/components/splitting.py
import logging
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
from tqdm import tqdm

class DataSplitter:
    """
    Encapsulates the logic for splitting data into train, validation, and test sets.
    """
    def __init__(self, input_dir: Path, output_dir: Path, test_size: float, validation_size: float, random_state: int):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.test_size = test_size
        self.validation_size = validation_size
        self.random_state = random_state
        self.logger = logging.getLogger(__name__)

    def _find_all_files(self) -> list:
        """Finds all files in the input directory."""
        files = [p for p in self.input_dir.glob('*') if p.is_file()]
        self.logger.info(f"Found {len(files)} files in {self.input_dir}.")
        return files

    def _copy_files(self, files: list, destination_dir: Path):
        """Copies a list of files to a destination directory."""
        destination_dir.mkdir(parents=True, exist_ok=True)
        for f in tqdm(files, desc=f"Copying to {destination_dir.name}"):
            try:
                shutil.copy(f, destination_dir / f.name)
            except Exception as e:
                self.logger.error(f"Could not copy file {f}. Error: {e}")

    def split_data(self):
        """
        Splits image files into train, validation, and test sets and copies them.
        """
        all_files = self._find_all_files()
        
        if not all_files:
            self.logger.warning("No files found in the input directory. Nothing to split.")
            return

        self.logger.info(f"Splitting data with test_size={self.test_size}.")
        train_val_files, test_files = train_test_split(
            all_files,
            test_size=self.test_size,
            random_state=self.random_state
        )

        val_size_adjusted = self.validation_size / (1.0 - self.test_size)
        self.logger.info(f"Splitting remaining data with validation_size={val_size_adjusted:.2f} (relative).")
        train_files, val_files = train_test_split(
            train_val_files,
            test_size=val_size_adjusted,
            random_state=self.random_state
        )

        self.logger.info("Splitting complete. Summary:")
        self.logger.info(f" - Training set size:   {len(train_files)}")
        self.logger.info(f" - Validation set size: {len(val_files)}")
        self.logger.info(f" - Test set size:       {len(test_files)}")

        train_dir = self.output_dir / 'train'
        val_dir = self.output_dir / 'validation' # Corrected from 'val' to 'validation' for clarity
        test_dir = self.output_dir / 'test'

        self.logger.info("Copying files to their respective split directories...")
        self._copy_files(train_files, train_dir)
        self._copy_files(val_files, val_dir)
        self._copy_files(test_files, test_dir)

        self.logger.info("File copying complete. Data splitting stage is finished.")
