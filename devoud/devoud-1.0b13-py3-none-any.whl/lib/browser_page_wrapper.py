from .devoud_data import *
from .pages import *
from .browser_embedded_view import EmbeddedView
from .browser_web_view import BrowserWebView
import re

url_protocol_pattern = re.compile(r'^(?:http|https|ftp|ftps|devoud|file)://', re.IGNORECASE)
url_pattern = re.compile("^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")


class BrowserPageWrapper(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('browser_page')
        self.tab_widget = parent
        self.window = parent.window()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.layout().addWidget(self.progress_bar)

        self.url = None
        self.view = None
        self.title = None

    def create_web_view(self):
        if self.view is not None:
            self.view.deleteLater()
        self.view = BrowserWebView(self)
        self.view.titleChanged.connect(lambda new_title: self.update_title(new_title))
        self.view.page().urlChanged.connect(self.url_changed)
        self.view.loadStarted.connect(self.loadStartedHandler)
        self.view.loadProgress.connect(self.loadProgressHandler)
        self.view.loadFinished.connect(self.loadFinishedHandler)
        self.layout().addWidget(self.view)

    def create_embedded_view(self, url='devoud://void'):
        print(f'[Страница]: Открытие встроенной страницы ({url})')
        if self.view is not None:
            self.view.deleteLater()
        self.view = embedded_pages.get(url.partition('#')[0], NotFoundPage)(self)
        self.layout().addWidget(self.view)

    @staticmethod
    def is_url(url):
        """По протоколу либо по домену"""
        return (re.match(url_protocol_pattern, url) is not None) or (re.match(url_pattern, url) is not None)

    @staticmethod
    def return_type_by_ulr(url):
        return EmbeddedView if url[:9].lower() == 'devoud://' else BrowserWebView

    def load(self, url: str, allow_search=False):
        url = redirects.get(url, url)  # если редирект не найден, то значение остается
        self.url = url

        if self.is_url(url):
            # если это ссылка, то блокируем поиск
            allow_search = False

        formatted_url = QUrl.fromUserInput(url).toString()

        if (self.view is None or self.view.embedded) and self.return_type_by_ulr(url) is BrowserWebView:
            self.create_web_view()
        elif (self.view is None or not self.view.embedded) and self.return_type_by_ulr(url) is EmbeddedView:
            self.create_embedded_view(url)
        elif self.view.embedded and self.return_type_by_ulr(url) is EmbeddedView:
            self.create_embedded_view(url)

        if not self.view.embedded:
            if allow_search:
                # при разрешении вставляем текст в поисковый движок
                self.view.load(f'{search_engines[self.window.search_box.currentText()][0]}{url}')
            else:
                self.view.load(formatted_url)

        PagesObserver.control_update_lists()
        self.update_title(self.view.title)

    def reload(self):
        self.view.reload()

    def back(self):
        self.view.back()

    def forward(self):
        self.view.forward()

    def url_changed(self, url):
        if isinstance(url, QUrl):
            self.url = url.toString()
        if FS.get_option('saveHistory'):
            with open(f'{FS.config_dir()}/history', 'a') as history_file:
                history_file.write(self.url + '\n')
        if self.tab_widget.currentWidget() == self:
            self.window.address_edit.setText(self.url)
            self.window.address_edit.setCursorPosition(0)
            self.window.check_state_bookmark()
        PagesObserver.control_update_lists()

    def update_title(self, title):
        self.title = title
        index = self.tab_widget.indexOf(self)
        self.tab_widget.setTabText(index, title)
        if self.tab_widget.currentWidget() == self:
            self.window.set_title(title)

    @QtCore.Slot()
    def loadStartedHandler(self):
        print(f"[Страница]: Начата загрузка страницы ({self.url})")

    @QtCore.Slot(int)
    def loadProgressHandler(self, progress):
        self.progress_bar.setValue(progress)
        print(f"[Страница]: {progress}% ({self.url})")

    @QtCore.Slot()
    def loadFinishedHandler(self):
        self.progress_bar.setValue(0)
        print(f"[Страница]: Страница загружена ({self.url})")
