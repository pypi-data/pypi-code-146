
from typing import List, Union
from pathlib import Path
import torch
import numpy
from PIL import Image
from numpy import ndarray
from torch import Tensor
from torchvision import transforms
from iv.cirtorch.networks.imageretrievalnet import extract_vectors
from iv.cirtorch.networks.imageretrievalnet import init_network
from iv.cirtorch.networks.imageretrievalnet import ImageRetrievalNet

__version__ = '0.0.3'
VERSION = __version__


class ResNet:
    def __init__(self, weight_file: Union[Path, str]) -> None:
        if isinstance(weight_file, Path):
            weight_file = str(weight_file)

        state: dict = torch.load(weight_file)

        state['state_dict']['whiten.weight'] = state['state_dict']['whiten.weight'][0::4, ::]
        state['state_dict']['whiten.bias'] = state['state_dict']['whiten.bias'][0::4]

        net_params = {}
        net_params['architecture'] = state['meta']['architecture']
        net_params['pooling'] = state['meta']['pooling']
        net_params['local_whitening'] = state['meta'].get(
            'local_whitening', False)
        net_params['regional'] = state['meta'].get('regional', False)
        net_params['whitening'] = state['meta'].get('whitening', False)
        net_params['mean'] = state['meta']['mean']
        net_params['std'] = state['meta']['std']
        net_params['pretrained'] = False

        network: ImageRetrievalNet = init_network(net_params)

        network.load_state_dict(state['state_dict'])

        network.eval()

        _normalize = transforms.Normalize(
            mean=network.meta['mean'],
            std=network.meta['std']
        )
        transform = transforms.Compose([
            transforms.ToTensor(),
            _normalize
        ])

        self.network = network
        self.transform = transform

    def gen_vector(self, image: Union[Image.Image, ndarray, Path, str]) -> List[float]:
        if isinstance(image, Image.Image):
            image = image.convert('RGB')
            image = numpy.array(image)

        if isinstance(image, Path) or isinstance(image, str):
            _image = Image.open(str(image)).convert('RGB')
            image = numpy.array(_image)

        assert isinstance(image, ndarray)

        vecs: Tensor = extract_vectors(
            self.network, [image], 512, self.transform)

        vector: ndarray = vecs.detach().cpu().numpy().T

        return vector[0].tolist()


def l2(vector1: List[float], vector2: List[float]) -> float:
    vector1 = numpy.array(vector1)
    vector2 = numpy.array(vector2)
    return float(numpy.sqrt(numpy.sum(numpy.square(vector1 - vector2))))
