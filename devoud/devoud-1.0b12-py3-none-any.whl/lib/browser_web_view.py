from .devoud_data import *
from .browser_context_menu import BrowserContextMenu
from .download_manager import DownloadMethod


class BrowserWebView(QWebEngineView):
    def __init__(self, parent):
        super().__init__()
        self.window = parent.window
        self.profile = parent.window.profile
        self.embedded = False
        self.menu = None
        self.title = 'Нет названия'
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, False)
        self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.setPage(QWebEnginePage(self.window.profile, self))

    def save_image_as(self):
        DownloadMethod.Method = DownloadMethod.SaveAs
        self.page().triggerAction(QWebEnginePage.DownloadImageToDisk)

    def createWindow(self, type_):
        if type_ == QWebEnginePage.WebBrowserTab:
            # запрос на новую вкладку
            return self.window.tab_widget.create_tab()

    def contextMenuEvent(self, event):
        self.menu = BrowserContextMenu(self.window)
        self.menu.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        page = self.page()

        if self.lastContextMenuRequest().selectedText():
            self.menu.addAction('Копировать', lambda: page.triggerAction(QWebEnginePage.Copy))
            self.menu.addSeparator()
            self.menu.addAction(f'Поиск в {FS.get_option("searchEngine")}', lambda: self.window.tab_widget.create_tab(
                f'{search_engines[FS.get_option("searchEngine")][0]}{page.selectedText()}'))
        elif self.lastContextMenuRequest().mediaType() == QWebEngineContextMenuRequest.MediaTypeImage:
            self.menu.addAction('Копировать изображение',
                                lambda: page.triggerAction(QWebEnginePage.CopyImageToClipboard))
            self.menu.addAction('Копировать ссылку на изображение',
                                lambda: page.triggerAction(QWebEnginePage.CopyImageUrlToClipboard))
            self.menu.addAction('Сохранить изображение как', self.save_image_as)
            self.menu.addAction('Открыть в новой вкладке',
                                lambda: self.window.tab_widget.create_tab(
                                    self.lastContextMenuRequest().mediaUrl().toString()))
        elif self.lastContextMenuRequest().linkUrl().isValid():
            self.menu.addAction('Копировать ссылку', lambda: page.triggerAction(QWebEnginePage.CopyLinkToClipboard))
            self.menu.addAction('Открыть в новой вкладке',
                                lambda: self.window.tab_widget.create_tab(
                                    self.lastContextMenuRequest().linkUrl().toString()))
        self.menu.addSeparator()
        self.menu.addAction('Выделить всё', lambda: page.triggerAction(QWebEnginePage.SelectAll))
        self.menu.addAction('Назад', self.back)
        self.menu.addAction('Вперед', self.forward)
        self.menu.addAction('Перезагрузить', lambda: page.triggerAction(QWebEnginePage.Reload))
        self.menu.addSeparator()
        self.menu.addAction('Посмотреть исходники', lambda: page.triggerAction(QWebEnginePage.ViewSource))
        self.menu.popup(event.globalPos())
