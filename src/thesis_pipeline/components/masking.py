# src/thesis_pipeline/components/masking.py
import logging
import shutil
import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm
import random

class MaskingStrategy:
    """
    Encapsulates strategies for generating image masks and creating inpainting datasets.
    """
    def __init__(self, strategy_name: str, mask_config: dict):
        self.mask_config = mask_config
        self.logger = logging.getLogger(__name__)
        
        if strategy_name == "random_rectangle":
            self.mask_generator = self._generate_random_rectangle_mask
        else:
            self.logger.error(f"Unknown masking strategy: {strategy_name}")
            raise ValueError(f"Unknown masking strategy: {strategy_name}")

    def _generate_random_rectangle_mask(self, height: int, width: int) -> np.ndarray:
        """Generates a mask with a single random rectangle."""
        mask = np.zeros((height, width), dtype=np.uint8)
        min_ratio = self.mask_config['min_mask_size_ratio']
        max_ratio = self.mask_config['max_mask_size_ratio']

        mask_height = random.randint(int(min_ratio * height), int(max_ratio * height))
        mask_width = random.randint(int(min_ratio * width), int(max_ratio * width))

        top = random.randint(0, height - mask_height)
        left = random.randint(0, width - mask_width)

        mask[top:top + mask_height, left:left + mask_width] = 255
        return mask

    def create_inpainting_dataset(self, image_dir: Path, output_dir: Path):
        """
        Creates a dataset for inpainting by generating masks for a set of images.
        Original images are copied to a 'ground_truth' sub-directory and masks
        are saved in a 'masks' sub-directory.
        """
        image_files = [p for p in image_dir.glob('*.png') if p.is_file()]
        
        if not image_files:
            self.logger.warning(f"No PNG images found in {image_dir}. Nothing to process.")
            return

        ground_truth_dir = output_dir / "ground_truth"
        masks_dir = output_dir / "masks"
        ground_truth_dir.mkdir(parents=True, exist_ok=True)
        masks_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Generating masks for {len(image_files)} images from {image_dir.name} split...")

        for img_path in tqdm(image_files, desc=f"Generating masks for {image_dir.name}"):
            try:
                shutil.copy(img_path, ground_truth_dir / img_path.name)

                with Image.open(img_path) as img:
                    width, height = img.size

                mask_array = self.mask_generator(height, width)
                mask_image = Image.fromarray(mask_array, mode='L')

                mask_image.save(masks_dir / img_path.name)

            except Exception as e:
                self.logger.error(f"Failed to process or generate mask for {img_path}. Error: {e}")

        self.logger.info(f"Finished generating masks for the {image_dir.name} split.")
