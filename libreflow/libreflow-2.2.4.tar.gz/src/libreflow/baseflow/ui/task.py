import time
from kabaret.app.ui.gui.widgets.flow.flow_view import QtWidgets, QtCore, QtGui, CustomPageWidget
from kabaret.app.ui.gui.widgets.flow_layout import FlowLayout
from kabaret.app import resources
from kabaret.app.ui.gui.icons import flow as _

from ...resources.icons import gui as _

from .controller import Controller
from .file import FileWidget
from .file_list import FileListsWidget


# Task page
# ----------------------


class TaskActionsButton(QtWidgets.QToolButton):
    """
    Holds the task's action shortcuts displayed in the task page header.
    """
    def __init__(self, flow_page, controller):
        super(TaskActionsButton, self).__init__()
        self.controller = controller
        self.flow_page = flow_page
        self.build()
    
    def build(self):
        self.setIcon(resources.get_icon(('icons.gui', 'menu')))
        self.setIconSize(QtCore.QSize(25, 25))
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.setFixedWidth(40)

        # Add actions
        self.menu = QtWidgets.QMenu('Task actions', self)

        for ta in self.controller.task_actions():
            a = self.menu.addAction(ta.label, lambda a=ta: self._on_action_menu_triggered(a))
            a.setIcon(resources.get_icon(ta.icon))
            a.setToolTip(ta.tooltip)
        
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.setArrowType(QtCore.Qt.NoArrow)
        self.setMenu(self.menu)

    def _on_action_menu_triggered(self, action):
        self.flow_page.show_action_dialog(action.oid)


class TaskBookmarkButton(QtWidgets.QToolButton):
    """
    Allows to add the task to the user's bookmarks
    """
    def __init__(self, flow_page, controller):
        super(TaskBookmarkButton, self).__init__()
        self.controller = controller
        self.flow_page = flow_page
        self.build()

        self.clicked.connect(self._on_button_triggered)
    
    def build(self):
        if self.controller.is_bookmarked():
            self.setIcon(resources.get_icon(('icons.gui', 'star')))
        else:
            self.setIcon(resources.get_icon(('icons.gui', 'star-1')))
        self.setIconSize(QtCore.QSize(25, 25))
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.setFixedWidth(40)

    def _on_button_triggered(self):
        self.controller.toggle_bookmark()
        self.build()


