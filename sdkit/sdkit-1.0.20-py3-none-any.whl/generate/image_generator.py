import torch
from tqdm import trange
from pytorch_lightning import seed_everything
from contextlib import nullcontext

from sdkit import Context
from sdkit.utils import latent_samples_to_images, base64_str_to_img, get_image_latent_and_mask, apply_color_profile
from sdkit.utils import gc

from .prompt_parser import get_cond_and_uncond
from .sampler import make_samples

def generate_images(
        context: Context,
        prompt: str = "",
        negative_prompt: str = "",

        seed: int = 42,
        width: int = 512,
        height: int = 512,

        num_outputs: int = 1,
        num_inference_steps: int = 25,
        guidance_scale: float = 7.5,

        init_image = None,
        init_image_mask = None,
        prompt_strength: float = 0.8,
        preserve_init_image_color_profile = False,

        sampler_name: str = "euler_a", # "ddim", "plms", "heun", "euler", "euler_a", "dpm2", "dpm2_a", "lms",
                                       # "dpm_solver_stability", "dpmpp_2s_a", "dpmpp_2m", "dpmpp_sde", "dpm_fast"
                                       # "dpm_adaptive"
        hypernetwork_strength: float = 0,

        callback=None,
    ):
    req_args = locals()

    try:
        images = []

        seed_everything(seed)
        precision_scope = torch.autocast if context.half_precision and context.device != "cpu" else nullcontext

        model = context.models['stable-diffusion']
        if 'hypernetwork' in context.models:
            context.models['hypernetwork']['hypernetwork_strength'] = hypernetwork_strength

        print('pre cond')
        print_mem(context)

        with precision_scope("cuda"):
            cond, uncond = get_cond_and_uncond(prompt, negative_prompt, num_outputs, model)

        model.cond_stage_model.to('cpu')
        model.cond_stage_model.device = 'cpu'
        model.cond_stage_model.transformer.to('cpu')
        gc(context)
        print_state(model)
        print('post cond')
        print_mem(context)

        generate_fn = txt2img if init_image is None else img2img
        common_sampler_params = {
            'context': context,
            'sampler_name': sampler_name,
            'seed': seed,
            'batch_size': num_outputs,
            'shape': [4, height // 8, width // 8],
            'cond': cond,
            'uncond': uncond,
            'guidance_scale': guidance_scale,
            'callback': callback,
        }

        print('pre-img')
        print_mem(context)

        with torch.no_grad(), precision_scope("cuda"):
            for _ in trange(1, desc="Sampling"):
                print('pre-img sampler')
                print_mem(context)
                images += generate_fn(common_sampler_params.copy(), **req_args)
                gc(context)

        del cond, uncond
        gc(context)

        return images
    finally:
        context.init_image_latent, context.init_image_mask_tensor = None, None

        model = context.models['stable-diffusion']
        print('model', model.model.device)
        print('cs', model.cond_stage_model.device)
        print('fs', model.first_stage_model.device)

        if hasattr(context, 'module_in_gpu') and context.module_in_gpu is not None and len(context.vram_optimizations) > 0:
            print('moving to cpu')
            context.module_in_gpu.to('cpu')
            context.module_in_gpu = None

        print('model', model.model.device)
        print('cs', model.cond_stage_model.device)
        print('fs', model.first_stage_model.device)

        print('clearing mem')
        print_mem(context)
        gc(context)
        print('cleared mem')
        print_mem(context)

def print_mem(context):
    mem_free, mem_total = torch.cuda.mem_get_info(context.device)
    mem_used = mem_total - mem_free
    mem_used /= float(10**9)
    print('mem_used', mem_used)

def print_state(model):
    print('state:')
    print('. model', model.model.device)
    print('. cs', model.cond_stage_model.device)
    print('. fs', model.first_stage_model.device)

def txt2img(params: dict, context: Context, num_inference_steps, **kwargs):
    params.update({
        'steps': num_inference_steps,
    })

    samples = make_samples(**params)
    print('post sampler')
    print_mem(context)

    images = latent_samples_to_images(context, samples)
    print('post images')
    print_mem(context)
    del samples

    print('post del samples')
    print_mem(context)

    return images

def img2img(params: dict, context: Context, num_inference_steps, num_outputs, width, height, init_image, init_image_mask, prompt_strength, preserve_init_image_color_profile, **kwargs):
    init_image = base64_str_to_img(init_image) if isinstance(init_image, str) else init_image
    init_image_mask = base64_str_to_img(init_image_mask) if isinstance(init_image_mask, str) else init_image_mask

    if not hasattr(context, 'init_image_latent') or context.init_image_latent is None:
        context.init_image_latent, context.init_image_mask_tensor = get_image_latent_and_mask(context, init_image, init_image_mask, width, height, num_outputs)

    params.update({
        'steps': num_inference_steps,
        'init_image_latent': context.init_image_latent,
        'mask': context.init_image_mask_tensor,
        'prompt_strength': prompt_strength,
    })

    samples = make_samples(**params)
    images = latent_samples_to_images(context, samples)
    del samples

    if preserve_init_image_color_profile:
        for i, img in enumerate(images):
            images[i] = apply_color_profile(init_image, img)

    return images
