from __future__ import annotations

from typing import Mapping

from tqdm.auto import tqdm


class AbsoluteProgressBar:
    percentage: float
    progress_bar: tqdm

    def __init__(self, position=None) -> None:
        self.percentage = 0
        self.progress_bar = tqdm(
            total=100,
            position=position,
            bar_format=
            "{desc}|{bar}| {percentage:.03f}% [{elapsed}<{remaining}]",
            leave=False
        )

    def __enter__(self) -> AbsoluteProgressBar:
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.progress_bar.close()

    def set_percentage(self, percentage: float) -> None:
        self.progress_bar.update(percentage - self.percentage)
        self.percentage = percentage


class AbsoluteProgressBars:
    absolute_progress_bars: Mapping[str, AbsoluteProgressBar]

    def __init__(self) -> None:
        self.absolute_progress_bars = {}

    def __enter__(self) -> AbsoluteProgressBars:
        return self

    def __exit__(self, type, value, traceback) -> None:
        for curr in self.absolute_progress_bars.values():
            curr.__exit__(type, value, traceback)

    def set_percentage(self, key: str, percentage: float) -> None:
        if key not in self.absolute_progress_bars:
            self.absolute_progress_bars[key] = AbsoluteProgressBar(
                len(self.absolute_progress_bars)
            )
        self.absolute_progress_bars[key].set_percentage(percentage)

    def set_percentages(self, percentages: Mapping[str, float]) -> None:
        for key, percentage in percentages.items():
            self.set_percentage(key, percentage)
