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
            ixye__bdz = set()
            xpjpd__esjek = list(self.context._get_attribute_templates(self.key)
                )
            lhvla__uqijv = xpjpd__esjek.index(self) + 1
            for sjp__nakk in range(lhvla__uqijv, len(xpjpd__esjek)):
                if isinstance(xpjpd__esjek[sjp__nakk], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    ixye__bdz.add(xpjpd__esjek[sjp__nakk]._attr)
            self._attr_set = ixye__bdz
        return attr_name in self._attr_set
