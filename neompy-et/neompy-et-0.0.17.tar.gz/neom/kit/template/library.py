# Copyright 2022 neomadas-dev
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import functools
from inspect import getfullargspec, unwrap
from typing import Callable, Generic, Tuple, TypeVar

from django.template import Library as LibraryBase
from django.template import Node
from django.template.base import NodeList, Parser, Token
from django.template.context import RequestContext
from django.template.library import parse_bits
from typing_extensions import ParamSpec  # TODO: 3.10

__all__ = ["Library"]

T = TypeVar("T")
P = ParamSpec("P")


class Library(LibraryBase):
    def singletag(self, call: Callable[P, str]):
        @functools.wraps(call)
        def compile_function(parser: Parser, token: Token):
            args, kwargs = self.__CallArguments(parser, token, call)
            return SingleNode(call, args, kwargs)

        self.tag(call.__name__, compile_function)
        return call

    def composetag(self, call: Callable[P, Tuple[str, str]]):
        @functools.wraps(call)
        def compile_function(parser: Parser, token: Token):
            nodelist = parser.parse((f"end_{call.__name__}",))
            parser.delete_first_token()
            args, kwargs = self.__CallArguments(parser, token, call)
            return ComposeNode(call, args, kwargs, nodelist)

        self.tag(call.__name__, compile_function)
        return call

    def directtag(self, call: Callable[P, str]):
        @functools.wraps(call)
        def compile_function(parser: Parser, token: Token):
            args, kwargs = self.__CallArguments(parser, token, call)
            return DirectNode(call, args, kwargs)

        self.tag(call.__name__, compile_function)
        return call

    @staticmethod
    def __CallArguments(
        parser: Parser, token: Token, call: Callable[P, T]
    ) -> Tuple[P.args, P.kwargs]:
        argspec = getfullargspec(unwrap(call))[:-1]
        bits = token.split_contents()[1:]
        args, kwargs = parse_bits(
            parser,
            bits,
            *argspec,
            False,
            call.__name__,
        )
        return args, kwargs


class ArgspecNodeBase(Node, Generic[T]):
    def __init__(self, call: Callable[P, T], args: P.args, kwargs: P.kwargs):
        self.call = call
        self.args = args
        self.kwargs = kwargs
        super().__init__()

    def _Call(self, context: RequestContext) -> T:
        args, kwargs = self.__ResolveArguments(context)
        return self.call(*args, **kwargs)

    def __ResolveArguments(
        self, context: RequestContext
    ) -> Tuple[P.args, P.kwargs]:
        args = [arg.resolve(context) for arg in self.args]
        kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
        return args, kwargs


class SingleNode(ArgspecNodeBase):
    def render(self, context: RequestContext):
        return self._Call(context)


class ComposeNode(ArgspecNodeBase):
    def __init__(
        self,
        call: Callable[P, Tuple[str, str]],
        args: P.args,
        kwargs: P.kwargs,
        nodelist: NodeList,
    ):
        super().__init__(call, args, kwargs)
        self.nodelist = nodelist

    def render(self, context: RequestContext):
        begin, end = self._Call(context)
        body = self.nodelist.render(context)
        return f"{begin}{body}{end}"


class DirectNode(ArgspecNodeBase):
    def render(self, context: RequestContext):
        return context.template.engine.from_string(self._Call(context)).render(
            context
        )
