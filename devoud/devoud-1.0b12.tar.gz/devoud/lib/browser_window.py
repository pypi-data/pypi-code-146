from functools import cached_property
from string import Template
from .browser_find_widget import FindWidget
from .browser_page_wrapper import *
from .browser_context_menu import BrowserContextMenu
from .download_manager import DownloadManager
from devoud import __name__, __version__


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme = Theme()
        self.setWindowIcon(QIcon('./ui/svg/browser_icon.svg'))
        self.setWindowTitle(__name__)
        self.setMinimumSize(QSize(400, 300))

        # профиль для веб-страниц
        self.profile = QWebEngineProfile('DevoudProfile')
        self.profile.setCachePath(str(FS.os_user_dir()))
        self.download_manager = DownloadManager(self)
        self.profile.downloadRequested.connect(lambda req: self.download_manager.download_requested(req))

        # шрифт
        QFontDatabase.addApplicationFont("./ui/fonts/ClearSans-Medium.ttf")
        self.setFont(QFont('Clear Sans Medium'))

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.window_layout = QGridLayout(self.central_widget)
        self.window_layout.setSpacing(0)
        self.window_layout.setContentsMargins(0, 0, 0, 0)

        # для растяжения окна с кастомной рамкой
        self.size_grip_right = QSizeGrip(self)
        self.window_layout.addWidget(self.size_grip_right, 1, 2)
        self.size_grip_right.setFixedWidth(5)
        self.size_grip_right.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.size_grip_right.setStyleSheet('border-radius: 5px; background: transparent;')

        self.size_grip_left = QSizeGrip(self)
        self.size_grip_left.setFixedWidth(5)
        self.size_grip_left.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.window_layout.addWidget(self.size_grip_left, 1, 0)
        self.size_grip_left.setStyleSheet('border-radius: 5px; background: transparent;')

        self.size_grip_top = QSizeGrip(self)
        self.window_layout.addWidget(self.size_grip_top, 0, 1)
        self.size_grip_top.setFixedHeight(5)
        self.size_grip_top.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.size_grip_top.setStyleSheet('border-radius: 5px; background: transparent;')

        self.size_grip_bottom = QSizeGrip(self)
        self.window_layout.addWidget(self.size_grip_bottom, 2, 1)
        self.size_grip_bottom.setFixedHeight(5)
        self.size_grip_bottom.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.size_grip_bottom.setStyleSheet('border-radius: 5px; background: transparent;')

        # все кроме size grip
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName('main_frame')

        # ломается рендер веб-страниц
        # self.window_shadow = QGraphicsDropShadowEffect(self)
        # self.window_shadow.setBlurRadius(17)
        # self.window_shadow.setXOffset(0)
        # self.window_shadow.setYOffset(0)
        # self.window_shadow.setColor(QColor(0, 0, 0, 150))
        # self.main_frame.setGraphicsEffect(self.window_shadow)

        self.window_layout.addWidget(self.main_frame, 1, 1)
        self.main_layout = QGridLayout(self.main_frame)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.panel = BrowserPanel()
        self.main_layout.addWidget(self.panel, 1, 0, 1, 1)

        # кнопки на панели
        self.back_button = BrowserPanelButton(self.panel, icon='./ui/custom/svg/arrow_left.svg')
        self.back_button.clicked.connect(self.back_page)
        self.back_button.setObjectName('back_button')
        self.forward_button = BrowserPanelButton(self.panel, icon='./ui/custom/svg/arrow_right.svg')
        self.forward_button.clicked.connect(self.forward_page)
        self.forward_button.setObjectName('forward_button')
        self.update_button = BrowserPanelButton(self.panel, icon='./ui/custom/svg/update.svg')
        self.update_button.clicked.connect(self.update_page)
        self.update_button.setObjectName('update_button')
        self.home_button = BrowserPanelButton(self.panel, icon='./ui/custom/svg/home.svg')
        self.home_button.clicked.connect(lambda: self.load_home_page(new_tab=False))
        self.home_button.setObjectName('home_button')

        self.address_frame = QFrame(self.panel)
        self.address_frame.setObjectName("address_frame")
        self.address_frame.setFixedHeight(29)
        self.panel.layout.addWidget(self.address_frame)

        self.address_layout = QHBoxLayout(self.address_frame)
        self.address_layout.setSpacing(0)
        self.address_layout.setContentsMargins(0, 0, 0, 0)

        self.search_box = QComboBox(self.address_frame)
        [self.search_box.addItem(QIcon(search_engines[key][2]), key) for key in search_engines.keys()]
        self.search_box.setObjectName("search_box")
        self.search_box.setFixedSize(QSize(115, 29))
        self.address_layout.addWidget(self.search_box)
        self.search_box.setCurrentText(FS.get_option('searchEngine'))

        self.address_edit = AddressEdit()
        self.address_layout.addWidget(self.address_edit)

        self.bookmarks_button = BrowserPanelButton(self.address_frame, './ui/custom/svg/bookmark_empty.svg',
                                                   self.address_layout)
        self.bookmarks_button.clicked.connect(self.add_bookmark)
        self.bookmarks_button.setObjectName('bookmark_button')
        self.bookmarks_state = False

        # виджет вкладок
        self.main_layout.addWidget(self.tab_widget, 3, 0)
        self.tab_widget.set_tab_bar_position()

        # кастомная рамка окна
        self.title_bar = TitleBar()
        self.main_layout.addWidget(self.title_bar, 0, 0)
        self.title_bar.close_button.clicked.connect(self.close)
        self.title_bar.maximize_button.clicked.connect(self.restore_or_maximize)
        self.title_bar.hide_button.clicked.connect(self.showMinimized)

        def move_window(event):
            if self.isMaximized():
                self.restore_or_maximize()
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.title_bar.mouseMoveEvent = move_window

        # выбор рамки окна
        if not systemFrame:
            # убрать системную рамку окна
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.window_corner_radius('12px')
        else:
            self.title_bar.deleteLater()
            self.size_grip_right.deleteLater()
            self.size_grip_left.deleteLater()
            self.size_grip_top.deleteLater()
            self.size_grip_bottom.deleteLater()

        # контекстное меню для вызова панели управления
        self.menu_button = BrowserPanelButton(self.panel, './ui/custom/svg/options.svg')
        self.menu_button.setObjectName('menu_button')
        self.options_menu = BrowserContextMenu(self)
        self.options_menu.setFixedWidth(100)
        self.options_menu.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.options_menu.addAction('Настройки', lambda: self.tab_widget.create_tab('devoud://control#settings'))
        self.options_menu.addAction('История', lambda: self.tab_widget.create_tab('devoud://control#history'))
        self.options_menu.addAction('Закладки', lambda: self.tab_widget.create_tab('devoud://control#bookmarks'))
        self.options_menu.addAction('Загрузки', lambda: self.tab_widget.create_tab('devoud://control#downloads'))
        self.menu_button.setMenu(self.options_menu)

        # комбинации клавиш
        QShortcut(QKeySequence("F5"), self).activated.connect(self.update_page)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.show_find_on_page)
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(lambda: self.tab_widget.create_tab(new_page))
        QShortcut(QKeySequence("Ctrl+W"), self).activated.connect(lambda: self.tab_widget.close_tab(self.tab_widget.currentIndex()))

        # восстановление предыдущей сессии
        self.restore_or_home()

    def change_style(self, name=None):
        self.theme = Theme(name)
        self.setStyleSheet(self.theme.style())
        self.address_edit.findChild(QToolButton).setIcon(QIcon("./ui/custom/svg/close_tab_alt.svg"))
        self.check_state_bookmark()

    def window_corner_radius(self, radius):
        self.main_frame.setStyleSheet(Template("""
        #main_frame { 
            border-radius: $radius;
        }""").substitute(radius=radius))

    def show_find_on_page(self):
        page = self.tab_widget.current()
        page_find_widget = page.findChild(FindWidget)
        if page_find_widget:
            if not page_find_widget.isHidden():
                page_find_widget.hide_find()
            else:
                page_find_widget.show()
                page_find_widget.find_focus()
                page_find_widget.find_text()
        elif not page.view.embedded:
            find_widget = FindWidget(page)
            page.layout().addWidget(find_widget)
            find_widget.show()
            find_widget.find_focus()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def restore_or_maximize(self):
        if self.isMaximized():
            self.window_corner_radius('12px')
            self.showNormal()
        else:
            self.window_corner_radius('0px')
            self.showMaximized()

    def load_home_page(self, new_tab=True):
        if new_tab:
            self.tab_widget.create_tab()
        self.tab_widget.current().load(FS.get_option('homePage'))

    def restore_or_home(self):
        if FS.get_option('restoreTabs'):
            with open(f'{FS.config_dir()}/tabs') as tabs_file:
                links = tabs_file.read().splitlines()
                if not links:
                    return self.load_home_page()

            for link in range(len(links) - 1):
                self.tab_widget.create_tab(links[link])
            self.tab_widget.setCurrentIndex(int(links[-1]))  # последняя посещенная вкладка
        else:
            self.load_home_page()

    def set_title(self, text):
        self.setWindowTitle(f"{text} – {__name__} {__version__}")
        if not systemFrame:
            self.title_bar.label.setText(f"{text} – {__name__} {__version__}")

    def back_page(self):
        self.tab_widget.current().back()

    def forward_page(self):
        self.tab_widget.current().forward()

    def update_page(self):
        self.tab_widget.current().reload()

    def check_state_bookmark(self):
        with open(f'{FS.config_dir()}/bookmarks', 'r') as bookmarks_file:
            bookmarks = bookmarks_file.read().splitlines()
            self.bookmarks_state = self.address_edit.text() in bookmarks
            self.bookmarks_button.setStyleSheet(
                f"icon: url(./ui/custom/svg/{'bookmark' if self.bookmarks_state else 'bookmark_empty'}.svg);")

    def add_bookmark(self):
        link = self.address_edit.text()
        with open(f'{FS.config_dir()}/bookmarks', 'r') as bookmarks_file:
            bookmarks = bookmarks_file.read().splitlines()
            if link in bookmarks:
                bookmarks.remove(link)
            else:
                bookmarks.append(link)
        with open(f'{FS.config_dir()}/bookmarks', 'w') as bookmarks_file:
            bookmarks = '\n'.join(bookmarks)
            bookmarks_file.write(bookmarks)
        self.check_state_bookmark()
        PagesObserver.control_update_lists()

    def closeEvent(self, event):
        if FS.get_option('restoreTabs'):
            with open(f'{FS.config_dir()}/tabs', 'w') as tabs_file:
                tabs = PagesObserver.urls()
                tabs.append(str(self.tab_widget.currentIndex()))  # последняя посещенная вкладка
                tabs = '\n'.join(tabs)
                tabs_file.write(tabs)
            print('[Вкладки]: Текущая сессия сохранена')

    @cached_property
    def tab_widget(self):
        return BrowserTabWidget()


class TitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("title_bar")

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self)
        self.label.setObjectName("title_label")
        self.layout.addWidget(self.label)

        self.window_buttons_widget = QWidget(self)
        self.window_buttons_widget.setFixedWidth(80)
        self.window_buttons_widget.setObjectName("window_buttons")
        self.window_buttons_layout = QHBoxLayout(self.window_buttons_widget)
        self.window_buttons_layout.setContentsMargins(0, 5, 0, 0)

        self.hide_button = QPushButton(self)
        self.hide_button.setObjectName("hide_button")
        self.hide_button.setFixedSize(QSize(23, 23))
        self.hide_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.hide_button.setFlat(True)
        self.window_buttons_layout.addWidget(self.hide_button)

        self.maximize_button = QPushButton(self)
        self.maximize_button.setObjectName("maximize_button")
        self.maximize_button.setFixedSize(QSize(23, 23))
        self.maximize_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.maximize_button.setFlat(True)
        self.window_buttons_layout.addWidget(self.maximize_button)

        self.close_button = QPushButton(self)
        self.close_button.setObjectName("close_button")
        self.close_button.setFixedSize(QSize(23, 23))
        self.close_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_button.setFlat(True)
        self.window_buttons_layout.addWidget(self.close_button)

        self.right_spacer = QSpacerItem(11, 10)

        self.layout.addWidget(self.window_buttons_widget)
        self.layout.addItem(self.right_spacer)


class BrowserPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("panel")
        self.setMinimumSize(QSize(550, 45))
        self.setMaximumSize(QSize(16777215, 45))

        self.layout = QHBoxLayout(self)


class AddressEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("address_edit")
        self.setPlaceholderText('Поиск или ссылка')
        self.setFixedHeight(29)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setClearButtonEnabled(True)
        self.returnPressed.connect(self.load_from_line)

    def load_from_line(self):
        self.window().tab_widget.current().load(self.text(), allow_search=True)
        self.clearFocus()

    def focusOutEvent(self, event):
        self.setCursorPosition(0)
        super().focusOutEvent(event)


class BrowserPanelButton(QPushButton):
    def __init__(self, parent, icon: str, layout=None):
        super().__init__()
        self.parent = parent
        self.setObjectName("panel_button")
        self.setFixedSize(QSize(30, 29))
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.icon = icon
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(25, 19))
        if layout is None:
            self.parent.layout.addWidget(self)
        else:
            layout.addWidget(self)

    def update_icon(self):
        self.setIcon(QIcon(self.icon))


class BrowserTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('tab_widget')
        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideRight)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.tab_changed)

        # кнопка создания новой вкладки
        self.add_tab_button = QPushButton(self)
        self.add_tab_button.setObjectName('add_tab_button')
        self.add_tab_button.setFixedSize(40, 40)
        self.add_tab_button.setIconSize(QSize(25, 19))
        self.add_tab_button.setToolTip('Создать новую вкладку (Ctrl + T)')
        self.add_tab_button.clicked.connect(lambda: self.create_tab(new_page))
        self.setCornerWidget(self.add_tab_button, Qt.Corner.TopLeftCorner)

    def set_tab_bar_position(self, position=None):
        if position is None:
            position = FS.get_option('TabBarPosition')
        if position == 'Сверху':
            self.setTabPosition(QTabWidget.North)
            self.add_tab_button.setStyleSheet('#add_tab_button {margin-bottom: 8px;}')
            self.window().panel.setFixedHeight(40)
        else:
            self.setTabPosition(QTabWidget.South)
            self.add_tab_button.setStyleSheet('#add_tab_button {margin-top: 8px;}')

    def create_tab(self, url: str = 'Пустая вкладка', title=None):
        page = BrowserPageWrapper(self)
        page.load(url)
        if title is not None:
            page.title = title
        self.addTab(page, page.title)
        self.setCurrentWidget(page)
        PagesObserver.add_page(page)
        self.tabBar().findChild(QAbstractButton).setToolTip('Закрыть вкладку (Ctrl + W)')
        return page.view

    def tab_changed(self):
        self.window().address_edit.setText(self.current().url)
        self.window().address_edit.setCursorPosition(0)
        self.window().set_title(self.current().title)
        self.window().check_state_bookmark()

    def close_tab(self, index):
        page = self.widget(index)
        if self.count() <= 1:  # если одна вкладка, то открывать сайт с заставкой
            page.load(new_page)
            return

        PagesObserver.remove_page(page)
        self.removeTab(index)

    def current(self) -> BrowserPageWrapper:
        return self.currentWidget()
