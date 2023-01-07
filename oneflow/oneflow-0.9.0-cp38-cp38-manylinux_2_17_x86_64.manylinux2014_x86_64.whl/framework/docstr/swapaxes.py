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
import oneflow
from oneflow.framework.docstr.utils import add_docstr

add_docstr(
    oneflow._C.swapaxes,
    """swapaxes(input, axis0, axis1) -> Tensor
    
    This function is equivalent to NumPy’s swapaxes function.

    For example:

    .. code-block:: python
    
        >>> import oneflow as flow
               
        >>> x = flow.tensor([[[0,1],[2,3]],[[4,5],[6,7]]])
        >>> x.shape
        oneflow.Size([2, 2, 2])
        >>> flow.swapaxes(x, 0, 1).shape
        oneflow.Size([2, 2, 2])
        >>> flow.swapaxes(x, 0, 2).shape
        oneflow.Size([2, 2, 2])

    """,
)
