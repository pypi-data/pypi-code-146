import logging

from PySide6 import QtCore

import remembering.model_old
import remembering.rg_global


class Timer(QtCore.QObject):
    update_signal = QtCore.Signal(list, bool)

    # -list has a collection of IDs, bool is whether it's a missed notification

    def __init__(self):
        super().__init__()

        self.shared_minute_qtimer = None

    def start(self):
        self.show_notifications(True)
        self.setup_notification_times()
        self.start_shared_minute_timer()

    def setup_notification_times(self):
        remembrances_list = remembering.model_old.Remembrances.get_all()
        for remembrance_item in remembrances_list:
            next_notification_time_ts_secs = remembrance_item.get_next_notification_time()
            remembering.model_old.Remembrances.update_next_notif(
                remembrance_item.id_int,
                next_notification_time_ts_secs
            )

    def show_notifications(self, i_missed: bool):
        now_ts_secs = QtCore.QDateTime.currentSecsSinceEpoch()
        remembrances_list = remembering.model_old.Remembrances.get_all()
        new_notifications_list = []
        for remembrance_item in remembrances_list:
            notification_time_ts_secs = remembrance_item.next_notif_ts_int
            if now_ts_secs >= notification_time_ts_secs and notification_time_ts_secs != \
                    remembering.model_old.NO_VALUE_SET_INT:
                t_notification_fired_bool = remembrance_item.notif_fired_bool
                next_notification_time_ts_secs = remembering.model_old.NO_VALUE_SET_INT
                if remembrance_item.notif_active_bool:
                    if t_notification_fired_bool == False:
                        new_notifications_list.append(remembrance_item.id_int)
                    t_notification_fired_bool = True
                    next_notification_time_ts_secs = remembrance_item.get_next_notification_time()
                remembering.model_old.Remembrances.update_next_notif(
                    remembrance_item.id_int,
                    next_notification_time_ts_secs
                )
                remembering.model_old.Remembrances.update_notif_fired(
                    remembrance_item.id_int,
                    t_notification_fired_bool
                )

        logging.debug("new_notifications_list = " + str(new_notifications_list))
        self.update_signal.emit(new_notifications_list, i_missed)

    def start_shared_minute_timer(self):
        self.stop_shared_minute_timer()
        self.shared_minute_qtimer = QtCore.QTimer(self)
        self.shared_minute_qtimer.timeout.connect(self.shared_minute_timer_timeout)
        self.shared_minute_qtimer.start(60 * 1000)  # -one minute

    def stop_shared_minute_timer(self):
        if self.shared_minute_qtimer is not None and self.shared_minute_qtimer.isActive():
            self.shared_minute_qtimer.stop()
        # update_gui()

    def shared_minute_timer_timeout(self):
        """
        Function is called every minute
        """
        logging.debug("timeout")
        self.show_notifications(False)
