class Image:
    def __init__(self, name=None, image=None, deployment=None, container=None):
        """Object to hold information about a container or related image

        :param image: Image
        :type image: string

        :param name: Name as identified in spec.relatedImages or olm.relatedImage annotation
        :type name: string

        :param deployment: Name of deployment(default: {None})
        :type deployment: string

        :param container: Name of container (default: {None})
        :type container: string
        """
        self.name       = name
        self.image      = image
        self.deployment = deployment
        self.container  = container
        self.tag        = None
        self.digest     = None
        self.full_image = None

        # Everything before the last '/' should make up repo
        self.image_repo = '/'.join(image.split('/')[:-1])
        remainder = image.split('/')[-1]
        if '@' in remainder and len(image.split(':')) > 2: #image name, tag and digest
            self.digest     = remainder.split('@')[1]
            self.image_name = remainder.split(':')[0]
            self.tag        = remainder.split('@')[0].split(':')[-1]
            self.full_image = self.image
            self.image      = f"{self.image_repo}/{self.image_name}@{self.digest}" 
        elif '@' in remainder: #image name and digest
            self.image_name = remainder.split('@')[0]
            self.digest     = remainder.split('@')[1]
            self.tag        = 'latest'
        elif ':' in remainder: #image name and tag
            self.image_name = remainder.split(':')[0]
            self.tag        = remainder.split(':')[1]
        else: #only image name
            self.image_name = remainder
            self.tag        = 'latest'

    def set_digest(self, digest):
        """Set image digest

        :param digest: Digest in format <type>:<hash>
        :type digest: string
        """
        if self.digest:
            # If already have a digest set we need to carefully replace
            self.image = self.image.replace(self.digest, digest)
            self.digest = digest
        else:
            self.digest = digest
            # We're assuming that when we're called the existing image doesn't have a digest
            self.image = '{}@{}'.format(self.image.split(':')[0], digest)
        return True

    def set_tag(self, tag):
        """Set new tag for image. Will update self.image only if image is identified by tag, but not overwrite digest

        :param tag: New tag to set
        :type tag: string
        """
        self.tag = tag
        if not self.digest:
            # We won't overwrite image info if we have digest
            self.image = '{}:{}'.format(self.image.split(':')[0], tag)

    def set_image_repo(self, repo):
        self.image      = self.image.replace(self.image_repo, repo)
        if self.full_image:
            self.full_image = self.full_image.replace(self.image_repo, repo)
        self.image_repo = repo
        return True

    def get_full_image(self):
        return self.full_image

    def set_full_image(self, full_image):
        self.full_image = full_image
    
    def get_image_repo(self):
        """Returns the image_repo section of the overall image

        :return: Image repo i.e. quay.io/myrepo]
        :rtype: string
        """
        return self.image_repo

    def get_digest(self):
        """Returns image digest 

        :return: Digest in format <type>:<hash> 
        :rtype: string
        """
        if hasattr(self, 'digest'):
            return self.digest
        else:
            return None

    def get_olm_name(self):
        """Return the name of the image. Typically associated with olm.relatedImage and spec.relatedImages

        :return: Name
        :rtype: string
        """
        return self.name

    def get_image_name(self):
        """Returns the image name, stripped of repo and tag/digest

        :return: Name
        :rtype: string
        """
        return self.image_name

    def get_tag(self):
        """Get the tag associated with an image if known

        :return: Tag
        :rtype: string
        """
        if hasattr(self, 'tag'):
            return self.tag
        else:
            return None

    def get_image(self):
        """Return the full image 

        :return: Full image in format <repo>/<name>[@digest][:tag]
        :rtype: string
        """
        return self.image