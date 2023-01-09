import os

class Parser:

    def __init__(self):
        pass

class ImageNameParser(Parser):

    def __init__(self):
        pass

    def parse(self, name, *args, **kwargs):
        """Sanitizes the image name. Adding :latest to non tagged images"""

        # Splits the image name
        name = name.split(':')

        # The image name is always the first
        image = name.pop(0)

        if len(name) >= 1:
            tag = ''.join(name).replace(':', '')

        else:
            tag = 'latest'

        return f'{image}:{tag}'
