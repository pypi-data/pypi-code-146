from typing import List, Optional

import PIL
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import torch
from einops import rearrange, repeat
from pytorch_lightning import seed_everything

import classy_imaginary.config as config
from classy_imaginary.api import _prompts_to_embeddings, IMAGINAIRY_SAFETY_MODE
from classy_imaginary import ImaginePrompt, ImagineResult
from classy_imaginary.enhancers.clip_masking import get_img_mask
from classy_imaginary.enhancers.face_restoration_codeformer import enhance_faces
from classy_imaginary.enhancers.upscale_realesrgan import upscale_image
from classy_imaginary.img_utils import pillow_fit_image_within, pillow_img_to_torch_image
from classy_imaginary.log_utils import ImageLoggingContext, log_conditioning, log_img, log_latent
from classy_imaginary.model_manager import get_diffusion_model
from classy_imaginary.modules.midas.utils import AddMiDaS
from classy_imaginary.safety import create_safety_score, EnhancedStableDiffusionSafetyChecker
from classy_imaginary.samplers import SAMPLER_LOOKUP
from classy_imaginary.samplers.base import NoiseSchedule, noise_an_image
from classy_imaginary.utils import get_device, platform_appropriate_autocast, fix_torch_nn_layer_norm, \
    fix_torch_group_norm, randn_seeded
import logging
from transformers import logging as transformers_logging, AutoFeatureExtractor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
transformers_logging.set_verbosity_error()


# logging.disable_default_handler()


