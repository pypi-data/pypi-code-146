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
            fetf__kplw = set()
            aaojf__dxj = list(self.context._get_attribute_templates(self.key))
            ckj__goiy = aaojf__dxj.index(self) + 1
            for bgqoq__cgxqk in range(ckj__goiy, len(aaojf__dxj)):
                if isinstance(aaojf__dxj[bgqoq__cgxqk], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    fetf__kplw.add(aaojf__dxj[bgqoq__cgxqk]._attr)
            self._attr_set = fetf__kplw
        return attr_name in self._attr_set
