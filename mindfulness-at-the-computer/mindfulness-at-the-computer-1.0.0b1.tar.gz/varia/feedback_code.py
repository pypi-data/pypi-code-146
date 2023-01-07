"""
SK_NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN = "nr_of_times_until_feedback_shown"
SK_NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN: matc.shared.INITIAL_NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN,
FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP = -1
INITIAL_NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN = 10

    def update_gui(self):
        self.gui_update_bool = True
        # settings = matc.state.settings.is.SettingsM.get()
        self.show_again_qcb.setChecked(
            settings.nr_times_started_since_last_feedback_notif !=
            matc.shared.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP
        )
        self.gui_update_bool = False

    def on_show_again_toggled(self, i_checked: bool):
        if self.gui_update_bool:
            return
        settings = matc.model.SettingsM.get()
        if i_checked:
            if settings.nr_times_started_since_last_feedback_notif ==
            matc.shared.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP:
                settings.nr_times_started_since_last_feedback_notif = 0
            else:
                pass
        else:
            settings.nr_times_started_since_last_feedback_notif =
            matc.shared.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP


    self.show_again_qcb = QtWidgets.QCheckBox(self.tr("Show this dialog at startup again in the
    future"))
    self.show_again_qcb.toggled.connect(self.on_show_again_toggled)
    vbox_l2.addWidget(self.show_again_qcb)

"""
