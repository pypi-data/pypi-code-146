from baseten.baseten_deployed_model import BasetenDeployedModel
from baseten.models.util import (get_or_create_pretrained_model,
                                 requests_error_handling, upload_file_to_s3)


class Whisper():
    def __init__(self):
        """
        Support for Whisper model for audio-to-text generation.

        Methods
        -------
        __call__(path, **kwargs) -> str
            Generate text from an audio file. Supports local file paths or URLs.

        Examples
        --------
        >>> from baseten.models import Whisper
        >>> model = Whisper()
        >>> model("https://baseten.s3.amazonaws.com/whisper/whisper_test.wav")

        >>> model = Whisper()
        >>> model("whisper_test.wav")
        """
        self._model = self._set_user_model()

    def _set_user_model(self) -> BasetenDeployedModel:
        """Creates internal BasetenDeployedModel object that points to users
        deployed Whisper model. If the user does not have a deployed model,
        we will create one for them.
        """
        model_version = get_or_create_pretrained_model("Whisper")
        return BasetenDeployedModel(
            model_id=model_version["model_id"],
            truss_spec_version=model_version["truss_spec_version"]
        )

    def __call__(self, path: str, **kwargs) -> dict:
        """ Generate text from an audio file. Supports local file paths or URLs.

        Args:
            path (str): Path to audio file. Can be a local file path or a URL.

        Returns:
            dict: Dictionary containing 3 keys: "language", "segments", and "text". Language is
                a str representing the language of the audio file. Segments is a list of dicts,
                each containing the "start" and "end" keys which correspond to the start and end
                times of the segment in seconds. They also contain a "text" key which is the text
                generated for that segment. Text is a string containing the full text generated
                for the audio file.
        """
        is_url = path.startswith("http")
        if not is_url:
            path = upload_file_to_s3(path)

        request_body = {
            "url" : path,
        }

        # TODO: Whisper model needs to have updated spec that returns status
        with requests_error_handling():
            server_response = self._model.predict(request_body)

        return server_response
