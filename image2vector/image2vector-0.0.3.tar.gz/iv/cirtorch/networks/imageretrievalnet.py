import os
import torch
import torch.nn as nn
import torchvision
from torch import Tensor
from torch.utils.data.dataloader import DataLoader
from iv.cirtorch.layers.pooling import MAC, SPoC, GeM, GeMmp, RMAC, Rpool
from iv.cirtorch.layers.normalization import L2N
from iv.cirtorch.datasets.genericdataset import ImagesFromList


# 可选全局池化层，每个都可以用于局部池化
POOLING = {
    'mac': MAC,
    'spoc': SPoC,
    'gem': GeM,
    'gemmp': GeMmp,
    'rmac': RMAC,
}


class ImageRetrievalNet(nn.Module):

    def __init__(self, features, lwhiten, pool, whiten, meta):
        super(ImageRetrievalNet, self).__init__()
        self.features = nn.Sequential(*features)
        self.lwhiten = lwhiten
        self.pool = pool
        self.whiten = whiten
        self.norm = L2N()
        self.meta = meta

    def forward(self, x: Tensor):
        o = self.features(x)

        # TODO: properly test (with pre-l2norm and/or post-l2norm)
        # 启用局部白化，则: features -> local whiten
        if self.lwhiten is not None:
            s = o.size()
            o = o.permute(0, 2, 3, 1).contiguous().view(-1, s[1])
            o = self.lwhiten(o)
            o = o.view(s[0], s[2], s[3],
                       self.lwhiten.out_features).permute(0, 3, 1, 2)

        # features -> pool -> norm
        o = self.norm(self.pool(o)).squeeze(-1).squeeze(-1)

        # 启用白化，则: pooled features -> whiten -> norm
        if self.whiten is not None:
            o = self.norm(self.whiten(o))

        # 使每个图像为Dx1列向量(如果有许多图像，则为DxN)
        return o.permute(1, 0)

    def __repr__(self):
        tmpstr = super(ImageRetrievalNet, self).__repr__()[:-1]
        tmpstr += self.meta_repr()
        tmpstr = tmpstr + ')'
        return tmpstr

    def meta_repr(self):
        # + self.meta.__repr__() + '\n'
        tmpstr = '  (' + 'meta' + '): dict( \n'
        tmpstr += '     architecture: {}\n'.format(self.meta['architecture'])
        tmpstr += '     local_whitening: {}\n'.format(
            self.meta['local_whitening'])
        tmpstr += '     pooling: {}\n'.format(self.meta['pooling'])
        tmpstr += '     regional: {}\n'.format(self.meta['regional'])
        tmpstr += '     whitening: {}\n'.format(self.meta['whitening'])
        tmpstr += '     outputdim: {}\n'.format(self.meta['outputdim'])
        tmpstr += '     mean: {}\n'.format(self.meta['mean'])
        tmpstr += '     std: {}\n'.format(self.meta['std'])
        tmpstr = tmpstr + '  )\n'
        return tmpstr


def init_network(params: dict):
    # 使用默认值解析参数
    architecture = params.get('architecture', 'resnet50')
    local_whitening = params.get('local_whitening', False)
    pooling = params.get('pooling', 'gem')
    regional = params.get('regional', False)
    whitening = params.get('whitening', False)
    mean = params.get('mean', [0.485, 0.456, 0.406])
    std = params.get('std', [0.229, 0.224, 0.225])
    pretrained = params.get('pretrained', False)

    dim = 512

    # 从torchvision加载网络
    net_in = getattr(torchvision.models, architecture)(pretrained=False)

    # 初始化特征
    # 只采用卷积的特性，总是以ReLU结束，使最后的激活非负
    if architecture.startswith('alexnet'):
        features = list(net_in.features.children())[:-1]
    elif architecture.startswith('vgg'):
        features = list(net_in.features.children())[:-1]
    elif architecture.startswith('resnet'):
        features = list(net_in.children())[:-2]
    elif architecture.startswith('densenet'):
        features = list(net_in.features.children())
        features.append(nn.ReLU(inplace=True))
    elif architecture.startswith('squeezenet'):
        features = list(net_in.features.children())
    else:
        raise ValueError(
            'Unsupported or unknown architecture: {}!'.format(architecture))

    # 初始化局部白化
    if local_whitening:
        lwhiten = nn.Linear(dim, dim, bias=True)  # 测试会减少维度
        nn.Linear()
    else:
        lwhiten = None

    # 初始化池化
    if pooling == 'gemmp':
        pool = POOLING[pooling](mp=dim)
    else:
        pool = POOLING[pooling]()

    # 初始化regional pooling
    if regional:
        rpool = pool
        rwhiten = nn.Linear(dim, dim, bias=True)
        pool = Rpool(rpool, rwhiten)

    # 初始化白化
    if whitening:
        # whiten = nn.Linear(dim, dim, bias=True)
        whiten = nn.Linear(2048, dim, bias=True)

    else:
        whiten = None

    # 创建存储在网络中的元信息
    meta = {
        'architecture': architecture,
        'local_whitening': local_whitening,
        'pooling': pooling,
        'regional': regional,
        'whitening': whitening,
        'mean': mean,
        'std': std,
        'outputdim': dim,
    }

    # 创建一个通用的图像检索网络
    net = ImageRetrievalNet(features, lwhiten, pool, whiten, meta)
    return net


def extract_vectors(net, images, image_size, transform, bbxs=None, ms=[1], msp=1, print_freq=10):

    detaset = ImagesFromList(
        images=images,
        imsize=image_size,
        bbxs=bbxs,
        transform=transform
    )

    loader = DataLoader(
        detaset,
        batch_size=1,
        shuffle=False,
        num_workers=0,
        pin_memory=False
    )

    # 提取向量
    # logger.debug("开始提取向量！")
    with torch.no_grad():
        vecs = torch.zeros(net.meta['outputdim'], len(images))
        for index, input in enumerate(loader):
            vecs[:, index] = extract_ss(net, input)
            
    return vecs


def extract_ss(net: ImageRetrievalNet, input: Tensor) -> Tensor:
    return net(input).cpu().data.squeeze()
