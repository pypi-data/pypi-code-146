import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from tepe.tasks.rd.resnet import wide_resnet50_2, wide_resnet101_2
from tepe.tasks.rd.de_resnet import de_wide_resnet50_2, de_wide_resnet101_2


class Model(nn.Module):
    def __init__(self, encoder_name, input_size=(256, 256)):
        super().__init__()
        if encoder_name == 'wres50':
            self.encoder, self.bn = wide_resnet50_2(pretrained=True)
            self.decoder = de_wide_resnet50_2(pretrained=False)
        elif encoder_name == 'wres101':
            self.encoder, self.bn = wide_resnet101_2(pretrained=True)
            self.decoder = de_wide_resnet101_2(pretrained=False)
        else:
            raise NotImplementedError

        # loss
        # self.mse_loss = torch.nn.MSELoss()
        self.cos_loss = nn.CosineSimilarity()

        self.input_size = input_size
        self.export = False

    def forward(self, x):
        x1 = self.encoder(x)
        x2 = self.decoder(self.bn(x1))

        if self.training:
            return self.loss_function(x1, x2)
        else:
            return self.cal_anomaly_map(x1, x2, amap_mode='add')

    def loss_function(self, a, b):
        loss = 0
        for item in range(len(a)):
            # loss += 0.1*self.mse_loss(a[item], b[item])
            loss += torch.mean(1 - self.cos_loss(a[item].view(a[item].shape[0], -1),
                                                 b[item].view(b[item].shape[0], -1)))
        return loss

    def cal_anomaly_map(self, fs_list, ft_list, amap_mode='add'):
        '''
        fs_list: sdudent model feature
        ft_list: teacher model feature
        '''
        a_map_list = []
        # max_shape = [64, 64]
        for item in range(len(ft_list)):
            # if item == 0:
            #     max_shape = [4 * int(fs_list[item].shape[2]), 4 * int(fs_list[item].shape[3])]
            # a_map = 1 - self.cos_loss(fs_list[item], ft_list[item]) # [1,16,16]
            # onnx don't support nn.CosineSimilarity
            a_map = 1 - cosine_similarity(fs_list[item], ft_list[item])
            a_map = torch.unsqueeze(a_map, dim=1)#[1,1,16,16]
            a_map = F.interpolate(a_map, size=self.input_size, mode='bilinear', align_corners=False)
            a_map_list.append(a_map)

        a_maps = torch.cat(a_map_list, dim=1)  # [B,3,256,256]
        anomaly_map = torch.sum(a_maps, dim=1)  # [B,256,256]

        return anomaly_map


def cosine_similarity(a: torch.Tensor, b: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
    frac1 = torch.sum(torch.mul(a, b), dim=1)
    a_norm = torch.norm(a, p=2, dim=1)
    b_norm = torch.norm(b, p=2, dim=1)
    frac2 = torch.mul(a_norm, b_norm)
    frac2[frac2 < eps] = eps
    sim = frac1 / frac2

    return sim