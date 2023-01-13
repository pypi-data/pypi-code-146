import torch


class BinaryClassifier(torch.nn.Module):
    def __init__(self, input_size, labels):
        super().__init__()
        self.linear = torch.nn.Linear(input_size, 1)
        self.labels = labels

    def preprocess(self, x):
        return x

    def forward(self, x):
        return self.linear(x)[:, 0]

    def postprocess(self, x):
        return self.labels[int(x.sigmoid().item() > 0.5)]


class BinaryTarget:
    def __init__(self, labels):
        self.labels = labels
        self.lookup = {l: i for i, l in enumerate(labels)}

    def eval(self):
        pass

    def preprocess(self, x):
        return self.lookup[x]

    def forward(self, x):
        return x.type(torch.float)
