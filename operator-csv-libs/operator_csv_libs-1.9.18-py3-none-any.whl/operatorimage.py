# Defines what an operator image definition looks like
class Operatorimage:
    deployment = None
    container  = None
    image      = None
    digest     = None
    tag        = None
    image_name = None
    image_repo = None

    def __init__(self, deployment=None, container=None, image=None):
        self.deployment = deployment
        self.container = container
        self.image = image
        # Everything before the last '/' should make up repo
        self.image_repo = '/'.join(image.split('/')[:-1])
        remainder = image.split('/')[-1]
        if '@' in remainder:
            self.image_name = remainder.split('@')[0]
            self.digest     = remainder.split('@')[1]
        else:
            self.image_name = remainder.split(':')[0]
            self.tag        = remainder.split(':')[1]
    
    def set_digest(self, digest):
        self.digest = digest
        # We're assuming that when we're called the existing image doesn't have a digest
        self.image = '{}@{}'.format(self.image.split(':')[0], digest)