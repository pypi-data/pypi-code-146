from torch import nn
from torch.autograd import Function
import torch


def nv_tensor_quant(inputs, amax=None, num_bits=8, unsigned=False, narrow_range=True):
    """Shared function body between TensorQuantFunction and FakeTensorQuantFunction.
    Author: nv_pytorch_quantization:
    https://github.com/NVIDIA/TensorRT/blob/master/tools/pytorch-quantization/pytorch_quantization/tensor_quant.py#L315
    """
    if isinstance(amax, torch.Tensor) and inputs.dim() != amax.dim():
        raise ValueError(
            "amax %s has different shape than inputs %s. Make sure broadcast works as expected!",
            amax.size(),
            inputs.size(),
        )

    # print("{} bits quantization on shape {} tensor.".format(num_bits, inputs.size()))

    if amax == None:
        amax = torch.amax(inputs, keepdim=True)

    if unsigned:
        if inputs.min() < 0.0:
            raise TypeError("Negative values encountered in unsigned quantization.")

    # Computation must be in FP32 to prevent potential over flow.
    input_dtype = inputs.dtype
    if inputs.dtype == torch.half:
        inputs = inputs.float()
    if amax.dtype == torch.half:
        amax = amax.float()

    min_amax = amax.min()
    if min_amax < 0:
        raise ValueError("Negative values in amax")

    max_bound = torch.tensor(
        (2.0 ** (num_bits - 1 + int(unsigned))) - 1.0, device=amax.device
    )
    if unsigned:
        min_bound = 0
    elif narrow_range:
        min_bound = -max_bound
    else:
        min_bound = -max_bound - 1
    scale = max_bound / amax

    epsilon = 1.0 / (1 << 24)
    if min_amax <= epsilon:  # Treat amax smaller than minimum representable of fp16 0
        zero_amax_mask = amax <= epsilon
        scale[zero_amax_mask] = 0  # Value quantized with amax=0 should all be 0

    outputs = torch.clamp((inputs * scale).round_(), min_bound, max_bound)

    if min_amax <= epsilon:
        scale[
            zero_amax_mask
        ] = 1.0  # Return 1 makes more sense for values quantized to 0 with amax=0

    if input_dtype == torch.half:
        outputs = outputs.half()

    return outputs, scale


def bit_set(var, pos, val):
    """
    description:
        this methods implements the following bit_set function:
        // variable, position, value
        #define BIT_SET(var, pos, val) var |= (val << pos)
    """
    var |= val << pos
    return var


def get_binary_row(nd_row, binary_row, nd_size, bits_per_binary_word):
    """
    description:
        binarize the input NDArray.
        This is a re-implementation of the cpp version:
        for (int i = 0; i < size; i+=BITS_PER_BINARY_WORD) {
          BINARY_WORD rvalue=0;
          BINARY_WORD sign;
          for (int j = 0;j < BITS_PER_BINARY_WORD; ++j) {
            sign = (row[i+j]>=0);
            BIT_SET(rvalue, j, sign);
          }
          b_row[i/BITS_PER_BINARY_WORD] = rvalue;
        }
    """
    i = 0
    while i < nd_size:
        rvalue = 0
        j = 0
        while j < bits_per_binary_word:
            sign = 0
            if nd_row[i + j] >= 0:
                sign = 1
            rvalue = bit_set(rvalue, j, sign)
            j += 1

        # print('{0:64b}'.format(rvalue))

        binary_row[int(i / bits_per_binary_word)] = rvalue

        # print('{0:64b}'.format(binary_row[int(i/bits_per_binary_word)]))
        # testing stuff
        # d = mx.nd.array(binary_row, dtype="float64")
        # print('{0:64b}'.format(int(d.asnumpy()[int(i/bits_per_binary_word)])))
        i += bits_per_binary_word
    return binary_row


def get_binary_col(nd_col, binary_col, dim_n, dim_k, bits_per_binary_word):
    """
    description:
        binarize an array column wise.
        A re-implementation of the cpp version:

        for(int y=0; y<(n/BITS_PER_BINARY_WORD); y++){
          for(int x=0; x < k; ++x){
            BINARY_WORD rvalue=0;
            BINARY_WORD sign;
            for(int b=0; b<BITS_PER_BINARY_WORD; ++b){
              sign = (col[(y*BITS_PER_BINARY_WORD+b)*k + x]>=0);
              BIT_SET(rvalue, b, sign);
            }
            b_col[y*k + x] = rvalue;
          }
        }

    """
    y = 0
    while y < int(dim_n / bits_per_binary_word):
        x = 0
        while x < dim_k:
            rvalue = 0
            b = 0
            while b < bits_per_binary_word:
                sign = 0
                if nd_col[(y * bits_per_binary_word + b) * dim_k + x] >= 0:
                    sign = 1
                rvalue = bit_set(rvalue, b, sign)
                b += 1
            binary_col[y * dim_k + x] = rvalue
            x += 1
        y += 1

    return binary_col
