from loguru import logger
import torch
from torchvision.models.feature_extraction import create_feature_extractor
from torchvision.models import wide_resnet50_2, resnet18
from .auto_encoder import ConvAutoEncoder


def build_feature_extractor(type, ae_cfg=None):
    logger.info(f'use feature extractor: {type}')
    if ae_cfg['use_ae']:
        model = ConvAutoEncoder(encoder_name=type)
        return_nodes={'encoder.layer1': 'feat1',
                      'encoder.layer2': 'feat2',
                      'encoder.layer3': 'feat3'}
        model.load_state_dict(torch.load(ae_cfg['weights']))
        logger.info(f'feature extractor {type} is fine tune by autoencoder!')
    else:
        if type == 'wrn50_2':
            model = wide_resnet50_2(pretrained=True, progress=True)
            return_nodes = {'layer1': 'feat1',
                            'layer2': 'feat2',
                            'layer3': 'feat3'}
        elif type == 'res18':
            model = resnet18(pretrained=True, progress=True)
            return_nodes = {'layer1': 'feat1',
                            'layer2': 'feat2',
                            'layer3': 'feat3'}
        else:
            raise NotImplementedError("not found feature extractor")

    feature_extractor = create_feature_extractor(model=model, return_nodes=return_nodes)

    return feature_extractor