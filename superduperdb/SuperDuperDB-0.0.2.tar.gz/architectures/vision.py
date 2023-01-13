import math
from torchvision import models as visionmodels

from torchvision import transforms
from torchvision.transforms.functional import pad
from torch import nn


class CNN:
    def __init__(self, width=224, height=224):
        resnet = visionmodels.resnet50(pretrained=True)
        modules = list(resnet.children())[:-1]
        self.resnet = nn.Sequential(*modules)

        self.normalize_values = \
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        self.width = width
        self.height = height
        self.to_tensor = transforms.ToTensor()

    def normalize_size(self, image):
        width_ratio = self.width / image.width
        height_ratio = self.height / image.height
        ratio = min(width_ratio, height_ratio)
        image = image.resize((math.floor(ratio * image.width), math.floor(ratio * image.height)))

        p_top = math.floor((self.height - image.height) / 2)
        p_bottom = math.ceil((self.height - image.height) / 2)
        p_left = math.floor((self.width - image.width) / 2)
        p_right = math.ceil((self.width - image.width) / 2)
        image = pad(image,
                    [p_left, p_top, p_right, p_bottom],
                    fill=0,
                    padding_mode='edge')
        return image

    def forward(self, x):
        return self.resnet(x)[:, :, 0, 0]

    def eval(self):
        self.resnet.eval()

    def preprocess(self, image):
        image = image.convert("RGB")
        image = self.normalize_size(image)
        image = self.to_tensor(image)
        return self.normalize_values(image)