import sys
# remove once platon supports python>=3.8
# Types was added to typing in 3.8
if sys.version_info >= (3, 8):
    from typing import Literal, Protocol, TypedDict
else:
    from typing_extensions import Literal, Protocol, TypedDict