class TaskHeader(QtWidgets.QWidget):
    """
    Represents the header of the task widget, displaying the task's name and icon.
    """
    def __init__(self, controller, task_widget):
        super(TaskHeader, self).__init__()
        self.controller = controller
        self.task_oid = task_widget.oid
        self.flow_page = task_widget.page

        self.build()
    
    def build(self):
        folder, icon = self.controller.task_small_icon()
        self.label_icon = QtWidgets.QLabel()
        pm = resources.get_pixmap(folder, icon)
        self.label_icon.setPixmap(pm.scaled(28, 28, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.label_icon.setFixedWidth(40)
        self.label_icon.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setWeight(QtGui.QFont.Bold)
        self.label_name = QtWidgets.QLabel(self.controller.task_label())
        self.label_name.setFont(font)
        self.label_name.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.bookmark_button = TaskBookmarkButton(self.flow_page, self.controller)
        self.actions_button = TaskActionsButton(self.flow_page, self.controller)

        hlo = QtWidgets.QHBoxLayout()
        hlo.addWidget(self.label_icon)
        hlo.addWidget(self.label_name)
        hlo.addStretch(1)
        hlo.addWidget(self.bookmark_button)
        hlo.addWidget(self.actions_button)
        hlo.setMargin(0)
        hlo.setSpacing(1)
        self.setLayout(hlo)

        pal = self.palette()
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(self.controller.task_color()))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        
        self.setFixedHeight(40)


class TaskView(QtWidgets.QWidget):

    def __init__(self, controller, task_widget):
        super(TaskView, self).__init__()
        self.task_widget = task_widget
        self.controller = controller

        self.build()
    
    def build(self):
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.file_lists = FileListsWidget(self.task_widget, self.splitter)
        self.file_view = FileWidget(self.task_widget, self.splitter)
        self.file_view.setVisible(False)
        self.splitter.setSizes([100, 100])

        vlo = QtWidgets.QVBoxLayout()
        vlo.addWidget(self.splitter)
        vlo.setSpacing(1)
        vlo.setMargin(1)
        self.setLayout(vlo)


class TaskPageWidget(CustomPageWidget):

    def build(self):
        # TODO: Task header
        # TODO: File lists
        # TODO: File view
        #       - header
        #       - history
        # self.parent().layout().setStretch(1, 0)
        import time
        start = time.time()
        
        self.controller = Controller(self)
        self.header = TaskHeader(self.controller, self)
        self.view = TaskView(self.controller, self)
        
        vlo = QtWidgets.QVBoxLayout()
        vlo.addWidget(self.header)
        vlo.addWidget(self.view)
        vlo.setSpacing(0)
        vlo.setMargin(0)
        self.setLayout(vlo)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        print('Task widget built in %.3fs' % (time.time() - start))

        self.key_press_start_time = -1
    
    def on_touch_event(self, oid):
        self.controller.on_touch_event(oid)
    
    def sizeHint(self):
        return QtCore.QSize(2000, 2000)
    
    def keyPressEvent(self, event):
        super(TaskPageWidget, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Escape:
            # This will automatically reset the selected item in the controller
            # (see selectionChanged())
            self.controller.clear_selected()
        elif event.key() == QtCore.Qt.Key_Shift:
            self.controller.toggle_file_statutes()
            self.key_press_start_time =  time.time()

    def keyReleaseEvent(self, event):
        super(TaskPageWidget, self).keyReleaseEvent(event)
        key_press_time = time.time() - self.key_press_start_time

        if event.key() == QtCore.Qt.Key_Shift and key_press_time > 0.5:
            self.controller.toggle_file_statutes()


# Task list page
# ----------------------


STYLESHEET = '''QPushButton:focus { 
    outline: none; 
    }'''


class HtmlButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(HtmlButton, self).__init__(parent)

        self.clicked.connect(self._on_clicked)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

    def _on_context_menu(self):
        pass

    def _on_clicked(self):
        pass

    def set_html(self, html):
        text = QtGui.QTextDocument()
        text.setHtml(html)
        text.setTextWidth(text.size().width())

        pix = QtGui.QPixmap(text.size().width(), text.size().height())
        pix.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pix)
        text.drawContents(painter, QtCore.QRectF(pix.rect()))
        painter.end()

        icon = QtGui.QIcon(pix)
        self.setText("")
        self.setIcon(icon)
        self.setIconSize(pix.rect().size())

        margins = QtCore.QSize(10, 10)
        self.setFixedSize(pix.size() + margins)


class ItemButton(HtmlButton):
    def __init__(self, oid, page, name, enabled, icon, color, button_height=100):
        super(ItemButton, self).__init__(page)
        self.page = page
        self.oid = oid
        self.enabled = enabled

        html = """
        <center><img src="{pict}" height={height}>
        <h3>{name}</h3></center>
        """.format(
            **dict(
                pict=icon, height=button_height, name=name
            )
        )

        self.setStyleSheet('''QPushButton {
            background-color: ''' + color + '''
        }''')

        if enabled == '':
            self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
            self.opacity_effect.setOpacity(0.3)
            self.setGraphicsEffect(self.opacity_effect)
            palette = self.parent().palette().color(QtGui.QPalette.Dark).name()
            self.setStyleSheet('''QPushButton {
            background-color: ''' + color + '''
            }
            QPushButton::hover {
                border-color: ''' + palette + '''
            }''')

        self.set_html(html)

    def _on_clicked(self):
        if self.enabled == True:
            self.page.page.goto(self.oid)


class AddTaskDialog(QtWidgets.QDialog):

    def __init__(self, session, parent=None):
        super(AddTaskDialog, self).__init__(parent)
        self.session = session
        self.parent = parent

        self.setMinimumSize(0, 150)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(30, 3, 5, 3)
        self.layout.setSpacing(0)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Base, palette.color(QtGui.QPalette.Window))
        self.setPalette(palette)

        label = QtWidgets.QLabel('<h2>Create Task</h2>')
        label.setContentsMargins(0, 10, 5, 15)

        self.error_label = QtWidgets.QLabel()
        self.error_label.setContentsMargins(0, 0, 0, 15)

        input_widget = QtWidgets.QWidget()
        input_widget.setMaximumWidth(800)
        
        hlayout_input = QtWidgets.QHBoxLayout()
        hlayout_input.setContentsMargins(0, 0, 0, 8)
        hlayout_input.setSpacing(7)

        icon_lbl = QtWidgets.QLabel()
        icon = QtGui.QIcon(resources.get_icon(('icons.flow', 'input')))
        pixmap = icon.pixmap(QtCore.QSize(16, 16))
        icon_lbl.setPixmap(pixmap)
        icon_lbl.setAlignment(QtCore.Qt.AlignVCenter)
        
        title_lbl = QtWidgets.QLabel('Name')
        title_lbl.setAlignment(QtCore.Qt.AlignVCenter)

        self.txt_input = QtWidgets.QLineEdit()

        hlayout_input.addWidget(icon_lbl)
        hlayout_input.addWidget(title_lbl)
        hlayout_input.addWidget(self.txt_input)
        input_widget.setLayout(hlayout_input)

        buttons_widget = QtWidgets.QWidget()

        hlayout_buttons = QtWidgets.QHBoxLayout()
        hlayout_buttons.setContentsMargins(58, 0, 0, 0)
        hlayout_buttons.setSpacing(10)

        create_button = QtWidgets.QPushButton('Create')
        close_button = QtWidgets.QPushButton('Close')

        hlayout_buttons.addWidget(create_button)
        hlayout_buttons.addWidget(close_button)
        buttons_widget.setLayout(hlayout_buttons)

        self.layout.addWidget(label)
        self.layout.addWidget(input_widget)
        self.layout.addWidget(buttons_widget)
        
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)

        create_button.clicked.connect(self._on_create_button_clicked)
        close_button.clicked.connect(self._on_close_button_clicked)
    
    def sizeHint(self):
        return QtCore.QSize(300, 175)

    def _on_create_button_clicked(self):
        default_tasks = self.session.cmds.Flow.call(
            self.parent.oid, 'get_default_tasks', [False], {}
        )

        if self.txt_input.text().lower() not in default_tasks:
            widget = self.layout.itemAt(1).widget()
            self.error_label.setText('Not in default task')
            if isinstance(widget, type(self.error_label)) == False:
                self.layout.insertWidget(self.layout.count() - 2, self.error_label)
                return
        elif self.txt_input.text().lower() in self.parent.task_names:
            widget = self.layout.itemAt(1).widget()
            self.error_label.setText('Task already in the shot')
            if isinstance(widget, type(self.error_label)) == False:
                self.layout.insertWidget(self.layout.count() - 2, self.error_label)
                return
        else:
            self.session.cmds.Flow.set_value(oid=self.parent.oid + '/tasks' + '/add_task' + '/entity_name', value=self.txt_input.text().lower())
            self.session.cmds.Flow.run_action(oid=self.parent.oid + '/tasks' + '/add_task', button='Create')
            self.parent.refresh_tasks()
            self.close()
    
    def _on_close_button_clicked(self):
        self.close()


