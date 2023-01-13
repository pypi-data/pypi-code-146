from pickle import UnpicklingError
from typing import Any, Tuple

from baseten.baseten_deployed_model import BasetenDeployedModel
from baseten.models.util import (from_object_to_str, from_str_to_object,
                                 get_or_create_pretrained_model,
                                 requests_error_handling)


class StableDiffusionPipeline():
    """
    Support for Stable Diffusion diffusion model for text-to-image generation.

    Attributes
    ----------
    hf_pretrained_model : str
        Name of the Hugging Face pretrained model to use for text-to-image generation.
        By default, we will use the v1.5 version provided by Huggingface.

    vae : str
        Name of the pretrained VAE model to use for image reconstruction. By default,
        we will use the "default" VAE. Users can also specify a custom VAE model either
            - stabilityai/sd-vae-ft-mse
            - stabilityai/sd-vae-ft-ema

    scheduler: str OR SchedulerMixin object
        Name of the scheduler to use for the diffusion process. By default, we will use
        the "dpmsolver" scheduler. Users can also specify a custom scheduler that is either
        one of
            - dpmsolver
            - ddim
            - euler
            - lms
            - pndm
            - eulera
        A user can also specify a custom scheduler by passing in a scheduler object that
        is a subclass of the diffusers.scheduler Mixin.

    Methods
    -------
    __call__(prompt, **kwargs) -> Tuple(PIL.Image, boolean)
        Generate image from a prompt. Supports all parameters of the underlying model

    Examples
    --------
    >>> from baseten.models import StableDiffusionPipeline
    >>> model = StableDiffusionPipeline()
    >>> image, success = model("A dog is running in the grass")

    >>> from baseten.models import StableDiffusionPipeline
    >>> from diffusers import LMSDiscreteScheduler
    >>> lms = LMSDiscreteScheduler()
    >>> model = StableDiffusionPipeline(scheduler=lms)
    >>> image, safe = model("A dog is running in the grass")

    >>> from baseten.models import StableDiffusionPipeline
    >>> model = StableDiffusionPipeline(vae="stabilityai/sd-vae-ft-mse")
    >>> image, safe = model("A dog is running in the grass")

    >>> from baseten.models import StableDiffusionPipeline
    >>> model = StableDiffusionPipeline("runwayml/stable-diffusion-v1-5",
    >>>     vae="stabilityai/sd-vae-ft-mse", scheduler="pndm")
    >>> image, safe = model("A dog is running in the grass", seed=2)
    """
    def __init__(
        self,
        hf_pretrained_model_path: str = "runwayml/stable-diffusion-v1-5",
        vae: str = "default",
        scheduler: str = "dpmsolver",
    ):
        self._supported_alterations = {
            "model" : ["runwayml/stable-diffusion-v1-5"],
            "vae" : ["stabilityai/sd-vae-ft-mse", "stabilityai/sd-vae-ft-ema", "default"],
            "scheduler": ["ddim", "euler", "lms", "pndm", "eulera", "dpmsolver"]
        }
        self._hf_pretrained_model_path = hf_pretrained_model_path
        self.vae = vae
        self.scheduler = scheduler
        self.safety_checker = None
        self.feature_extractor = None
        self._model = self._set_user_model()
        self._is_model_components_supported()

    def _set_user_model(self) -> BasetenDeployedModel:
        """Creates internal BasetenDeployedModel object that points to users
        deployed Stable Diffusion model. If the user does not have a deployed
        model, we will create one for them.
        """
        model_version = get_or_create_pretrained_model("Stable Diffusion")
        return BasetenDeployedModel(
            model_id=model_version["model_id"],
            truss_spec_version=model_version["truss_spec_version"]
        )

    def _is_supported_scheduler(self, scheduler) -> None :
        """Checks if the scheduler is supported by the BasetenDeployedModel
        """
        supported_schedulers = self._supported_alterations["scheduler"]
        if scheduler not in supported_schedulers:
            # Check if scheduler is from diffusers.scheduler
            if "diffusers.scheduler" not in str(type(self.scheduler)):
                raise ValueError(f"""
                    Scheduler must be one of {' or '.join(self._supported_alterations['scheduler'])}
                    or a Diffusers scheduler
                """)

    def _is_supported_vae(self, vae) -> None:
        """Checks if the vae is supported by the BasetenDeployedModel
        """
        if vae not in self._supported_alterations["vae"]:
            raise ValueError(f"""
                VAE must be one of {' or '.join(self._supported_alterations['vae'])} as str
            """)

    def _is_supported_model(self, model) -> None:
        """Checks if the model version is supported by the BasetenDeployedModel
        """
        if model not in self._supported_alterations["model"]:
            raise ValueError(f"""
                Pretrained model path must be one of {' or '.join(self._supported_alterations['model'])}
            """)

    def _is_model_components_supported(self) -> None:
        """Checks if model components are supported by the BasetenDeployedModel
        before request to the model is made.
        """
        self._is_supported_model(self._hf_pretrained_model_path)
        self._is_supported_vae(self.vae)
        self._is_supported_scheduler(self.scheduler)

    def __setattr__(self, __name: str, __value: Any) -> None:
        """Prevents users from setting unsupported model components
        """
        if __name in ["unet", "tokenizer", "text_encoder"]:
            raise ValueError(f"{__name} not settable on free-tier")
        super().__setattr__(__name, __value)

    def __call__(
        self,
        prompt: str,
        height: int = 512,
        width: int = 512,
        guidance_scale: float = 7.5,
        num_images_per_prompt: int = 1,
        eta: float = 0.0,
        seed: int = -1,
        num_inference_steps: int = -1,
    ) -> Tuple:
        """Generate image from a prompt. Supports all parameters of the underlying model
        from diffusers library.

        Args:
            prompt (str): Text prompt to generate image from
            height (int, optional): Height of the generated image. Defaults to 512.
            width (int, optional): Width of the generated image. Defaults to 512.
            guidance_scale (float, optional): Guidance scale for the diffusion process.
                Defaults to 7.5.
            num_images_per_prompt (int, optional): Number of images to generate per prompt.
                Defaults to 1.
            eta (float, optional): Eta value for the diffusion process. Defaults to 0.0.
            seed (int, optional): Seed for the diffusion process. Defaults to -1, which will
                use a random seed.
            num_inference_steps (int, optional): Number of inference steps for the
                diffusion process. Defaults to None.

        Returns:
            Tuple: Tuple of List[PIL.Image], boolean indicating if the image is safe, and list of
            s3_urls for images returned.
        """
        self._is_model_components_supported()

        # If default scheduler, DPMSolver, is being used, set num_inference_steps to 30
        # instead of 50 as it requires less time steps for high quality generation
        if num_inference_steps < 0:
            num_inference_steps = 30 if self.scheduler == "DPMSolver" else 50

        request_body = {
            "prompt" : prompt,
            "height" : height,
            "width" : width,
            "guidance_scale": guidance_scale,
            "num_images_per_prompt" : num_images_per_prompt,
            "eta" : eta,
            "seed" : seed,
            "num_inference_steps" : num_inference_steps,
            "scheduler" : self.scheduler if isinstance(self.scheduler, str) else from_object_to_str(self.scheduler),
            "vae" : self.vae,
            "b64_response" : False
        }
        with requests_error_handling():
            server_response = self._model.predict(request_body)

        if server_response["status"] == "error":
            raise ValueError(server_response["message"])

        try:
            output = from_str_to_object(server_response["data"][0])
        except UnpicklingError:
            raise ValueError("Error unpickling response. This may be due to an older \
                Python version. If so, please `pip install pickle5` and try again.")
        except ValueError:
            raise ValueError("Corruputed network bytes")

        from baseten.common.files import upload_pil_to_s3

        # The server returns a Tuple of (PIL, bool)
        if output[1] is None:
            pil_objects = output[0]
            s3_urls = [upload_pil_to_s3(pil_object) for pil_object in pil_objects]

            return (output[0], False, s3_urls)
        return output
