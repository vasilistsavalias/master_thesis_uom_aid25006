# src/thesis_pipeline/components/dataset.py
import logging
from pathlib import Path
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms

class InpaintingDataset(Dataset):
    """
    A PyTorch Dataset for the image inpainting task.
    It loads a ground truth image and its corresponding mask.
    """
    def __init__(self, data_dir: Path, image_size: list, split_name: str):
        """
        Args:
            data_dir (Path): Path to the root of the inpainting dataset.
            image_size (list): The target size [height, width] to resize images to.
            split_name (str): The name of the split to load ('train', 'validation', 'test').
        """
        self.image_dir = data_dir / split_name / 'ground_truth'
        self.mask_dir = data_dir / split_name / 'masks'
        self.logger = logging.getLogger(__name__)
        
        self.image_files = sorted([p for p in self.image_dir.glob('*.png') if p.is_file()])
        self.mask_files = sorted([p for p in self.mask_dir.glob('*.png') if p.is_file()])

        if not self.image_files:
            self.logger.warning(f"No images found in {self.image_dir}. This split will be empty.")
        if len(self.image_files) != len(self.mask_files):
            raise ValueError(f"Number of images and masks do not match in '{split_name}' split!")
        
        self.logger.info(f"Loaded {len(self.image_files)} samples from '{split_name}' split.")

        self.transform = transforms.Compose([
            transforms.Resize(image_size, interpolation=transforms.InterpolationMode.BILINEar),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])
        
        self.mask_transform = transforms.Compose([
            transforms.Resize(image_size, interpolation=transforms.InterpolationMode.NEAREST),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        try:
            image_path = self.image_files[idx]
            mask_path = self.mask_files[idx]
            
            original_image = Image.open(image_path).convert("RGB")
            mask = Image.open(mask_path).convert("L")

            original_image_tensor = self.transform(original_image)
            mask_tensor = self.mask_transform(mask)
            
            masked_image_tensor = original_image_tensor * (1 - mask_tensor)

            return {
                "original_image": original_image_tensor,
                "masked_image": masked_image_tensor,
                "mask": mask_tensor
            }
        except Exception as e:
            self.logger.error(f"Error loading sample {idx} ({self.image_files[idx]}). Error: {e}")
            return self.__getitem__((idx + 1) % len(self))