class TasksCustomWidget(CustomPageWidget):

    def build(self):
        self.task_names = []
        self.visibility_status = False

        grid = QtWidgets.QGridLayout()
        grid.setMargin(0)
        grid.setSpacing(0)
        self.setLayout(grid)
        self.setStyleSheet(STYLESHEET)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        grid.addWidget(scroll, 0, 0, 1, 4)

        scroll_elements = QtWidgets.QWidget()
        scroll.setWidget(scroll_elements)
        
        vlo = QtWidgets.QVBoxLayout()
        scroll_elements.setLayout(vlo)

        self.tasks_layout = FlowLayout()
        self.tasks_layout.setSpacing(6)
        vlo.addLayout(self.tasks_layout)

        self.button_height = 100

        self.refresh_tasks()
        
        self.button_visibility_toggle = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.libreflow', 'show'))), ''
        )
        self.button_visibility_toggle.setToolTip('Show disabled tasks')
        self.button_visibility_toggle.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.button_visibility_toggle.setFixedWidth(40)
        self.button_visibility_toggle.clicked.connect(self._on_visibility_toggle_button_clicked)

        button_add_task = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add_task.setToolTip('Add task')
        button_add_task.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add_task.setFixedWidth(40)
        button_add_task.clicked.connect(self._on_addtask_button_clicked)
        
        grid.setColumnStretch(1, 1)
        grid.addWidget(self.button_visibility_toggle, 1, 2)
        grid.addWidget(button_add_task, 1, 3)
    
    def sizeHint(self):
        return QtCore.QSize(300, 800)
    
    def refresh_tasks(self):
        self.task_names = []

        for i in reversed(range(self.tasks_layout.count())):
            self.tasks_layout.itemAt(i).widget().deleteLater()
        
        for item in self.session.cmds.Flow.get_mapped_oids(self.oid + '/tasks'):
            enabled = self.session.cmds.Flow.get_value(item + "/enabled")
            if enabled != True:
                if self.visibility_status == False:
                    continue
            
            label = self.session.cmds.Flow.call(item, 'get_display_name', [], {})
            icon_ref = self.session.cmds.Flow.call(item, 'get_icon', [], {})
            icon = resources.get(*icon_ref)
            color = self.session.cmds.Flow.call(item, 'get_color', [], {})
            b = ItemButton(item, self, label, enabled, icon, color, self.button_height)
            self.tasks_layout.addWidget(b)
            self.task_names.append(item.split('/')[-1].lower())
    
    def _on_visibility_toggle_button_clicked(self):
        if self.visibility_status == False:
            self.visibility_status = True
            self.button_visibility_toggle.setToolTip("Hide disabled tasks")
            self.button_visibility_toggle.setIcon(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'hide'))))
        else:
            self.visibility_status = False
            self.button_visibility_toggle.setToolTip("Show disabled tasks")
            self.button_visibility_toggle.setIcon(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'show'))))
        self.refresh_tasks()

    def _on_addtask_button_clicked(self):
        dialog_add_task = AddTaskDialog(self.session, self)
        dialog_add_task.exec()