class Imagine:
    def __init__(self,
                 model_name: str = config.DEFAULT_MODEL,
                 half_mode: bool = None,
                 precision="autocast",
                 for_inpainting: bool = False,
                 nsfw_filter: bool = False):
        """
        Initialize the Imagine class.
        :param model_name: the name of the SD model to use.
        :param half_mode: whether to use half-precision. If None, will use half-precision if available.
        :param precision: whether to use autocast or not.
        :param for_inpainting: whether to use the model for inpainting.
        """
        self.model_name = model_name
        self.half_mode = half_mode
        self.precision = precision
        self.for_inpainting = for_inpainting
        self.sd_model = get_diffusion_model(
            weights_location=model_name,
            half_mode=half_mode,
            for_inpainting=for_inpainting,
        )

        safety_model_id = "CompVis/stable-diffusion-safety-checker"
        self.nsfw_filter = nsfw_filter
        if for_inpainting:
            self.midas_model = AddMiDaS()
        if nsfw_filter:
            self.safety_feature_extractor = AutoFeatureExtractor.from_pretrained(safety_model_id)
            self.safety_checker = EnhancedStableDiffusionSafetyChecker.from_pretrained(
                safety_model_id
            )

    def imagine(self,
                prompt: ImaginePrompt,
                debug_img_callback=None,
                progress_img_callback=None,
                progress_img_interval_steps=3,
                progress_img_interval_min_s=0.1) -> Optional[ImagineResult]:
        """
        Run inference on the model.
        :param prompt: ImaginePrompt.
        :param debug_img_callback: a callback that will be called with the debug image.
        :param progress_img_callback: a callback that will be called with the progress image.
        :param progress_img_interval_steps: the number of steps between progress images.
        :param progress_img_interval_min_s: the minimum time between progress images.
        :return: a list of ImagineResult objects.
        """
        latent_channels = 4
        downsampling_factor = 8
        batch_size = 1

        if get_device() == "cpu":
            logger.info(f"This will take a while on CPU. Consider using a GPU.")

        with torch.no_grad(), platform_appropriate_autocast(
                self.precision
        ), fix_torch_nn_layer_norm(), fix_torch_group_norm():
            logger.info(f"Running inference on prompt {prompt.prompt_text}")
            has_depth_channel = hasattr(self.sd_model, "depth_stage_key")
            with ImageLoggingContext(
                    prompt=prompt,
                    model=self.sd_model,
                    debug_img_callback=debug_img_callback,
                    progress_img_callback=progress_img_callback,
                    progress_img_interval_steps=progress_img_interval_steps,
                    progress_img_interval_min_s=progress_img_interval_min_s,
            ) as lc:
                seed_everything(prompt.seed)
                self.sd_model.tile_mode(prompt.tile_mode)
                with lc.timing("conditioning"):
                    # need to expand if doing batches
                    neutral_conditioning = _prompts_to_embeddings(
                        prompt.negative_prompt, self.sd_model
                    )
                    log_conditioning(neutral_conditioning, "neutral conditioning")
                    if prompt.conditioning is not None:
                        positive_conditioning = prompt.conditioning
                    else:
                        positive_conditioning = _prompts_to_embeddings(
                            prompt.prompts, self.sd_model
                        )
                    log_conditioning(positive_conditioning, "positive conditioning")

                shape = [
                    batch_size,
                    latent_channels,
                    prompt.height // downsampling_factor,
                    prompt.width // downsampling_factor,
                ]

                SamplerCls = SAMPLER_LOOKUP[prompt.sampler_type.lower()]
                sampler = SamplerCls(self.sd_model)
                mask = mask_image = mask_image_orig = mask_grayscale = None
                t_enc = init_latent = init_latent_noised = None

                if prompt.init_image:
                    generation_strength = 1 - prompt.init_image_strength
                    t_enc = int(prompt.steps * generation_strength)
                    try:
                        init_image = pillow_fit_image_within(
                            prompt.init_image,
                            max_height=prompt.height,
                            max_width=prompt.width,
                        )
                    except PIL.UnidentifiedImageError:
                        logger.warning(f"Could not load image: {prompt.init_image}")
                        return

                    init_image_t = pillow_img_to_torch_image(init_image)

                    if prompt.mask_prompt:
                        mask_image, mask_grayscale = get_img_mask(
                            init_image, prompt.mask_prompt, threshold=0.1
                        )
                    elif prompt.mask_image:
                        mask_image = prompt.mask_image.convert("L")

                    if mask_image is not None:
                        log_img(mask_image, "init mask")
                        if prompt.mask_mode == ImaginePrompt.MaskMode.REPLACE:
                            mask_image = ImageOps.invert(mask_image)

                        log_img(
                            Image.composite(init_image, mask_image, mask_image),
                            "mask overlay",
                        )
                        mask_image_orig = mask_image
                        mask_image = mask_image.resize(
                            (
                                mask_image.width // downsampling_factor,
                                mask_image.height // downsampling_factor,
                            ),
                            resample=Image.Resampling.LANCZOS,
                        )
                        log_img(mask_image, "latent_mask")

                        mask = np.array(mask_image)
                        mask = mask.astype(np.float32) / 255.0
                        mask = mask[None, None]
                        mask = torch.from_numpy(mask)
                        mask = mask.to(get_device())

                    init_image_t = init_image_t.to(get_device())
                    init_latent = self.sd_model.get_first_stage_encoding(
                        self.sd_model.encode_first_stage(init_image_t)
                    )
                    shape = init_latent.shape

                    log_latent(init_latent, "init_latent")
                    # encode (scaled latent)
                    seed_everything(prompt.seed)
                    noise = randn_seeded(seed=prompt.seed, size=init_latent.size())
                    noise = noise.to(get_device())

                    schedule = NoiseSchedule(
                        model_num_timesteps=self.sd_model.num_timesteps,
                        ddim_num_steps=prompt.steps,
                        model_alphas_cumprod=self.sd_model.alphas_cumprod,
                        ddim_discretize="uniform",
                    )

                    if generation_strength >= 1:
                        # prompt strength gets converted to time encodings,
                        # which means you can't get to true 0 without this hack
                        # (or setting steps=1000)
                        init_latent_noised = noise
                    else:
                        init_latent_noised = noise_an_image(
                            init_latent,
                            torch.tensor([t_enc - 1]).to(get_device()),
                            schedule=schedule,
                            noise=noise,
                        )
                batch_size = 1
                log_latent(init_latent_noised, "init_latent_noised")
                batch = {
                    "txt": batch_size * [prompt.prompt_text],
                }
                c_cat = []
                depth_image_display = None

                if has_depth_channel and prompt.init_image:
                    _init_image_d = np.array(prompt.init_image.convert("RGB"))
                    _init_image_d = (
                            torch.from_numpy(_init_image_d).to(dtype=torch.float32) / 127.5
                            - 1.0
                    )
                    depth_image = self.midas_model(_init_image_d)
                    depth_image = torch.from_numpy(depth_image[None, ...])
                    batch[self.sd_model.depth_stage_key] = depth_image.to(device=get_device())
                    _init_image_d = rearrange(_init_image_d, "h w c -> 1 c h w")
                    batch["jpg"] = _init_image_d

                    for ck in self.sd_model.concat_keys:
                        cc = batch[ck]
                        cc = self.sd_model.depth_model(cc)
                        depth_min, depth_max = torch.amin(
                            cc, dim=[1, 2, 3], keepdim=True
                        ), torch.amax(cc, dim=[1, 2, 3], keepdim=True)
                        display_depth = (cc - depth_min) / (depth_max - depth_min)
                        depth_image_display = Image.fromarray(
                            (display_depth[0, 0, ...].cpu().numpy() * 255.0).astype(
                                np.uint8
                            )
                        )
                        cc = torch.nn.functional.interpolate(
                            cc,
                            size=shape[2:],
                            mode="bicubic",
                            align_corners=False,
                        )
                        depth_min, depth_max = torch.amin(
                            cc, dim=[1, 2, 3], keepdim=True
                        ), torch.amax(cc, dim=[1, 2, 3], keepdim=True)
                        cc = 2.0 * (cc - depth_min) / (depth_max - depth_min) - 1.0
                        c_cat.append(cc)
                    c_cat = [torch.cat(c_cat, dim=1)]

                if mask_image_orig and not has_depth_channel:
                    mask_t = pillow_img_to_torch_image(
                        ImageOps.invert(mask_image_orig)
                    ).to(get_device())
                    inverted_mask = 1 - mask
                    masked_image_t = init_image_t * (mask_t < 0.5)
                    batch.update(
                        {
                            "image": repeat(
                                init_image_t.to(device=get_device()),
                                "1 ... -> n ...",
                                n=batch_size,
                            ),
                            "txt": batch_size * [prompt.prompt_text],
                            "mask": repeat(
                                inverted_mask.to(device=get_device()),
                                "1 ... -> n ...",
                                n=batch_size,
                            ),
                            "masked_image": repeat(
                                masked_image_t.to(device=get_device()),
                                "1 ... -> n ...",
                                n=batch_size,
                            ),
                        }
                    )

                    for concat_key in getattr(self.sd_model, "concat_keys", []):
                        cc = batch[concat_key].float()
                        if concat_key != self.sd_model.masked_image_key:
                            bchw = [batch_size, 4, shape[2], shape[3]]
                            cc = torch.nn.functional.interpolate(cc, size=bchw[-2:])
                        else:
                            cc = self.sd_model.get_first_stage_encoding(
                                self.sd_model.encode_first_stage(cc)
                            )
                        c_cat.append(cc)
                    if c_cat:
                        c_cat = [torch.cat(c_cat, dim=1)]

                positive_conditioning = {
                    "c_concat": c_cat,
                    "c_crossattn": [positive_conditioning],
                }
                neutral_conditioning = {
                    "c_concat": c_cat,
                    "c_crossattn": [neutral_conditioning],
                }

                with lc.timing("sampling"):
                    samples = sampler.sample(
                        num_steps=prompt.steps,
                        initial_latent=init_latent_noised,
                        positive_conditioning=positive_conditioning,
                        neutral_conditioning=neutral_conditioning,
                        guidance_scale=prompt.prompt_strength,
                        t_start=t_enc,
                        mask=mask,
                        orig_latent=init_latent,
                        shape=shape,
                        batch_size=1,
                    )

                x_samples = self.sd_model.decode_first_stage(samples)
                x_samples = torch.clamp((x_samples + 1.0) / 2.0, min=0.0, max=1.0)

                for x_sample in x_samples:
                    x_sample = x_sample.to(torch.float32)
                    x_sample = 255.0 * rearrange(
                        x_sample.cpu().numpy(), "c h w -> h w c"
                    )
                    x_sample_8_orig = x_sample.astype(np.uint8)
                    img = Image.fromarray(x_sample_8_orig)
                    if mask_image_orig and init_image:
                        mask_final = mask_image_orig.filter(
                            ImageFilter.GaussianBlur(radius=3)
                        )
                        log_img(mask_final, "reconstituting mask")
                        mask_final = ImageOps.invert(mask_final)
                        img = Image.composite(img, init_image, mask_final)
                        log_img(img, "reconstituted image")

                    upscaled_img = None
                    rebuilt_orig_img = None

                    if self.nsfw_filter:
                        with lc.timing("safety-filter"):
                            safety_score = create_safety_score(
                                self.safety_checker,
                                self.safety_feature_extractor,
                                img,
                                safety_mode=IMAGINAIRY_SAFETY_MODE
                            )

                    if not self.nsfw_filter or not safety_score.is_filtered:
                        if prompt.fix_faces:
                            logger.info("Fixing 😊 's in 🖼  using CodeFormer...")
                            img = enhance_faces(img, fidelity=prompt.fix_faces_fidelity)
                        if prompt.upscale:
                            logger.info("Upscaling 🖼  using real-ESRGAN...")
                            upscaled_img = upscale_image(img)

                        # put the newly generated patch back into the original, full size image
                        if (
                                prompt.mask_modify_original
                                and mask_image_orig
                                and prompt.init_image
                        ):
                            img_to_add_back_to_original = (
                                upscaled_img if upscaled_img else img
                            )
                            img_to_add_back_to_original = (
                                img_to_add_back_to_original.resize(
                                    prompt.init_image.size,
                                    resample=Image.Resampling.LANCZOS,
                                )
                            )

                            mask_for_orig_size = mask_image_orig.resize(
                                prompt.init_image.size,
                                resample=Image.Resampling.LANCZOS,
                            )
                            mask_for_orig_size = mask_for_orig_size.filter(
                                ImageFilter.GaussianBlur(radius=5)
                            )
                            log_img(mask_for_orig_size, "mask for original image size")

                            rebuilt_orig_img = Image.composite(
                                prompt.init_image,
                                img_to_add_back_to_original,
                                mask_for_orig_size,
                            )
                            log_img(rebuilt_orig_img, "reconstituted original")

                    result = ImagineResult(
                        img=img,
                        prompt=prompt,
                        upscaled_img=upscaled_img,
                        is_nsfw=False if self.nsfw_filter is False else safety_score.is_nsfw,
                        safety_score=None if self.nsfw_filter is False else safety_score,
                        modified_original=rebuilt_orig_img,
                        mask_binary=mask_image_orig,
                        mask_grayscale=mask_grayscale,
                        depth_image=depth_image_display,
                        timings=lc.get_timings(),
                    )
                    logger.info(f"Image Generated. Timings: {result.timings_str()}")

                return result
