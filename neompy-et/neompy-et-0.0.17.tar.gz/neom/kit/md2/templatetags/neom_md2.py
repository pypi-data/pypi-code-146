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

from django.template import Node
from django.template.base import Parser, Token
from django.template.context import RequestContext

from neom.kit.template.library import Library
from neom.templatetags.neom_webtools import keytoken as _kt

__all__ = (
    "neom_md2_button_contained",
    "neom_md2_button_outlined",
    "neom_md2_button_text",
    "neom_md2_style",
)

register = Library()


@register.tag
def neom_md2_style(parser: Parser, token: Token):
    return Md2StyleNode()


@register.singletag
def neom_md2_button_text(label: str):
    return (
        f'<button class="{_kt("mdc-button")}">'
        f'<span class="{_kt("mdc-button__ripple")}"></span>'
        f'<span class="{_kt("mdc-button__label")}">{label}</span>'
        "</button>"
    )


@register.singletag
def neom_md2_button_outlined(label: str):
    return (
        f'<button class="{_kt("mdc-button")} {_kt("mdc-button--outlined")}">'
        f'<span class="{_kt("mdc-button__ripple")}"></span>'
        f'<span class="{_kt("mdc-button__label")}">{label}</span>'
        "</button>"
    )


@register.singletag
def neom_md2_button_contained(label: str):
    return (
        f'<button class="{_kt("mdc-button")} {_kt("mdc-button--raised")}">'
        f'<span class="{_kt("mdc-button__label")}">{label}</span>'
        "</button>"
    )


class Md2StyleNode(Node):
    def render(self, context: RequestContext):
        template = context.template.engine.get_template("neom/kit/md2/web.css")
        return f"<style>{template.render(context)}</style>"
