from typing import Iterator, Literal, Optional, Tuple, Union, overload

#
# @overload
# def thing(value_1: str, value_2: Optional[str] = None) -> Tuple[str, str]:
#     ...
#
#
# @overload
# def thing(
#     value_1: str, value_2: Optional[str], include_extra: Literal[False]
# ) -> Tuple[str, str]:
#     ...
#
#
# @overload
# def thing(
#     value_1: str, value_2: Optional[str], include_extra: Literal[True]
# ) -> Tuple[str, str, str]:
#     ...
#
#
# @overload
# def thing(value_1: str, *, include_extra: Literal[False]) -> Tuple[str, str]:
#     ...
#
#
# @overload
# def thing(value_1: str, *, include_extra: Literal[True]) -> Tuple[str, str, str]:
#     ...
#
#
# # @overload
# # def thing(
# #     value_1: str, value_2: Optional[str], include_extra: bool
# # ) -> Union[Tuple[str, str], Tuple[str, str, str]]:
# #     ...
#
#
# def thing(
#     value_1: str, value_2: Optional[str] = None, include_extra: bool = False
# ) -> Union[Tuple[str, str], Tuple[str, str, str]]:
#     if value_2 is None:
#         value_2 = "empty"
#     if include_extra:
#         return value_1, value_2, "extra"
#     return value_1, value_2
#
#
# thing("aaa", include_extra=True)


def thing() -> Iterator[int]:
    yield ""
    yield ""
    yield ""


for x in thing():
    print(1 + x)
