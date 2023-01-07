from typing import Callable, Dict, List, Any, Tuple, Optional, Union


QueryType = Dict[str, List[str]]
HeadersType = Dict[str, str]
ReturnType = Tuple[str, HeadersType, str]
GetHandlerType = Callable[[QueryType, HeadersType], ReturnType]
PostHandlerType = Callable[[QueryType, HeadersType, Any], ReturnType]
BodyParserType = Callable[[Any], Any]

JsonType = Optional[Union[dict, list, int, float, str, bool]]