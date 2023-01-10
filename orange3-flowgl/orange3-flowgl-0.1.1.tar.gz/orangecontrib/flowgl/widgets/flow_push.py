from concurrent.futures import Executor

import flowgl
import pandas as pd
from Orange.data import Table
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.concurrent import ConcurrentWidgetMixin
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from AnyQt.QtWidgets import QLineEdit


class PushToFlow(OWWidget, ConcurrentWidgetMixin):
    name = "Push to Flow"
    description = "Push data to Flow Immersive"
    icon = "icons/flow_icon.svg"
    priority = 100  # where in the widget order it will appear
    keywords = ["flow", "push"]
    want_main_area = False
    resizing_enabled = False
    
    username = Setting("")
    password = Setting("")
    dataset_name = Setting("")
    autocommit = Setting(True)
    
    class Inputs:
        data = Input("Data", Table)

    class Error(OWWidget.Error):
        auth_error = Msg("Invalid credentials")

    def __init__(self):
        OWWidget.__init__(self)
        ConcurrentWidgetMixin.__init__(self)
        self.data = None
        self.client = None

        self.dataset_edit = gui.lineEdit(
            self.controlArea,
            self,
            "dataset_name",
            box="Dataset Name",
            callback=self.commit.deferred
        )

        self.credentials_box = gui.widgetBox(self.controlArea, "Credentials")

        self.username_edit = gui.lineEdit(
            self.credentials_box,
            self,
            "username",
            label="Username",
            callback=self.credentials_changed,
        )
        self.password_edit = gui.lineEdit(
            self.credentials_box,
            self,
            "password",
            label="Password",
            callback=self.credentials_changed,
        )
        # make password field show dots
        self.password_edit.setEchoMode(QLineEdit.Password)

        # autocommit
        gui.auto_commit(self.controlArea, self, "autocommit", "Push", box=False)

    @Inputs.data
    def send_data(self, data):
        if data:
            self.data = data
        else:
            self.data = None

        self.commit.deferred()

    def credentials_changed(self):
        self.Error.auth_error.clear()
        if not self.username or not self.password:
            self.client = None
            return
        try:
            self.client = flowgl.Client(self.username, self.password)
        except Exception:
            self.Error.auth_error()
            self.client = None

    @gui.deferred
    def commit(self):
        if self.client is None:
            self.credentials_changed()
        if not self.data or not self.client or not self.dataset_name:
            return

        self.start(self.push_data, self.data)

    def push_data(self, data, *args, **kwargs):
        concat_df = pd.concat([data.X_df, data.Y_df, data.metas_df], axis=1)
        self.client.push_data(concat_df, dataset_title=self.dataset_name)

    def on_done(self, result):
        pass

    def send_report(self):
        # self.report_plot() includes visualizations in the report
        self.report_caption(self.label)


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(PushToFlow).run()
