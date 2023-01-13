import fire
from roboflow2huggingface import roboflow_to_huggingface_pipeline


def app() -> None:
    """Cli app."""
    fire.Fire(roboflow_to_huggingface_pipeline)


if __name__ == "__main__":
    app()
