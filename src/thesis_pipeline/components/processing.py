# src/thesis_pipeline/components/processing.py
import logging
from pathlib import Path
from PIL import Image
from tqdm import tqdm

class ImageProcessor:
    """
    Encapsulates the logic for processing raw images.
    """
    def __init__(self, input_dir: Path, output_dir: Path, image_size: tuple, output_format: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.target_size = image_size
        self.output_format = output_format
        self.logger = logging.getLogger(__name__)

    def _find_image_files(self) -> list:
        """Finds all image files in the input directory."""
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        image_files = []
        for ext in extensions:
            image_files.extend(self.input_dir.glob(f'*{ext}'))
        self.logger.info(f"Found {len(image_files)} image files in {self.input_dir}.")
        return image_files

    def process_images(self) -> dict:
        """
        Processes raw images by resizing, converting to RGB, and saving them.
        Returns a summary of the operation.
        """
        image_files = self._find_image_files()
        
        if not image_files:
            self.logger.warning("No images found in the input directory. Nothing to process.")
            return {"processed_count": 0, "error_count": 0, "total_found": 0}

        self.logger.info(f"Processing {len(image_files)} images. Target size: {self.target_size}, Format: {self.output_format}")
        
        processed_count = 0
        error_count = 0

        for img_path in tqdm(image_files, desc="Processing Images"):
            try:
                with Image.open(img_path) as img:
                    img_rgb = img.convert('RGB')
                    img_resized = img_rgb.resize(self.target_size, Image.Resampling.LANCZOS)
                    
                    output_filename = f"{img_path.stem}.{self.output_format.lower()}"
                    output_path = self.output_dir / output_filename
                    
                    img_resized.save(output_path, format=self.output_format)
                    processed_count += 1

            except Exception as e:
                self.logger.error(f"Failed to process {img_path}. Error: {e}")
                error_count += 1
        
        summary = {
            "processed_count": processed_count,
            "error_count": error_count,
            "total_found": len(image_files)
        }
        self.logger.info(f"Image processing complete. Summary: {summary}")
        return summary

