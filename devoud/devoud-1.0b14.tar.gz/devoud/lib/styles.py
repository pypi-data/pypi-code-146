from string import Template
from .svg import set_icon_color
import json


class Theme:
    def __init__(self, name=None):
        if name is None:
            from .devoud_data import FS
            self.current_theme = FS.get_option('theme')
        else:
            self.current_theme = name

        # стандартная тема
        self.title_buttons_color = {
            "min": "#1D1F2A",
            "max": "#1D1F2A",
            "close": "#aa2f2f"
        }

        self.bg = '#282A3A'
        self.fg = '#eef1f1'

        self.search_box = {
            'bg': '#515375',
            'fg': '#eef1f1',
            'item': '#1d1f2a'
        }

        self.address_edit = {
            'bg': '#1D1F2A',
            'fg': '#dfdfdf',
            'border': '#515375',
            'hover': '#515375'
        }

        self.button = {
            'bg': '#282a3a',
            'fg': '#eef1f1',
            'hover': '#3D3F59',
            'border': '#aa2f2f'
        }

        self.tab_widget = {
            "bg": "#282a3a",
            "fg": "#dfdfdf",
            "select_bg": "#515375",
            "select_fg": "#dfdfdf",
            "hover": "#3D3F59"
        }

        self.combobox = {
            'bg': '#515375',
            'fg': '#eef1f1',
            'select': '#515375',
            'item': '#3d3f59'
        }

        self.check_box = {
            'normal': '#1d1f2a',
            'checked': '#aa2f2f'
        }

        self.sections_panel = {
            'bg': '#1d1f2a',
            'fg': '#eef1f1',
            'select': '#515375',
            'hover': '#3D3F59'
        }

        self.widget = {
            'bg': '#363a4f',
            'fg': '#eef1f1'
        }

        self.widget_title = {
            'bg': '#1d1f2a',
            'fg': '#eef1f1',
            'alt_fg': '#b3b5b5'
        }

        self.widget_title_btn = {
            'bg': '#363a4f',
            'hover': '#515375'
        }

        self.progress_bar = {
            'fg': '#eef1f1',
            'chunk': '#aa2f2f',
            'border': '#515375'
        }

        self.import_theme()
        set_icon_color(self)

    def import_theme(self):
        try:
            with open(f"./ui/themes/{self.current_theme}.json", "r") as read_file:
                data = json.load(read_file)
        except FileNotFoundError:
            print('[Стили]: Файл темы не найден', self.current_theme)
            return

        self.title_buttons_color = data['title_buttons_color']
        self.bg = data['bg']
        self.fg = data['fg']
        self.search_box = data['search_box']
        self.address_edit = data['address_edit']
        self.button = data['button']
        self.tab_widget = data['tab_widget']
        self.combobox = data['combobox']
        self.check_box = data['check_box']
        self.sections_panel = data['sections_panel']
        self.widget = data['widget']
        self.widget_title = data['widget_title']
        self.widget_title_btn = data['widget_title_btn']
        self.progress_bar = data['progress_bar']

    def style(self):
        return Template("""
        #central_widget {
            background-color: transparent;
        }
        
        QWidget {
            background: $bg;
            outline: 0px;
            color: $fg;
            border: 0;
            font: 11pt "Clear Sans Medium";
        }
        
        QPushButton {
            background: transparent;
            border: none;
            border-radius: 6px;
        }
        
        QPushButton:hover {
            background: $button_hover_bg;
        }
        
        QPushButton:pressed {
            background: $button_hover_bg;
            border: 2px solid $button_pressed_border;
        }

        QPushButton::menu-indicator { 
            height: 0px;
            width: 0px;
        }
        
        #back_button {
            icon: url(./ui/custom/svg/arrow_left.svg);
        }
        
        #forward_button {
            icon: url(./ui/custom/svg/arrow_right.svg);
        }
        
        #update_button {
            icon: url(./ui/custom/svg/update.svg);
        }
        
        #home_button {
            icon: url(./ui/custom/svg/home.svg);
        }
        
        #menu_button {
            icon: url(./ui/custom/svg/options.svg);
        }
        
        QToolTip {
            background-color: $bg;
            color: $fg;
            font: 10pt "Clear Sans Medium";
            border: 2px solid $tool_tip_border;
            padding: 3px;
        }
        
        QLabel {
            background: transparent;
        }
        
        QComboBox {
            padding: 0px 13px 0px 13px;
            background: $combobox_bg;
            color: $combobox_fg;
            border-top-left-radius: 6px;
            border-bottom-left-radius: 6px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }

        QComboBox::drop-down {
            width: 0px;
        }

        QComboBox QAbstractItemView {
            border: 0px;
            border-radius: 0;
        }

        QComboBox:hover {
            background: $combobox_select;
        }

        #search_box {
            border: none;
            padding: 0px 13px 0px 13px;
            background: $search_box_bg;
            color: $search_box_fg;
            border-top-left-radius: 6px;
            border-bottom-left-radius: 6px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }
        
        #search_box QAbstractItemView {
            border: 0px;
            border-radius: 0px;
            background: $search_box_item;
        }
        
        #address_frame {
            background: $line_edit_bg;
            padding: 0;
            border-radius: 6px;
        }
        
        #address_frame QPushButton {
            border: none;
            background: transparent;
            border-top-right-radius: 6px;
            border-top-left-radius: 0px;
            border-bottom-right-radius: 6px;
            border-bottom-left-radius: 0px;
        }
        
        #address_frame QPushButton:hover {
            background: $line_edit_hover;
        }
        
        QLineEdit {
            background: $line_edit_bg;
            color: $line_edit_fg;
            padding-left: 5px;
            border-radius: 0;
            selection-background-color: $line_edit_border;
        }

        QLineEdit:focus {
            border: 2px solid $line_edit_border;
        }
        
        QProgressBar {
            border: 0;
        }

        QProgressBar::chunk {
            background: $progress_bar_chunk;
        }
        
        #embedded_widget_content {
            background: $embedded_widget_content_bg;
            border-bottom-right-radius: 6px;
            border-bottom-left-radius: 6px;
        }

        #embedded_widget_content QWidget {
            background: transparent;
            font: 12pt "Clear Sans Medium";
            color: $embedded_widget_content_fg;
        }

        #embedded_widget_content QLineEdit {
            border: 2px solid $line_edit_border;
            selection-background-color: $line_edit_border;
            border-radius: 6px;
            padding-left: 7px;
            padding-right: 7px;
            padding-bottom: 1px;
            font: 11pt "Clear Sans Medium";
            background: $line_edit_bg;
            color: $line_edit_fg;
        }

        #embedded_widget_content QComboBox {
            border: 0px;
            background: $combobox_bg;
            color: $combobox_fg;
            border-radius: 6px;
            padding: 0px 15px 0px 10px;
        }

        #embedded_widget_content QComboBox QAbstractItemView {
            border: 0px;
            border-radius: 0px;
            background: $combobox_item;
            selection-background-color: $combobox_select;
        }
        
        #embedded_widget_title {
            background: $embedded_widget_title_bg;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
            outline: 0px;
        }

        #embedded_widget_title_text {
            padding-top: 2px;
            padding-bottom: 2px;
            background: none;
            font: 16pt 'Clear Sans Medium';
            color: $embedded_widget_title_fg;
        }

        #embedded_widget_title QPushButton {
            border: 0px;
            border-radius: 6px;
            background: $embedded_widget_title_button_bg;
            font-size: 14px;
            padding: 2px;
        }
        
        #embedded_widget_title QPushButton:hover {
            background: $embedded_widget_title_button_hover;
        }
        
        #find_widget {
            border-radius: 0;
        }

        QCheckBox::indicator {
            background: $checkbox_indicator_normal;
            border-radius: 6px;
        }
        
        QCheckBox::indicator:checked {
            background: $checkbox_indicator_checked;
        }

        #find_widget_edit {
            background: $line_edit_bg;
            border-radius: 6px;
            padding: 4px;
        }

        #find_widget_previous_button {
            border-radius: 6px;
            padding: 4px;
            padding-right: 0px;
            padding-left: 0px;
            icon: url(./ui/custom/svg/arrow_left.svg)
        }

        #find_widget_next_button {
            border-radius: 6px;
            padding: 4px;
            padding-right: 0px;
            padding-left: 0px;
            icon: url(./ui/custom/svg/arrow_right.svg)
        }

        #find_widget_hide_button {
            border-radius: 6px;
            font-size: 14px;
            padding: 4px;
            padding-left: 6px;
            padding-right: 6px;
            background: $window_close_button;
            border: 0;
        }
        
        #title_label {
            margin-left: 12px;
            margin-top: 5px;
        }

        #hide_button, #maximize_button {
            border: 2px solid transparent;
            image: url(./ui/custom/svg/hide.svg);
        }

        #hide_button:hover, #maximize_button:hover {
            background: $window_min_button;
            border-radius: 6px;
        }

        #close_button {
            border: 2px solid transparent;
            image: url(./ui/custom/svg/close.svg);
        }

        #close_button:hover {
            background: $window_close_button;
            icon: none;
            border-radius: 6px;
        }
        
        #sections_panel {
            background: $sections_panel_bg;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            min-width: 50px;
            max-width: 50px;
        }

        #sections_panel::item {
            border-radius: 0;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }
        
        QListWidget {
            show-decoration-selected: 0;
        }

        QListWidget::item {
            padding-left: 10px;
            border: 0;
            border-radius: 6px;
        }

        QListWidget::item:hover {
            background: $sections_panel_hover;
            color: $tab_widget_select_fg;
        }

        QListWidget::item:selected {
            background: $sections_panel_select;
            border-radius: 6px;
        }
        
        #downloads_item QWidget {
            background: $embedded_widget_title_bg;
            border-radius: 6px;
            color: $embedded_widget_title_fg;
        }
        
        #downloads_item_info QLabel {
            color: $embedded_widget_title_alt_fg;
        }
        
        #downloads_item_open {
            icon: url(./ui/custom/svg/folder_open.svg);
        }
        
        #downloads_item_delete {
            icon: url(./ui/custom/svg/close_tab.svg);
        }
        
        #downloads_item QProgressBar {
            border: 2px solid $progress_bar_border;
            border-radius: 6px;
            text-align: center;
            color: $progress_bar_fg;
        }
        
        #downloads_item QProgressBar::chunk {
            border-radius: 3px;
        }
        
        QTabWidget {
            background: $tab_widget_bg;
            border: 0px;
            padding: 0px;
        }

        QTabWidget::tab-bar {
            left: 1px;
            right: 35px;
        }

        QTabBar::tab {
            margin: 4px;
            margin-top: 6px;
            margin-bottom: 5px;
            border-radius: 6px;
            min-width: 100px;
            max-width: 200px;
            color: $tab_widget_fg;
            padding: 5px;
        }

        QTabBar::tab:text {
            padding-left: 5px;
        }

        QTabWidget::pane {}

        QTabBar::tab:selected {
            background: $tab_widget_select_bg;
            color: $tab_widget_select_fg;
        }

        QTabBar::tab:!selected:hover {
            background: $tab_widget_hover_bg;
        }

        QTabBar::tab:!selected {
            background: $tab_widget_bg;
            color: $tab_widget_fg;
        }

        QTabBar QToolButton::right-arrow {
            image: url(./ui/custom/svg/arrow_right.svg);
        }

        QTabBar QToolButton::left-arrow {
            image: url(./ui/custom/svg/arrow_left.svg);
        }

        QTabBar::close-button {
            image: url(./ui/custom/svg/close_tab_alt.svg);
            background: $tab_widget_hover_bg;
            border-radius: 6px;
            margin-right: 3px;
            min-width 15px;
        }
        
        QTabBar::tear {
            image: none;
        }
        
        #add_tab_button {
            min-width: 25px;
            min-height: 25px;
            margin-top: 8px;
            margin-left: 10px;
            background: transparent;
            icon: url(./ui/custom/svg/add_tab.svg);
            border-radius: 6px;
        }

        #add_tab_button:hover {
            background: $button_hover_bg;
        }
        
        QScrollBar:horizontal {
                background: $sections_panel_bg;
                max-height: 11px;
                border-radius: 4px;
                margin-top: 3px;
        }
    
        QScrollBar::handle:horizontal {
                background-color: $checkbox_indicator_checked;
                min-width: 5px;
                border-radius: 4px;
        }
    
        QScrollBar::add-line:horizontal {
                border-image: url(:/qss_icons/rc/right_arrow_disabled.png);
        }
    
        QScrollBar::sub-line:horizontal {
                border-image: url(:/qss_icons/rc/left_arrow_disabled.png);
        }
    
        QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on {
                border-image: url(:/qss_icons/rc/right_arrow.png);
        }

        QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on {
                border-image: url(:/qss_icons/rc/left_arrow.png);
        }
    
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
                background: none;
        }
    
    
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
        }
    
        QScrollBar:vertical {
                background: $sections_panel_bg;
                max-width: 11px;
                border-radius: 4px;
                margin-left: 3px;
        }
    
        QScrollBar::handle:vertical {
                background-color: $checkbox_indicator_checked;
                min-height: 5px;
                border-radius: 4px;
        }
    
        QScrollBar::sub-line:vertical {
                border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
        }
    
        QScrollBar::add-line:vertical {
                border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
        }
    
        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {
                border-image: none;
        }
    
        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
                border-image: none;
        }
    
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
        }
    
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
        }
        
        QMenu {
            color: $context_menu_fg;
            background-color: $context_menu_bg;
            border: 2px solid $context_menu_border;
            border-radius: 6px;
        }

        QMenu::item {
            padding: 6px;
            padding-left: 6px;
            padding-right: 6px;
            background: transparent;
        }

        QMenu::item:selected {
            background: $context_menu_select_bg;
            border-radius: 3px;
        }

        QMenu::separator {
            background-color: $context_menu_border;
            height: 0.1em;
        }

        """).substitute(bg=self.bg,
                        fg=self.fg,
                        button_bg=self.button['bg'],
                        button_fg=self.button['fg'],
                        button_hover_bg=self.button['hover'],
                        button_pressed_border=self.button['border'],
                        combobox_bg=self.combobox['bg'],
                        combobox_fg=self.combobox['fg'],
                        combobox_item=self.combobox['item'],
                        combobox_select=self.combobox['select'],
                        checkbox_indicator_normal=self.check_box['normal'],
                        checkbox_indicator_checked=self.check_box['checked'],
                        search_box_bg=self.search_box['bg'],
                        search_box_fg=self.search_box['fg'],
                        search_box_item=self.search_box['item'],
                        line_edit_bg=self.address_edit['bg'],
                        line_edit_fg=self.address_edit['fg'],
                        line_edit_border=self.address_edit['border'],
                        line_edit_hover=self.address_edit['hover'],
                        progress_bar_fg=self.progress_bar['fg'],
                        progress_bar_chunk=self.progress_bar['chunk'],
                        progress_bar_border=self.progress_bar['border'],
                        embedded_widget_title_bg=self.widget_title['bg'],
                        embedded_widget_title_fg=self.widget_title['fg'],
                        embedded_widget_title_alt_fg=self.widget_title['alt_fg'],
                        embedded_widget_title_button_bg=self.widget_title_btn['bg'],
                        embedded_widget_title_button_hover=self.widget_title_btn['hover'],
                        embedded_widget_content_bg=self.widget['bg'],
                        embedded_widget_content_fg=self.widget['fg'],
                        window_close_button=self.title_buttons_color['close'],
                        window_min_button=self.title_buttons_color['min'],
                        tool_tip_border=self.address_edit['border'],
                        sections_panel_bg=self.sections_panel['bg'],
                        sections_panel_hover=self.sections_panel['hover'],
                        sections_panel_select=self.sections_panel['select'],
                        context_menu_fg=self.fg,
                        context_menu_bg=self.bg,
                        context_menu_border=self.search_box['bg'],
                        context_menu_select_bg=self.widget['bg'],
                        tab_widget_bg=self.tab_widget['bg'],
                        tab_widget_fg=self.tab_widget['fg'],
                        tab_widget_select_bg=self.tab_widget['select_bg'],
                        tab_widget_select_fg=self.tab_widget['select_fg'],
                        tab_widget_hover_bg=self.tab_widget['hover']
                        )
