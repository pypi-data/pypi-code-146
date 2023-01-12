from collections import OrderedDict

import torch
from torch import nn


class Cat(nn.Module):
    """Cat. Concatenation module"""

    def __init__(
        self, dimension: int = 1, parent: list = [], childs: list = [], id: int = 0
    ) -> None:
        """__init__.

        :param dimension:
        :type dimension: int
        :param parent:
        :type parent: list
        :param childs:
        :type childs: list
        :param id:
        :type id: int
        :rtype: None
        """
        super(Cat, self).__init__()
        self.dimension = dimension
        self.parent = parent
        self.id = id
        self.childs = childs

    def forward(self, matrix: torch.FloatTensor) -> torch.FloatTensor:
        """forward.

        :param matrix:
        :type matrix: torch.FloatTensor
        :rtype: torch.FloatTensor
        """
        return torch.cat(matrix, self.dimension)


class Conv(nn.Sequential):
    """Conv. Convolution module"""

    def __init__(
        self,
        ci: int,
        co: int,
        kernel: int = 1,
        stride: int = 1,
        parent: list = [],
        childs: list = [],
        id: int = 0,
    ) -> None:
        """__init__.

        :param ci:
        :type ci: int
        :param co:
        :type co: int
        :param kernel:
        :type kernel: int
        :param stride:
        :type stride: int
        :param parent:
        :type parent: list
        :param childs:
        :type childs: list
        :param id:
        :type id: int
        :rtype: None
        """
        self.parent = parent
        self.id = id
        self.childs = childs
        nn.Sequential.__init__(
            self,
            OrderedDict(
                [
                    (
                        "conv",
                        nn.Conv2d(
                            ci,
                            co,
                            kernel,
                            stride,
                            autopad(kernel),
                            groups=1,
                            bias=False,
                        ),
                    ),
                    ("bn", nn.BatchNorm2d(co, eps=0.001, momentum=0.03)),
                    ("act", nn.SiLU()),
                ]
            ),
        )


def autopad(k: int) -> int:
    """autopad.

    :param k:
    :type k: int
    :rtype: int
    """
    p = k // 2 if isinstance(k, int) else [x // 2 for x in k]
    return p


