import dataclasses


@dataclasses.dataclass
class LightEffect:
    name: str
    colors: [[int]]

    @staticmethod
    def icicle() -> 'LightEffect':
        return LightEffect(
            "Aurora",
            [
                [120, 100, 100],
                [240, 100, 100],
                [260, 100, 100],
                [280, 100, 100]
            ]
        )

    @staticmethod
    def icicle() -> 'LightEffect':
        return LightEffect(
            "Icicle",
            [[190, 100, 100]]
        )

    @staticmethod
    def ocean() -> 'LightEffect':
        return LightEffect(
            "Ocean",
            [[198, 84, 100]]
        )

    @staticmethod
    def rainbow() -> 'LightEffect':
        return LightEffect(
            "Rainbow",
            [
                [0, 100, 100],
                [100, 100, 100],
                [200, 100, 100],
                [300, 100, 100]
            ]
        )
