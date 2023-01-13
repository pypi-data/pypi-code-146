import logging, sys, copy, yaml, ast
from .images import Image

class _literal(str):
    pass

def _literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

class ClusterServiceVersion:
    LATEST_IMAGE_INDICATOR   = '-latest'
    RELATED_IMAGE_IDENTIFIER = 'olm.relatedImage.'
    TAGGED_RELATED_IMAGE_IDENTIFIER = 'olm.tag.relatedImage.'
    NO_UPGRADE_LIST = ['3.1.1']

    def __init__(self, csv, name=None, target_version=None, replaces=None, skiprange=None, logger=None):
        self.original_csv = csv
        self.csv = copy.deepcopy(self.original_csv)

        self.original_operator_images    = []
        self.operator_images             = []
        self.annotation_related_images   = []
        self.spec_related_images         = []
        self.init_container_images       = []

        # Holds the version information
        self.version = ''
        self.major_minor = ''
        self.major_minor_patch = ''
        self.versioned_name = ''
        self.replaces = None
        self.skiprange = None
        self.hidden_crds = []

        # If name is not provided, we can try extrapolate it
        if name:
            self.name = name
        else:
            self.name = self.csv['metadata']['name'].split('.')[0]

        # Get only X.Y.Z from target version
        if target_version:
            self.major_minor_patch = target_version.split('-')[0]

        # Only add replaces and skiprange if given and version allows for upgrades
        if replaces and self.major_minor_patch not in self.NO_UPGRADE_LIST:
            self.replaces = replaces

        if skiprange and self.major_minor_patch not in self.NO_UPGRADE_LIST:
            self.skiprange = skiprange

        if target_version:
            self.set_version(target_version)

        if logger:
            self.log = logger
        else:
            self._setup_basic_logger()

        # Extract some other useful info
        self._get_hidden_crds()
        self._manipulate_tag_images()
        self._get_operator_images()
        self._get_related_images()
        self._get_init_container_images()

    def set_deployments_annotations(self, key=None, value=None):
        """Set key with value passed in for each deployment in the CSV

        :param key: Key being search for in deployment annotations
        :type key: string

        :param value: Value that will be assigned to the key passed in
        :type value: string
        """
        for d in self.csv['spec']['install']['spec']['deployments']:
            if not 'annotations' in d['spec']['template']['metadata']:
                continue
            d['spec']['template']['metadata']['annotations'][key] = value

    def set_container_image_annotation(self, image):
        """ Set metadata.annotations.containerImage with Image.image passed in

        :param image: Image that will be assigned to metadata.annotations.containerImage
        :type image: Image
        """
        self.csv['metadata']['annotations']['containerImage'] = image.image

    def set_version(self, version):
        """Set the target version for the CSV

        :param version: Target version in semver format X.Y.Z with optional -nnnn for pre-release
        :type version: string
        """
        self.version = version
        self.versioned_name = '{}.v{}'.format(self.name, self.version)
        self._update_version_references()

    def set_replaces(self, replaces):
        """ Set the release that this replaces

        :param replaces: The versioned name of the csv that this csv replaces
        :type replaces: string
        """
        self.replaces = replaces
        self.csv['spec']['replaces'] = self.replaces

    def set_image_pullsecret(self, name):
        """ Set the image pull secret for all operator deployment deployments. Overwrites any existing pull secret

        :param name: String or list of strings containing name of the pull secret to add
        :type name: string, list
        """
        if isinstance(name, str):
            p = [{'name': name}]
        else:
            p = [ {'name': x} for x in name ]

        for d in self.csv['spec']['install']['spec']['deployments']:
            d['spec']['template']['spec']['imagePullSecrets'] = p

    def add_image_pullsecret(self, name):
        """ Add image pull secret for all operator deployment deployments. Existing pull secrets will be kept

        :param name: String or list of strings containing name of the pull secret to add
        :type name: string, list
        """
        if isinstance(name, str):
            p = [{'name': name}]
        else:
            p = [ {'name': x} for x in name ]

        for d in self.csv['spec']['install']['spec']['deployments']:
            if not 'imagePullSecrets' in d['spec']['template']['spec']:
                # If imagepullsecret is missing, set it
                d['spec']['template']['spec']['imagePullSecrets'] = p
            else:
                # If imagepullsecret exists, add to the list
                if not(all(x in p for x in d['spec']['template']['spec']['imagePullSecrets'])):
                    try:
                        d['spec']['template']['spec']['imagePullSecrets'].extend(p)
                    except TypeError:
                        print('imagePullSecrets is not of type list')

    def generate_spec_relatedImages(self):
        """ Generates spec.relatedImages based on information found in operator deployment annotations marked with 'olm.relatedImage.*'
        """
        self.spec_related_images=self.annotation_related_images
        if 'relatedImages' in self.csv['spec']:
            self.log.debug('Resetting existing spec.relatedImages')
        self.csv['spec']['relatedImages'] = []

        # Hold dict of all names and images so we can find conflicting information
        images_validation = {}
        for r in self.spec_related_images:
            if r.name in images_validation:
                self.log.debug('found previous entry for {}'.format(r.name))
                if r.image != images_validation[r.name]:
                    self.log.warning('Validation error: Found different values for {}: {} and {}'.format(r.name, r.image, images_validation[r.name]))
                    self.log.debug('overwriting')
                    self.csv['spec']['relatedImages'][r.name] = r.image
                    continue
            if r.full_image:
                self.csv['spec']['relatedImages'].append({
                    'name':     r.name,
                    'image':    r.full_image
                })
            else:
                self.csv['spec']['relatedImages'].append({
                    'name':     r.name,
                    'image':    r.image
                })

    def get_owned_crds(self):
        """ Returns a list of owned CustomResourceDefinitions

        :return: List of owned custom resource definitions as dict object
        :rtype: list
        """
        return self.csv['spec']['customresourcedefinitions']['owned']

    def get_updated_csv(self):
        """ Returns the updated CSV object

        :return: CSV with updated version and image information
        :rtype: dict
        """
        # Merge in the updates that are done to Operatorimages and Operandimages
        self._update_operator_container_images()
        self._update_operand_images()
        self._update_init_container_images()

        return self.csv

    def get_formatted_csv(self):
        """ Returns a stringified save ready formatted ClusterServiceVersion
            This allows maintaining the format of the `alm-examples: |-` block
        """
        yaml.add_representer(_literal, _literal_presenter)
        formatted_csv = self.get_updated_csv()
        formatted_csv['metadata']['annotations']['alm-examples'] = _literal(formatted_csv['metadata']['annotations']['alm-examples'])
        return yaml.dump(formatted_csv, default_flow_style=False)

    def get_replaces(self):
        """ Return String

        :return: Returns the csv file name with previous version
        :rtype: string
        """
        return self.csv['spec']['replaces']

    def get_operator_images(self):
        """ Return a list of images used for operator deployment

        :return: Returns a List of Images as defined in Images class
        :rtype: list
        """
        return self.operator_images

    def get_annotation_related_images(self):
        """ Return a list of images found in 'olm.relatedImages.*' deployment annotations

        :return: Returns a List of Images as defined in Images class
        :rtype: list
        """
        return self.annotation_related_images

    def get_init_container_images(self):
        """ Return a list of images used for init containers

        :return: Returns a List of Images as defined in Images class
        :rtype: list
        """
        return self.init_container_images 

    def get_operator_deployments(self, api_version='apps/v1', kind='Deployment'):
        """ Return a list of kubernetes deployment objects constructed from the CSV deployments section

        :return: List of kubernetes deployment objects
        :rtype: list
        """
        # Extract the deployment(s)
        deployments = []
        for d in self.csv['spec']['install']['spec']['deployments']:
            deployments.append(copy.deepcopy(d))

        # Adjust the dict to make it valid deployment object
        for d in deployments:
            d.update({"apiVersion": api_version, "kind": kind})
            d['metadata'] = {
                'name': d['name']
                }
            del(d['name'])

        return deployments

    def _update_version_references(self):
        """ Update the version specifc fields based on self.version
        """
        self.csv['spec']['version'] = self.version
        self.csv['metadata']['name'] = self.versioned_name
        if len(self.versioned_name) > 63:
            if hasattr(self, 'log'):
                # Fixing a weird issue where the logger is not available when we are constructing a csv object. I even tried switching the
                # order of parameters when creating the csv object in create-release.py
                self.log.warning('{} is longer than 63 characters, and may lead to problems'.format(self.name))
        if self.skiprange:
            self.csv['metadata']['annotations']['olm.skipRange'] = self.skiprange
        if self.replaces:
            self.csv['spec']['replaces'] = self.replaces
        else:
            if 'replaces' in self.csv['spec']:
                del(self.csv['spec']['replaces'])

    def _get_operator_images(self):
        """[Populate a list of all images that are used for the operator deployment]
        """
        for d in self.csv['spec']['install']['spec']['deployments']:
            for c in d['spec']['template']['spec']['containers']:
                o = Image(
                    deployment = d['name'],
                    container  = c['name'],
                    image      = c['image']
                )
                self.original_operator_images.append(o)
                self.operator_images.append(o)

    def _get_related_images(self):
        # Capture related images from annotations
        for d in self.csv['spec']['install']['spec']['deployments']:
            if not 'annotations' in d['spec']['template']['metadata']:
                continue
            for a in d['spec']['template']['metadata']['annotations']:
                if a.startswith(self.RELATED_IMAGE_IDENTIFIER):
                    o = Image(
                        deployment  = d['name'],
                        name        = a.replace(self.RELATED_IMAGE_IDENTIFIER, ''),
                        image       = d['spec']['template']['metadata']['annotations'][a]
                    )
                    self.annotation_related_images.append(o)

    def _get_init_container_images(self):
        """[Populate a list of all images that are used for the init containers]
        """
        for d in self.csv['spec']['install']['spec']['deployments']:
            if 'initContainers' in d['spec']['template']['spec']:
                for c in d['spec']['template']['spec']['initContainers']:
                    o = Image(
                        deployment = d['name'],
                        container  = c['name'], 
                        image      = c['image']
                    )
                    self.init_container_images.append(o)

    def _manipulate_tag_images(self):
        taggedImages = {}
        for d in self.csv['spec']['install']['spec']['deployments']:
            if not 'annotations' in d['spec']['template']['metadata']:
                continue
            for a in d['spec']['template']['metadata']['annotations']:
                related_image_annotation = a.replace(self.TAGGED_RELATED_IMAGE_IDENTIFIER, self.RELATED_IMAGE_IDENTIFIER)
                # olm.relatedImage should take precedence over olm.tag.relatedImage so do not overwrite olm.relatedImage
                if a.startswith(self.TAGGED_RELATED_IMAGE_IDENTIFIER) and not related_image_annotation in d['spec']['template']['metadata']['annotations']:
                        taggedImages[related_image_annotation] = d['spec']['template']['metadata']['annotations'][a]
        for d in self.csv['spec']['install']['spec']['deployments']:
            if not 'annotations' in d['spec']['template']['metadata']:
                continue
            for i in taggedImages:
                d['spec']['template']['metadata']['annotations'][i] = taggedImages[i]

    def _update_operator_container_images(self):
        for image in self.operator_images:
            for d in self.csv['spec']['install']['spec']['deployments']:
                if d['name'] == image.deployment:
                    for c in d['spec']['template']['spec']['containers']:
                        if c['name'] == image.container:
                            c['image'] = image.image

    def _update_init_container_images(self):
        for image in self.init_container_images:
            for d in self.csv['spec']['install']['spec']['deployments']:
                if d['name'] == image.deployment:
                    for c in d['spec']['template']['spec']['initContainers']:
                        if c['name'] == image.container:
                            c['image'] = image.image

    def _update_operand_images(self):
        # Update the annotations that has been updated
        for image in self.annotation_related_images:
            for d in self.csv['spec']['install']['spec']['deployments']:
                if d['name'] == image.deployment:
                    if image.full_image:
                        d['spec']['template']['metadata']['annotations'][self.RELATED_IMAGE_IDENTIFIER + image.name] = image.full_image
                    else:
                        d['spec']['template']['metadata']['annotations'][self.RELATED_IMAGE_IDENTIFIER + image.name] = image.image

    def _setup_basic_logger(self):
        # Setup logging to stdout if we're not provided a logger
        self.log = logging.getLogger(__name__)
        out_hdlr = logging.StreamHandler(sys.stdout)
        out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S'))
        out_hdlr.setLevel(logging.INFO)
        self.log.addHandler(out_hdlr)
        self.log.setLevel(logging.INFO)

    def _get_hidden_crds(self):
        try:
            self.hidden_crds = ast.literal_eval(self.csv['metadata']['annotations']['operators.operatorframework.io/internal-objects'])
        except:
            self.hidden_crds = []
            
    def get_hidden_crds(self):
        return self.hidden_crds