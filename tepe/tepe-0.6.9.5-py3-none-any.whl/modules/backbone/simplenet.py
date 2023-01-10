import torch
import torch.nn as nn


class Unit(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(Unit, self).__init__()

        self.conv = nn.Conv2d(in_channels=in_channels, kernel_size=(3, 3),
                              out_channels=out_channels, stride=1, padding=1)
        self.bn = nn.BatchNorm2d(num_features=out_channels)
        self.relu = nn.ReLU()

    def forward(self, input):
        output = self.conv(input)
        output = self.bn(output)
        output = self.relu(output)

        return output


class SimpleNet(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleNet, self).__init__()
        # stride: 16

        # Create 14 layers of the unit with max pooling in between
        self.unit1 = Unit(in_channels=3, out_channels=16)
        self.unit2 = Unit(in_channels=16, out_channels=16)
        self.pool1 = nn.MaxPool2d(kernel_size=2)

        self.unit4 = Unit(in_channels=16, out_channels=32)
        self.pool2 = nn.MaxPool2d(kernel_size=2)

        self.unit8 = Unit(in_channels=32, out_channels=64)
        self.pool3 = nn.MaxPool2d(kernel_size=2)

        self.unit12 = Unit(in_channels=64, out_channels=128)
        self.avgpool = nn.AvgPool2d(kernel_size=2)

        # Add all the units into the Sequential layer in exact order
        self.net = nn.Sequential(
            self.unit1, self.unit2, self.pool1,
            self.unit4, self.pool2,
            self.unit8, self.pool3,
            self.unit12, self.avgpool)
        self.conv1x1 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=512, kernel_size=(1, 1)),
            nn.BatchNorm2d(num_features=512),
            nn.ReLU()
        )
        self.globalpool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Linear(in_features=512, out_features=num_classes)

    def forward(self, x):
        x = self.net(x)
        x = self.conv1x1(x)
        x = self.globalpool(x)
        x = x.view(-1, 512)

        output = self.fc(x)
        return output


class SimpleNetM(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleNetM, self).__init__()
        # stride: 16

        # Create 14 layers of the unit with max pooling in between
        self.unit1 = Unit(in_channels=3, out_channels=16)
        self.unit2 = Unit(in_channels=16, out_channels=16)

        self.pool1 = nn.MaxPool2d(kernel_size=2)

        self.unit4 = Unit(in_channels=16, out_channels=32)
        self.unit5 = Unit(in_channels=32, out_channels=32)

        self.pool2 = nn.MaxPool2d(kernel_size=2)

        self.unit8 = Unit(in_channels=32, out_channels=64)
        self.unit9 = Unit(in_channels=64, out_channels=64)

        self.pool3 = nn.MaxPool2d(kernel_size=2)

        self.unit12 = Unit(in_channels=64, out_channels=128)
        self.unit13 = Unit(in_channels=128, out_channels=128)

        self.avgpool = nn.AvgPool2d(kernel_size=2)

        # Add all the units into the Sequential layer in exact order
        self.net = nn.Sequential(
            self.unit1, self.unit2, self.pool1,
            self.unit4, self.unit5, self.pool2,
            self.unit8, self.unit9, self.pool3,
            self.unit12, self.unit13, self.avgpool)
        self.conv1x1 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=512, kernel_size=(1, 1)),
            nn.BatchNorm2d(num_features=512),
            nn.ReLU()
        )
        self.globalpool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Linear(in_features=512, out_features=num_classes)

    def forward(self, x):
        x = self.net(x)
        x = self.conv1x1(x)
        x = self.globalpool(x)
        x = x.view(-1, 512)
        output = self.fc(x)
        return output


class SimpleNetL(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleNetL, self).__init__()
        # stride: 16

        # Create 14 layers of the unit with max pooling in between
        self.unit1 = Unit(in_channels=3, out_channels=16)
        self.unit2 = Unit(in_channels=16, out_channels=16)
        self.unit3 = Unit(in_channels=16, out_channels=16)

        self.pool1 = nn.MaxPool2d(kernel_size=2)

        self.unit4 = Unit(in_channels=16, out_channels=32)
        self.unit5 = Unit(in_channels=32, out_channels=32)
        self.unit6 = Unit(in_channels=32, out_channels=32)
        self.unit7 = Unit(in_channels=32, out_channels=32)

        self.pool2 = nn.MaxPool2d(kernel_size=2)

        self.unit8 = Unit(in_channels=32, out_channels=64)
        self.unit9 = Unit(in_channels=64, out_channels=64)
        self.unit10 = Unit(in_channels=64, out_channels=64)
        self.unit11 = Unit(in_channels=64, out_channels=64)

        self.pool3 = nn.MaxPool2d(kernel_size=2)

        self.unit12 = Unit(in_channels=64, out_channels=128)
        self.unit13 = Unit(in_channels=128, out_channels=128)
        self.unit14 = Unit(in_channels=128, out_channels=128)

        self.avgpool = nn.AvgPool2d(kernel_size=2)

        # Add all the units into the Sequential layer in exact order
        self.net = nn.Sequential(
            self.unit1, self.unit2, self.unit3, self.pool1,
            self.unit4, self.unit5, self.unit6, self.unit7, self.pool2,
            self.unit8, self.unit9, self.unit10, self.unit11, self.pool3,
            self.unit12, self.unit13, self.unit14, self.avgpool
        )
        self.conv1x1 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=512, kernel_size=(1, 1)),
            nn.BatchNorm2d(num_features=512),
            nn.ReLU()
        )
        self.globalpool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Linear(in_features=512, out_features=num_classes)

    def forward(self, x):
        x = self.net(x)
        x = self.conv1x1(x)
        x = self.globalpool(x)
        x = x.view(-1, 512)
        output = self.fc(x)
        return output