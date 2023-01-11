"""
Helper functions and classes to simplify Template Generation
for Bodo classes.
"""
import numba
from numba.core.typing.templates import AttributeTemplate


class OverloadedKeyAttributeTemplate(AttributeTemplate):
    _attr_set = None

    def _is_existing_attr(self, attr_name):
        if self._attr_set is None:
            gehc__ibiru = set()
            mhy__auvke = list(self.context._get_attribute_templates(self.key))
            aoci__nvay = mhy__auvke.index(self) + 1
            for fmv__cymb in range(aoci__nvay, len(mhy__auvke)):
                if isinstance(mhy__auvke[fmv__cymb], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    gehc__ibiru.add(mhy__auvke[fmv__cymb]._attr)
            self._attr_set = gehc__ibiru
        return attr_name in self._attr_set
