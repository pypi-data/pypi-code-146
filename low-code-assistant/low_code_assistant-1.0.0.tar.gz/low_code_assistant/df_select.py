from typing import Callable, List, Optional

import ipyvuetify as v
import reacton
import traitlets


class DfSelectWidget(v.VuetifyTemplate):
    template_file = (__file__, "df_select.vue")

    label = traitlets.Unicode("").tag(sync=True)
    items = traitlets.List().tag(sync=True)
    v_model = traitlets.Unicode(allow_none=True).tag(sync=True)


@reacton.component
def DfSelect(label: str, items: List, v_model: Optional[str], on_v_model: Callable[[Optional[str]], None]):
    return DfSelectWidget.element(label=label, items=items, v_model=v_model, on_v_model=on_v_model)
