# src/thesis_pipeline/components/model_training.py
import logging
import torch
import torch.nn.functional as F
from diffusers import AutoencoderKL, DDPMScheduler, UNet2DConditionModel
from transformers import CLIPTextModel, CLIPTokenizer
from torch.optim import AdamW
from diffusers.optimization import get_scheduler
from accelerate import Accelerator
from tqdm.auto import tqdm
from box import ConfigBox

class ModelTrainer:
    def __init__(self, config: ConfigBox, hyperparams: ConfigBox):
        self.config = config
        self.hyperparams = hyperparams
        self.logger = logging.getLogger(__name__)
        
        self.accelerator = Accelerator(
            mixed_precision=self.hyperparams.get('mixed_precision', 'no')
        )
        self.device = self.accelerator.device
        self.logger.info(f"Using device: {self.device} with mixed precision: {self.accelerator.mixed_precision}")

    def _load_pretrained_models(self):
        """Loads all necessary model components from Hugging Face."""
        try:
            model_id = self.hyperparams.model_id
            self.tokenizer = CLIPTokenizer.from_pretrained(model_id, subfolder="tokenizer")
            self.text_encoder = CLIPTextModel.from_pretrained(model_id, subfolder="text_encoder")
            self.vae = AutoencoderKL.from_pretrained(model_id, subfolder="vae")
            self.unet = UNet2DConditionModel.from_pretrained(model_id, subfolder="unet")
            self.noise_scheduler = DDPMScheduler.from_pretrained(model_id, subfolder="scheduler")
            
            self.vae.requires_grad_(False)
            self.text_encoder.requires_grad_(False)
            self.logger.info(f"Successfully loaded pretrained models from '{model_id}'")
        except Exception as e:
            self.logger.error(f"Failed to load models. Check model_id and internet. Error: {e}")
            raise

    def train(self, train_dataloader, val_dataloader):
        """The main training loop."""
        self._load_pretrained_models()

        optimizer = AdamW(
            self.unet.parameters(),
            lr=self.hyperparams.learning_rate,
            betas=(self.hyperparams.adam_beta1, self.hyperparams.adam_beta2),
            weight_decay=self.hyperparams.adam_weight_decay,
            eps=self.hyperparams.adam_epsilon,
        )
        
        lr_scheduler = get_scheduler(
            name="constant",
            optimizer=optimizer,
            num_warmup_steps=0,
            num_training_steps=len(train_dataloader) * self.config.num_epochs,
        )

        self.unet, optimizer, train_dataloader, val_dataloader, lr_scheduler = self.accelerator.prepare(
            self.unet, optimizer, train_dataloader, val_dataloader, lr_scheduler
        )

        text_input = self.tokenizer("", padding="max_length", max_length=self.tokenizer.model_max_length, truncation=True, return_tensors="pt")
        with torch.no_grad():
            text_embeddings = self.text_encoder(text_input.input_ids.to(self.device))[0]
        null_prompt_embeds = text_embeddings.repeat(self.config.train_batch_size, 1, 1)

        self.logger.info("Starting training loop...")
        for epoch in range(self.config.num_epochs):
            self.unet.train()
            progress_bar = tqdm(total=len(train_dataloader), desc=f"Epoch {epoch + 1}/{self.config.num_epochs}")
            
            for step, batch in enumerate(train_dataloader):
                with self.accelerator.accumulate(self.unet):
                    with torch.no_grad():
                        latents = self.vae.encode(batch["original_image"]).latent_dist.sample() * self.vae.config.scaling_factor
                        masked_latents = self.vae.encode(batch["masked_image"]).latent_dist.sample() * self.vae.config.scaling_factor
                    
                    mask = F.interpolate(batch["mask"], size=latents.shape[-2:])
                    noise = torch.randn_like(latents)
                    bsz = latents.shape[0]
                    timesteps = torch.randint(0, self.noise_scheduler.config.num_train_timesteps, (bsz,), device=latents.device).long()
                    noisy_latents = self.noise_scheduler.add_noise(latents, noise, timesteps)
                    
                    latent_model_input = torch.cat([noisy_latents, mask, masked_latents], dim=1)
                    noise_pred = self.unet(latent_model_input, timesteps, null_prompt_embeds).sample
                    loss = F.mse_loss(noise_pred, noise, reduction="mean")
                    
                    self.accelerator.backward(loss)
                    optimizer.step()
                    lr_scheduler.step()
                    optimizer.zero_grad()

                progress_bar.update(1)
                progress_bar.set_postfix(loss=loss.item())
            
            progress_bar.close()
            
            if (epoch + 1) % self.config.save_model_epochs == 0:
                self.accelerator.wait_for_everyone()
                unwrapped_unet = self.accelerator.unwrap_model(self.unet)
                save_path = Path(self.config.output_dir) / f"unet_epoch_{epoch+1}"
                unwrapped_unet.save_pretrained(save_path)
                self.logger.info(f"Saved model checkpoint to {save_path}")

        self.logger.info("Training finished.")
        return self.accelerator.unwrap_model(self.unet)
