from statsu.ui.main_window import MainWindow
from statsu.actions.settings import WindowSettings

class ActionBase:
    def __init__(
            self, 
            window: MainWindow, 
            settings: WindowSettings
        ) -> None:
        
        self.main_window = window
        self.window_settings = settings