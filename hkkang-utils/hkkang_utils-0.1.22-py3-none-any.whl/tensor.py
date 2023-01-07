import torch
from typing import List, Tuple


def show_environment_setting(print_fn):
    msg = "CUDA INFO:"
    msg += f"\n\tIs CUDA supported by this system? {torch.cuda.is_available()}"
    if torch.cuda.is_available():
        msg += f"\n\tCUDA version: {torch.version.cuda}"
        msg += f"\n\tID of current CUDA device: {torch.cuda.current_device()}"
        msg += f"\n\tName of current CUDA device: {torch.cuda.get_device_name(torch.cuda.current_device())}"
    print_fn(msg)

def att_mask_from_individual_masks(tgt_mask: torch.Tensor, src_mask: torch.Tensor)-> torch.Tensor:
    """Combine two individual masks for attention mask

    :param tgt_mask: mask for target sequence with shape (bsz, tgt_len)
    :type tgt_mask: torch.Tensor
    :param src_mask: mask for source sequence with shape (bsz, src_len)
    :type src_mask: torch.Tensor
    :return: attention mask with shape (bsz, tgt_len, src_len)
    :rtype: torch.Tensor
    """
    tgt_len = tgt_mask.shape[-1]
    src_len = src_mask.shape[-1]
    
    _tgt_mask = tgt_mask.unsqueeze(-1).repeat(1, 1, src_len)
    _src_mask = src_mask.unsqueeze(1).repeat(1, tgt_len, 1)
    
    return _tgt_mask * _src_mask

def zero_pad_batching_one_dim(tensor_list: List[torch.Tensor], return_mask=True) -> Tuple[torch.Tensor, torch.Tensor]:
    max_len = max([len(tensor) for tensor in tensor_list])
    device = tensor_list[0].device
    shape = (len(tensor_list), max_len) if len(tensor_list[0].shape) == 1 else (len(tensor_list), max_len, *list(tensor_list[0].shape[1:]))
    token_tensor = torch.zeros(shape, dtype=tensor_list[0].dtype, device=device)
    if return_mask:
        mask_tensor = torch.ones(token_tensor.shape[:-1], dtype=torch.bool, device=device)
    for idx, tensor in enumerate(tensor_list):
        token_tensor[idx, :len(tensor)] = tensor
        if return_mask:
            mask_tensor[idx, :len(tensor)] = False
    return (token_tensor, mask_tensor) if return_mask else token_tensor

def zero_pad_batching_two_dim(tensor_list: List[torch.Tensor], return_mask=True) -> torch.Tensor:
    device = tensor_list[0].device
    dim_one_max_len = max([len(tensor) for tensor in tensor_list])
    dim_two_max_len = max([len(tensor[0]) for tensor in tensor_list])
    token_tensor = torch.zeros(len(tensor_list), dim_one_max_len, dim_two_max_len, dtype=tensor_list[0].dtype, device=device)
    if return_mask:
        mask_tensor = torch.ones(token_tensor, dtype=torch.bool, device=device)
    for idx, tensor in enumerate(tensor_list):
        token_tensor[idx, :len(tensor), :len(tensor[0])] = tensor
        if return_mask:
            mask_tensor[idx, :len(tensor), :len(tensor[0])] = False
    return (token_tensor, mask_tensor) if return_mask else token_tensor

def zero_pad_batching(tensor_list: List[torch.Tensor]) -> torch.Tensor:
    tensor_item = tensor_list[0]
    if len(tensor_item.shape) == 1:
        return zero_pad_batching_one_dim(tensor_list)
    elif len(tensor_item.shape) == 2:
        return zero_pad_batching_two_dim(tensor_list)
    else:
        raise NotImplementedError(f"Only support 1D and 2D tensor, but found: {tensor_item.shape}")
    
if __name__ == "__main__":
    show_environment_setting()

