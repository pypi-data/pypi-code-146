from torch.optim import Optimizer


def get_learning_rate(optimizer: Optimizer) -> float:
    """Get learning rate from optimizer
    """
    return optimizer.param_groups[0]['lr']
