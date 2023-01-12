import numpy as np

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from tqdm import tqdm

from torchvision.models import wide_resnet50_2, resnet50
from torchvision.models.feature_extraction import create_feature_extractor

from tepe.tasks.cfa import CFAConfig


class ConvAutoEncoder(nn.Module):
    def __init__(
            self,
            encoder_name='wrn50_2',

    ):
        super().__init__()
        if encoder_name == 'wrn50_2':
            backbone = wide_resnet50_2(pretrained=True)
        else:
            backbone = resnet50(pretrained=True)
        self.encoder = create_feature_extractor(
            backbone,
            ['layer3']
        )

        self.decoder = nn.Sequential(
            Up(1024, 512),
            Up(512, 256),
            Up(256, 128),
            Up(128, 64),
        )
        self.outlayer = nn.Sequential(
            nn.Conv2d(64, 3, kernel_size=1),
        )

    def forward(self, x):
        x = self.encoder(x)['layer3']
        x = self.decoder(x)
        x = self.outlayer(x)
        return x


class Up(nn.Module):
    """Upscaling then double conv"""

    def __init__(self, in_channels, out_channels, bilinear=True):
        super().__init__()

        # if bilinear, use the normal convolutions to reduce the number of channels
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
            self.conv = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True),
                nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True),
            )
        else:
            self.up = nn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)
            self.conv = nn.Sequential(
                nn.Conv2d(in_channels // 2, out_channels, kernel_size=3, padding=1, bias=False),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True),
                nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True),
            )

    def forward(self, x):
        return self.conv(self.up(x))


def train(task, encoder_name='wrn50_2', wights_path='convae.pth', resume=False):

    if resume:
        model = torch.load(wights_path)
    else:
        model = ConvAutoEncoder(encoder_name=encoder_name)
    print('get model')

    # specify loss function
    criterion = nn.MSELoss()

    # specify loss function
    for param in model.encoder.parameters():
        param.requires_grad = False
    params = filter(lambda p: p.requires_grad, model.parameters())
    optimizer = torch.optim.Adam(params, lr=0.002)

    # number of epochs to train the model
    n_epochs = 120

    train_loader = task.get_train_loader()

    print('start training')
    model.train()
    model.to('cuda')
    for epoch in range(1, n_epochs+1):
        # monitor training loss
        train_loss = 0.0

        # freeze encoder
        if epoch == 40:
            print('============add encoder params')
            for param in model.encoder.parameters():
                param.requires_grad = True
            optimizer.add_param_group(
                {"params": model.encoder.parameters(),
                 "lr": 1e-5,
                 "weight_decay": 5e-4}
            )

        for data in tqdm(train_loader):
            images, _, _ = data
            images = images.cuda()
            # clear the gradients of all optimized variables
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, images)
            # backward pass: compute gradient of the loss with respect to model parameters
            loss.backward()
            # perform a single optimization step (parameter update)
            optimizer.step()
            train_loss += loss.item()

        # print avg training statistics
        train_loss = train_loss/len(train_loader)
        print('Epoch: {} \tTraining Loss: {:.6f}'.format(
            epoch,
            train_loss
        ))

        torch.save(model, wights_path)
    print('model save in ', wights_path)


def imshow(ax, img):
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img = (((img.transpose(1, 2, 0) * std) + mean) * 255.).astype(np.uint8)
    ax.imshow(img)


def test():
    task = CFAConfig()
    task.data_root = '/home/zepei/DATA/yiwushuju/image'
    task.scene = 'eguo'
    task.keep_ratio = False
    task.batch_size = 5
    test_loader = task.get_train_loader()

    #Batch of test images
    dataiter = iter(test_loader)
    images, _, _ = dataiter.next()

    model = ConvAutoEncoder()
    ckpt = torch.load('ae_wo_sigmoid_s.pth')
    model.load_state_dict(ckpt)

    model.cuda().eval()
    #Sample outputs
    with torch.no_grad():
        output = model(images.cuda())

    images = images.numpy()
    output = output.cpu().detach().numpy()

    #Original Images
    fig = plt.figure(figsize=(12,8))
    for idx in np.arange(5):
        ax = fig.add_subplot(2, 5, idx+1, xticks=[], yticks=[])
        ax.axis('off')
        imshow(ax, images[idx])
        ax.set_title('Original Images')

    #Reconstructed Images
    for idx in np.arange(5):
        ax = fig.add_subplot(2, 5, 5 + idx+1, xticks=[], yticks=[])
        ax.axis('off')
        imshow(ax, output[idx])
        ax.set_title('Reconstructed Images')
    fig.tight_layout()

    plt.show()
    fig.savefig('res3.jpg', dpi=100)


if __name__ == '__main__':
    resume = True
    checkpoint = 'assets/convae.pth'
    # train()
    test()