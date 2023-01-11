"""Node utils"""
from typing import Optional
import torch as tr

def compare_two_states(state1: Optional[tr.Tensor], state2: Optional[tr.Tensor]) -> bool:
    """Returns true if both states are identical"""
    assert isinstance(state1, (tr.Tensor, type(None))), f"State should be Tensor or None, got {type(state1)}"
    assert isinstance(state2, (tr.Tensor, type(None))), f"State should be Tensor or None, got {type(state2)}"
    if isinstance(state1, tr.Tensor) and isinstance(state2, tr.Tensor):
        return tr.allclose(state1, state2)
    return state1 == state2
