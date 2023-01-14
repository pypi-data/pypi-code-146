import os
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

import torch
from torch import Tensor
from torch.utils.data import Dataset


class CommonVoiceDataset(Dataset):
    def __init__(
        self,
        auth_token: str,
        version: int,
        sub_version: int = 0,
        root: str = "./data",
        languages: Sequence[str] = ["en"],
        with_info: bool = False,
        transforms: Optional[Callable] = None,
    ):
        self.with_info = with_info
        self.transforms = transforms

        from datasets import interleave_datasets, load_dataset

        self.dataset = interleave_datasets(
            [
                load_dataset(
                    f"mozilla-foundation/common_voice_{version}_{sub_version}",
                    language,
                    split="train",
                    cache_dir=os.path.join(root, "common_voice_dataset"),
                    use_auth_token=auth_token,
                )
                for language in languages
            ]
        )

    def __getitem__(
        self, idx: Union[Tensor, int]
    ) -> Union[Tensor, Tuple[Tensor, Dict]]:
        idx = idx.tolist() if torch.is_tensor(idx) else idx  # type: ignore
        data = self.dataset[idx]

        waveform = torch.tensor(data["audio"]["array"]).view(1, -1)

        info = dict(
            sample_rate=data["audio"]["sampling_rate"],
            text=data["sentence"],
            age=data["age"],
            accent=data["accent"],
            gender=data["gender"],
            locale=data["locale"],
        )

        if self.transforms:
            waveform = self.transforms(waveform)
        return (waveform, info) if self.with_info else waveform

    def __len__(self) -> int:
        return len(self.dataset)
