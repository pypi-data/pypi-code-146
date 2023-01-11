import grok
from waeup.kofa.interfaces import IKofaObject
from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAnnotations

class KofaAttributeAnnotations(AttributeAnnotations, grok.Adapter):
    """An adapter to IAnnotations for any KofaObject.

    Providing this adapter, each Kofa object becomes (attribute)
    annotatable.
    """
    grok.provides(IAnnotations)
    grok.context(IKofaObject)
