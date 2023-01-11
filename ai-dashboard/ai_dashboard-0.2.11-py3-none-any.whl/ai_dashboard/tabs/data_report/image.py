import os


def is_path(path: str) -> bool:
    return os.path.isfile(path)


def image(image_src: str):
    return [
        {
            "type": "appBlock",
            "content": [
                {
                    "type": "imageDisplayBlock",
                    "attrs": {
                        "imageSrc": image_src,
                        "title": "",
                        "width": "100%",
                        "height": "auto",
                    },
                }
            ],
        }
    ]
