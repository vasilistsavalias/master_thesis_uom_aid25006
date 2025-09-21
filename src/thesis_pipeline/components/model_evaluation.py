# src/thesis_pipeline/components/model_evaluation.py
import logging
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from diffusers import StableDiffusionInpaintingPipeline

class ModelEvaluator:
    def __init__(self, config, test_data_dir: Path):
        self.config = config
        self.test_data_dir = test_data_dir
        self.device = config.device
        self.output_dir = Path(config.output_dir)
        self.logger = logging.getLogger(__name__)

    def _load_pipeline(self):
        """Loads the trained model into an inpainting pipeline."""
        try:
            model_path = Path(self.config.trained_model_dir) / "unet_final"
            pipeline = StableDiffusionInpaintingPipeline.from_pretrained(
                "runwayml/stable-diffusion-inpainting",
                unet=model_path,
                device_map=self.device,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            )
            self.logger.info(f"Successfully loaded pipeline with UNet from: {model_path}")
            return pipeline
        except Exception as e:
            self.logger.error(f"Failed to load the inpainting pipeline. Error: {e}")
            raise

    def evaluate(self):
        """Runs the full evaluation process."""
        pipeline = self._load_pipeline()
        
        image_dir = self.test_data_dir / 'ground_truth'
        mask_dir = self.test_data_dir / 'masks'

        image_files = sorted([p for p in image_dir.glob('*.png') if p.is_file()])
        mask_files = sorted([p for p in mask_dir.glob('*.png') if p.is_file()])

        if not image_files or not mask_files:
            self.logger.warning("Test data not found. Skipping evaluation.")
            return

        num_samples = self.config.num_samples_to_evaluate
        if num_samples > 0 and num_samples < len(image_files):
            image_files = image_files[:num_samples]
            mask_files = mask_files[:num_samples]
        
        self.logger.info(f"Evaluating on {len(image_files)} samples.")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        comparison_dir = self.output_dir / "comparisons"
        comparison_dir.mkdir(exist_ok=True)

        results = []
        generator = torch.Generator(device=self.device).manual_seed(0)

        for img_path, mask_path in tqdm(zip(image_files, mask_files), total=len(image_files), desc="Evaluating"):
            try:
                original_image = Image.open(img_path).convert("RGB")
                mask_image = Image.open(mask_path).convert("RGB")

                with torch.no_grad():
                    restored_image = pipeline(
                        prompt="", image=original_image, mask_image=mask_image,
                        num_inference_steps=self.config.num_inference_steps,
                        generator=generator,
                    ).images[0]

                original_np = np.array(original_image)
                restored_np = np.array(restored_image)
                
                current_psnr = psnr(original_np, restored_np, data_range=255)
                current_ssim = ssim(original_np, restored_np, data_range=255, channel_axis=2)
                results.append({'filename': img_path.name, 'psnr': current_psnr, 'ssim': current_ssim})

                masked_image = Image.fromarray(original_np * (np.array(mask_image) < 128))
                comparison_img = Image.new('RGB', (original_image.width * 3, original_image.height))
                comparison_img.paste(original_image, (0, 0))
                comparison_img.paste(masked_image, (original_image.width, 0))
                comparison_img.paste(restored_image, (original_image.width * 2, 0))
                comparison_img.save(comparison_dir / f"compare_{img_path.name}")

            except Exception as e:
                self.logger.error(f"Failed on sample {img_path.name}. Error: {e}")

        if results:
            df = pd.DataFrame(results)
            df.to_csv(self.output_dir / "evaluation_metrics.csv", index=False)
            
            summary = f"Samples: {len(df)}\nAvg PSNR: {df['psnr'].mean():.4f}\nAvg SSIM: {df['ssim'].mean():.4f}"
            with open(self.output_dir / "summary_report.txt", 'w') as f:
                f.write(summary)
            self.logger.info(f"Evaluation Complete. {summary}")
        else:
            self.logger.warning("No results generated during evaluation.")
