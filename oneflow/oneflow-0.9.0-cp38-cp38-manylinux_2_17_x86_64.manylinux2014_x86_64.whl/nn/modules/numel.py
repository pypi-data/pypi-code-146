"""
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import oneflow as flow


def numel_op(input):
    """
    numel(input) -> int

    Returns the total number of elements in the :attr:`input` tensor.

    Args:
        input (oneflow.Tensor): Input Tensor

    .. code-block:: python

        >>> import oneflow as flow

        >>> a = flow.randn(1, 2, 3, 4, 5)
        >>> flow.numel(a)
        120
        >>> a = flow.zeros(4,4)
        >>> flow.numel(a)
        16
    """
    return input.numel()


if __name__ == "__main__":
    import doctest

    doctest.testmod(raise_on_error=True)
