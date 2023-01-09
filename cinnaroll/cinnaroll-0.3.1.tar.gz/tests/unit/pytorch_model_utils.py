import numpy as np
import numpy.typing as npt
from typing import Tuple, Optional, Dict, Any

import torch


class PyTorchSimpleModel(torch.nn.Module):  # type: ignore
    """A class representing a simple dense neural network in PyTorch."""

    def __init__(self, input_dim: int, dense_layers: Tuple[int, int]):
        super().__init__()
        self.fc1 = torch.nn.Linear(input_dim, dense_layers[0])
        self.fc2 = torch.nn.Linear(dense_layers[0], dense_layers[1])
        self.criterion = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.01)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.nn.functional.relu(self.fc1(x))
        return self.fc2(x).squeeze(1)

    def perform_training(
        self, X: torch.Tensor, Y: torch.Tensor, num_epochs: int
    ) -> None:
        for epoch in range(num_epochs):
            # zero the parameter gradients
            self.optimizer.zero_grad()

            loss = self.compute_loss(X, Y)
            print(f"Epoch: {epoch + 1}, loss: {loss.item():.4f}")
            loss.backward()
            self.optimizer.step()

    def compute_loss(self, X: torch.Tensor, Y: torch.Tensor) -> torch.Tensor:
        outputs = self.forward(X)
        return self.criterion(outputs, Y)


def create_pytorch_model_object(
    input_dim: int,
    dense_layers: Tuple[int, int],
    weights: Optional[Dict[str, npt.NDArray[np.float64]]] = None,
) -> Any:
    model_object = PyTorchSimpleModel(input_dim, dense_layers)

    if weights is not None:
        for j in range(1, 3):
            model_object.state_dict()[f"fc{j}.weight"].data[:, :] = torch.Tensor(
                weights[f"lay{j}.w"].T
            )
            model_object.state_dict()[f"fc{j}.bias"].data[:] = torch.Tensor(
                weights[f"lay{j}.b"]
            )
    return model_object
