from typing import Iterator

from torch import Tensor
from jaxtyping import Float

from torchmix.core._module import Component


class Repeat(Component):
    """Repeat the given module `depth` times.

    `Repeat` creates multiple copies of the `children` and
    applies them sequentially. Every copy of `children` will
    be re-instantiated based on its configuration. The input
    and output shapes of the `children` must be the same in
    order to be applied in this way.

    Args:
        children (Component): The module to be repeated.
        depth (int): The number of copies of `children` to create.

    Examples:
        Repeat(
            nn.Sequential(
                nn.Linear(100, 200),
                nn.GELU(),
                nn.Linear(200, 100)
            ),
            depth=12
        )
    """

    def __init__(
        self,
        children: Component,
        depth: int = 8,
    ) -> None:
        for idx in range(depth):
            self.add_module(
                str(idx),
                children.instantiate(),
            )

    def __len__(self) -> int:
        return len(self._modules)

    def __iter__(self) -> Iterator[Component]:
        return iter(self._modules.values())  # type: ignore

    def forward(self, x: Float[Tensor, " *shape"]) -> Float[Tensor, " *shape"]:
        for module in self:
            x = module(x)
        return x
