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
            ysf__naquz = set()
            qwgg__rbix = list(self.context._get_attribute_templates(self.key))
            vlpy__grujf = qwgg__rbix.index(self) + 1
            for tty__xmab in range(vlpy__grujf, len(qwgg__rbix)):
                if isinstance(qwgg__rbix[tty__xmab], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    ysf__naquz.add(qwgg__rbix[tty__xmab]._attr)
            self._attr_set = ysf__naquz
        return attr_name in self._attr_set
