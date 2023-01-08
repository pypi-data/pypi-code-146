from .AlteredAiDataLoader import AlteredAiDataLoader
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from .DataTransformations import DataTransformations


class AlteredAiPytorch(AlteredAiDataLoader):

    def __init__(self, access_key_id, secret_access_key, dataKey, resize=64, batchSize=5):
        super().__init__(access_key_id, secret_access_key, dataKey)
        self.resize = resize
        self.batchSize = batchSize
        transform = transforms.Compose(
            [transforms.Resize(self.resize), transforms.ToTensor(), transforms.Normalize(mean=0, std=1)])
        dataset = DataTransformations(self.data, self.targets, transform=transform)
        self.dataloader = DataLoader(dataset, batch_size=self.batchSize)

    def getPytorchDataLoader(self):
        return self.dataloader

    def dataloaderIterator(self):
        iterator = iter(self.dataloader)
        inputs, classes = next(iterator)
        return inputs, classes

    def getTransformationInfo(self):
        pass