class SPPCSPC(nn.Module):
    """SPPCSPC. CrossStagePartialNetworks module"""

    def __init__(
        self,
        ci: int,
        co: int,
        n: int = 1,
        e: float = 0.5,
        kernels: (int, int, int) = (5, 9, 13),
        parent: list = [],
        childs: list = [],
        id: int = 0,
    ) -> None:
        """__init__.

        :param ci:
        :type ci: int
        :param co:
        :type co: int
        :param n:
        :type n: int
        :param e:
        :type e: float
        :param kernels:
        :type kernels: (int, int, int)
        :param parent:
        :type parent: list
        :param childs:
        :type childs: list
        :param id:
        :type id: int
        :rtype: None
        """
        super(SPPCSPC, self).__init__()
        self.parent = parent
        self.childs = childs
        self.id = id
        c_ = int(2 * co * e)  # hidden channels
        self.cv1 = Conv(ci, c_, 1, 1)
        self.cv2 = Conv(ci, c_, 1, 1)
        self.cv3 = Conv(c_, c_, 3, 1)
        self.cv4 = Conv(c_, c_, 1, 1)
        self.module = nn.ModuleList(
            [nn.MaxPool2d(kernel_size=x, stride=1, padding=x // 2) for x in kernels]
        )
        self.cv5 = Conv(4 * c_, c_, 1, 1)
        self.cv6 = Conv(c_, c_, 3, 1)
        self.cv7 = Conv(2 * c_, co, 1, 1)

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        """forward.

        :param x:
        :type x: torch.FloatTensor
        :rtype: torch.FloatTensor
        """
        x1 = self.cv4(self.cv3(self.cv1(x)))
        y1 = self.cv6(self.cv5(torch.cat([x1] + [m(x1) for m in self.module], 1)))
        y2 = self.cv2(x)
        return self.cv7(torch.cat((y1, y2), dim=1))


class RepConv(nn.Module):
    """RepConv. Represented convolution module"""

    def __init__(
        self,
        ci: int,
        co: int,
        kernel: int = 3,
        stride: int = 1,
        g: int = 1,
        parent: list = [],
        childs: list = [],
        id: int = 0,
    ) -> None:
        """__init__.

        :param ci:
        :type ci: int
        :param co:
        :type co: int
        :param kernel:
        :type kernel: int
        :param stride:
        :type stride: int
        :param g:
        :type g: int
        :param parent:
        :type parent: list
        :param childs:
        :type childs: list
        :param id:
        :type id: int
        :rtype: None
        """
        super(RepConv, self).__init__()
        self.parent = parent
        self.id = id
        self.childs = childs
        self.groups = g
        self.in_channels = ci
        self.out_channels = co

        padding_11 = autopad(kernel) - kernel // 2

        self.act = nn.SiLU()

        self.rbr_identity = (
            nn.BatchNorm2d(num_features=self.in_channels, eps=0.001, momentum=0.03)
            if self.out_channels == self.in_channels and stride == 1
            else None
        )

        self.rbr_dense = nn.Sequential(
            nn.Conv2d(
                self.in_channels,
                self.out_channels,
                kernel,
                stride,
                autopad(kernel),
                groups=g,
                bias=False,
            ),
            nn.BatchNorm2d(num_features=self.out_channels, eps=0.001, momentum=0.03),
        )

        self.rbr_1x1 = nn.Sequential(
            nn.Conv2d(
                self.in_channels,
                self.out_channels,
                1,
                stride,
                padding_11,
                groups=g,
                bias=False,
            ),
            nn.BatchNorm2d(num_features=self.out_channels, eps=0.001, momentum=0.03),
        )

    def forward(self, inputs: torch.FloatTensor) -> torch.FloatTensor:
        """forward.

        :param inputs:
        :type inputs: torch.FloatTensor
        :rtype: torch.FloatTensor
        """
        if self.rbr_identity is None:
            id_out = 0
        else:
            id_out = self.rbr_identity(inputs)

        return self.act(self.rbr_dense(inputs) + self.rbr_1x1(inputs) + id_out)


class ImplicitA(nn.Module):
    """ImplicitA. Addition module"""

    def __init__(self, channel: int, mean: float = 0.0, std: float = 0.02) -> None:
        """__init__.

        :param channel:
        :type channel: int
        :param mean:
        :type mean: float
        :param std:
        :type std: float
        :rtype: None
        """
        super(ImplicitA, self).__init__()
        self.channel = channel
        self.mean = mean
        self.std = std
        self.implicit = nn.Parameter(torch.zeros(1, channel, 1, 1))
        nn.init.normal_(self.implicit, mean=self.mean, std=self.std)

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        """forward.

        :param x:
        :type x: torch.FloatTensor
        :rtype: torch.FloatTensor
        """
        return self.implicit + x


class ImplicitM(nn.Module):
    """ImplicitM. Multiplication module"""

    def __init__(self, channel: int, mean: float = 1.0, std: float = 0.02) -> None:
        """__init__.

        :param channel:
        :type channel: int
        :param mean:
        :type mean: float
        :param std:
        :type std: float
        :rtype: None
        """
        super(ImplicitM, self).__init__()
        self.channel = channel
        self.mean = mean
        self.std = std
        self.implicit = nn.Parameter(torch.ones(1, channel, 1, 1))
        nn.init.normal_(self.implicit, mean=self.mean, std=self.std)

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        """forward.

        :param x:
        :type x: torch.FloatTensor
        :rtype: torch.FloatTensor
        """
        return self.implicit * x


class Detect(nn.Module):
    """Detect."""

    def __init__(
        self,
        nc: int = 80,
        anchors: torch.FloatTensor = (),
        ch: list = (),
        parent: list = [],
        childs: list = [],
        id: int = 0,
        stride: torch.FloatTensor = None,
    ) -> None:
        """__init__.

        :param nc:
        :type nc: int
        :param anchors:
        :type anchors: torch.FloatTensor
        :param ch:
        :type ch: list
        :param parent:
        :type parent: list
        :param childs:
        :type childs: list
        :param id:
        :type id: int
        :param stride:
        :type stride: torch.FloatTensor
        :rtype: None
        """
        super(Detect, self).__init__()
        self.parent = parent
        self.stride = stride
        self.id = id
        self.childs = childs
        self.nc = nc
        self.no = nc + 5
        self.nl = anchors.shape[0]
        self.na = anchors.shape[1]
        self.grid = [torch.zeros(1)] * self.nl
        a = anchors
        self.register_buffer("anchors", a)
        self.register_buffer("anchor_grid", a.clone().view(self.nl, 1, -1, 1, 1, 2))
        self.m = nn.ModuleList(nn.Conv2d(x, self.no * self.na, 1) for x in ch)

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        """forward.

        :param x:
        :type x: torch.FloatTensor
        :rtype: torch.FloatTensor
        """
        z = []
        for i in range(self.nl):
            x[i] = self.m[i](x[i])
            bs, _, ny, nx = x[i].shape
            x[i] = (
                x[i]
                .view(bs, self.na, self.no, ny, nx)
                .permute(0, 1, 3, 4, 2)
                .contiguous()
            )

            if not self.training:
                if self.grid[i].shape[2:4] != x[i].shape[2:4]:
                    self.grid[i] = self._make_grid(nx, ny).to(x[i].device)
                y = x[i].sigmoid()
                y[..., 0:2] = (y[..., 0:2] * 2.0 - 0.5 + self.grid[i]) * self.stride[i]
                y[..., 2:4] = (y[..., 2:4] * 2) ** 2 * self.anchor_grid[i]
                z.append(y.view(bs, -1, self.no))

        if self.training:
            out = x
        else:
            out = (torch.cat(z, 1), x)

        return out

    @staticmethod
    def _make_grid(nx: int = 20, ny: int = 20) -> torch.FloatTensor:
        """_make_grid.

        :param nx:
        :type nx: int
        :param ny:
        :type ny: int
        :rtype: torch.FloatTensor
        """
        yv, xv = torch.meshgrid([torch.arange(ny), torch.arange(nx)])
        return torch.stack((xv, yv), 2).view((1, 1, ny, nx, 2)).float()
