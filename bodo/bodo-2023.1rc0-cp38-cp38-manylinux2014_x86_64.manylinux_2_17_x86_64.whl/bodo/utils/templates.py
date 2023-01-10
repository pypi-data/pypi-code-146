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
            dryu__zpo = set()
            updv__zwb = list(self.context._get_attribute_templates(self.key))
            sdh__ruy = updv__zwb.index(self) + 1
            for jfgpn__dmxj in range(sdh__ruy, len(updv__zwb)):
                if isinstance(updv__zwb[jfgpn__dmxj], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    dryu__zpo.add(updv__zwb[jfgpn__dmxj]._attr)
            self._attr_set = dryu__zpo
        return attr_name in self._attr_set
