# -*- coding: utf-8 -*-
from z3c.form.browser.widget import HTMLFormElement
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.object import ObjectWidget
from z3c.form.widget import FieldWidget
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.schema.interfaces import IObject


class IExceptionalClosure(IObject):
    """IExceptionalClosure"""


@implementer(IExceptionalClosure)
class ExceptionalClosure(schema.Object):
    """ """


@implementer(IExceptionalClosure)
class ExceptionalClosureWidget(HTMLFormElement, ObjectWidget):

    klass = "object-widget"
    css = "object"


@adapter(IObject, IFormLayer)
@implementer(IFieldWidget)
def ObjectFieldWidget(field, request):
    """IFieldWidget factory for IObjectWidget."""
    return FieldWidget(field, ExceptionalClosureWidget(request))
