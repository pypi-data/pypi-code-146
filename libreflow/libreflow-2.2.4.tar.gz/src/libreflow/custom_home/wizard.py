import ast
import os
import pprint
import re
import json
from pathlib import Path
from kabaret.app.ui.gui.widgets.flow.flow_view import (
    CustomPageWidget,
    QtWidgets,
    QtCore,
    QtGui,
)
from kabaret.app.actors.flow.utils import import_object
from kabaret.app import resources
from kabaret import flow

from ..resources.icons import gui as _, applications as _

from ..baseflow.runners import CHOICES_ICONS

STYLESHEET = '''QTextEdit, QLineEdit, QComboBox {
    max-width: 3840px;
    }
    QPushButton:disabled {
        background-color: rgba(255, 255, 255, 0);
        color: rgba(255, 255, 255, 50);
    }
    QPushButton::menu-indicator {
        width:0px;
    }'''


class LabelIcon(QtWidgets.QLabel):

    def __init__(self, icon=None):
        QtWidgets.QLabel.__init__(self, '')

        icon = QtGui.QIcon(resources.get_icon(icon))
        pixmap = icon.pixmap(QtCore.QSize(16, 16))
        self.setPixmap(pixmap)
        self.setAlignment(QtCore.Qt.AlignVCenter)


class LineEdit(QtWidgets.QLineEdit):

    def __init__(self, value=None, placeholder=None, options=None, mandatory=False, custom_widget=None, copy=False):
        QtWidgets.QLineEdit.__init__(self)
        self.copy = copy
        self.options = options
        self.mandatory = mandatory
        self.custom_widget = custom_widget

        if value != None:
            self.setText(value)
        if value == 'id':
            project_id = re.sub('\s+', '_', self.custom_widget.project_name.text().lower())
            self.setText(project_id)

        if placeholder != None:
            self.setPlaceholderText(placeholder)

        if options == 'password':
            self.setEchoMode(QtWidgets.QLineEdit.Password)
        if options == 'read':
            self.setReadOnly(True)
        if (
            options == 'type' or
            options == 'user' or
            options == 'working_site' or
            options == 'exchange_site' or
            options == 'default_task' or
            options == 'task_template' or
            options == 'project_name' or
            options == 'path' or
            mandatory
        ):
            self.editingFinished.connect(self.on_text_finish_edit)

        self.textChanged.connect(self.on_text_changed)

    def empty_check(self):
        if not self.text():
            self.setProperty('error', True)
            self.style().polish(self)
            error = '!!!\nERROR: This field must not be empty.'
            self.setToolTip(error)
            self.custom_widget.refresh_buttons()
            return True
        else:
            self.setProperty('error', False)
            self.style().polish(self)
            self.setToolTip('')
            self.custom_widget.refresh_buttons()
            return False

    def name_check(self):
        tree = None
        if self.options == 'project_name':
            input_type = "Project"
            tree = self.custom_widget.parent().tree
        if self.options == 'user':
            input_type = "User"
            tree = self.custom_widget.parent().tree
        if self.options == 'working_site' or self.options == 'exchange_site':
            input_type = "Site"
            tree = self.custom_widget.parent().tree
        if self.options == 'default_task':
            input_type = "Task"
            tree = self.custom_widget.parent().dft_tree
        if self.options == 'task_template':
            input_type = "Template"
            tree = self.custom_widget.parent().template_tree
        
        for i in range(tree.topLevelItemCount()):
            name = tree.topLevelItem(i).name
            if self.options == 'working_site' or self.options == 'exchange_site':
                name = name.split(' ⚠️')[0]
            if self.text() == name:
                self.setProperty('error', True)
                self.style().polish(self)
                error = '!!!\nERROR: {type} {text} already exists.'.format(
                    type=input_type, 
                    text=self.text()
                )
                self.setToolTip(error)
                return self.custom_widget.refresh_buttons()

        self.setProperty('error', False)
        self.style().polish(self)
        self.setToolTip('')
        self.custom_widget.refresh_buttons()

    def project_type_check(self):
        try:
            TYPE = import_object(self.text())
        except Exception as err:
            print('Error:%s' % (err,))
            self.setProperty('error', True)
            self.style().polish(self)
            self.setToolTip('!!!\nERROR: %s' % (err,))
            self.custom_widget.refresh_buttons()
        else:
            if not issubclass(TYPE, flow.Object):
                self.setProperty('error', True)
                self.style().polish(self)
                self.setToolTip('!!!\nERROR: Project type must be a subclass of Object')
            else:
                self.setProperty('error', False)
                self.style().polish(self)
                self.setToolTip('Project Type looks good:\n%s' % (TYPE,))
            self.custom_widget.refresh_buttons()

    def path_check(self):
        count = 0
        for i in range(self.custom_widget.content_layout.count()):
            widget = self.custom_widget.content_layout.itemAt(i).widget()
            if isinstance(widget, LineEdit) == False:
                continue
            if widget.text() == '':
                count = count + 1
        if count == 3:
            self.setProperty('error', True)
            self.style().polish(self)
            error = '!!!\nERROR: At least one path must be defined.'
            self.setToolTip(error)
            return self.custom_widget.refresh_buttons()
        else:
            for i in range(self.custom_widget.content_layout.count()):
                widget = self.custom_widget.content_layout.itemAt(i).widget()
                if isinstance(widget, LineEdit) == False:
                    continue
                widget.setProperty('error', False)
                widget.style().polish(widget)
                widget.setToolTip('')
            self.custom_widget.refresh_buttons()

    def on_text_changed(self):
        if self.copy:
            text = self.text().lower()
            text_id = re.sub('\s+', '_', text)
            self.custom_widget.input_id.setText(text_id)
        if self.options == 'underscore':
            original_text = self.text().lower()
            original_text = re.sub(r'[^a-zA-Z0-9_]+', '', original_text)
            underscore_text = re.sub('\s+', '_', original_text)
            self.setText(underscore_text)
        if self.options == 'digit':
            original_text = self.text()
            original_text = re.sub(r'[^0-9]+', '', original_text)
            self.setText(original_text)

    def on_text_finish_edit(self):
        if self.mandatory:
            empty = self.empty_check()
            if empty:
                return
        if (
            self.options == 'project_name' or
            self.options == 'user' or
            self.options == 'working_site' or
            self.options == 'exchange_site' or
            self.options == 'default_task' or
            self.options == 'task_template'
        ):
            self.name_check()
        if self.options == 'type':
            self.project_type_check()
        if self.options == 'path':
            self.path_check()


class ObjectGroup(QtWidgets.QWidget):

    def __init__(self, custom_widget, label=None, expanded=False):
        super(ObjectGroup, self).__init__(custom_widget)
        self.expanded = expanded

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.icon = QtWidgets.QLabel('')
        self.icon.setAlignment(QtCore.Qt.AlignVCenter)
        self.icon.mousePressEvent = self._on_label_mouse_press
        self.icon.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self.icon, 0, 0)

        label = QtWidgets.QLabel(label)
        label.mousePressEvent = self._on_label_mouse_press
        label.setStyleSheet('border: 1px solid palette(mid); padding: 5px;')
        layout.addWidget(label, 0, 1, 1, 2)

        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QGridLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_widget.setLayout(self.content_layout)

        layout.addWidget(self.content_widget, 1, 1)

        self.setLayout(layout)

        self.refresh()
    
    def refresh(self):
        if self.expanded == False:
            icon = QtGui.QIcon(resources.get_icon(('icons.flow', 'collapsed')))
            pixmap = icon.pixmap(QtCore.QSize(16, 16))
            self.icon.setPixmap(pixmap)
            self.content_widget.hide()
        else:
            icon = QtGui.QIcon(resources.get_icon(('icons.flow', 'expanded')))
            pixmap = icon.pixmap(QtCore.QSize(16, 16))
            self.icon.setPixmap(pixmap)
            self.content_widget.show()
    
    def _on_label_mouse_press(self, event):
        if self.expanded == False:
            self.expanded = True
        else:
            self.expanded = False
        self.refresh()


class RunnersChoiceValue(QtWidgets.QComboBox):

    def __init__(self, tree, item=None):
        QtWidgets.QComboBox.__init__(self)

        if item:
            for runner in tree.runners:
                if runner.runner_name() == item.text(0):
                    if runner.runner_icon() != None:
                        icon = QtGui.QIcon(resources.get_icon(runner.runner_icon()))
                        icon.addPixmap(icon.pixmap(QtCore.QSize(16, 16)), QtGui.QIcon.Disabled)
                        self.addItem(icon, runner.runner_name())
                    else:
                        self.addItem(runner.runner_name())
        else:
            for runner in tree.runners:
                exist = False
                for i in range(tree.topLevelItemCount()):
                    if tree.topLevelItem(i).text(0) == runner.runner_name():
                        exist = True
                        break
                if exist == False:
                    if runner.runner_icon() != None:
                        self.addItem(QtGui.QIcon(resources.get_icon(runner.runner_icon())), runner.runner_name())
                    else:
                        self.addItem(runner.runner_name())


class CurrentExchangeSite(QtWidgets.QComboBox):

    def __init__(self, page_widget):
        QtWidgets.QComboBox.__init__(self)
        self.page_widget = page_widget

        self.refresh()
    
    def refresh(self):
        self.clear()
        exchange_sites = []
        for i in range(self.page_widget.tree.topLevelItemCount()):
            exchange_sites.append(self.page_widget.tree.topLevelItem(i).name)

        for site in exchange_sites:
            if '⚠️' in site:
                continue
            self.addItem(site)
        
        self.setCurrentText(self.page_widget.parent().get_exchange_site(self.page_widget.parent().project_selected).name())


class SetupStep(QtWidgets.QLabel):
    
    def __init__(self, text=None, subgroup=None):
        QtWidgets.QLabel.__init__(self, text)
        step = re.sub(re.compile('<.*?>'), '', text)

        self.setObjectName(step)

        if subgroup == True:
            self.setContentsMargins(15, 0, 0, 0)


class SetupSteps(QtWidgets.QWidget):

    def __init__(self, homepage_widget):
        super(SetupSteps, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(5)

        self.layout.addStretch()
        self.layout.addWidget(SetupStep('<h2>Project</h2>'))
        self.layout.addWidget(SetupStep('<h3>Global settings</h3>', True))
        self.layout.addWidget(SetupStep('<h3>MongoDB</h3>', True))
        self.layout.addWidget(SetupStep('<h3>Kitsu</h3>', True))
        self.layout.addWidget(SetupStep('<h3>Users</h3>', True))
        self.layout.addWidget(SetupStep('<h3>Working sites</h3>', True))
        self.layout.addWidget(SetupStep('<h3>Files</h3>', True))
        self.layout.addWidget(SetupStep('<h3>Tasks</h3>', True))
        self.layout.addStretch()

        self.setLayout(self.layout)

    def refresh(self, page_name=None):
        if page_name is None:
            page_name = self.homepage_widget.layout().itemAt(2).widget().objectName()
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                if widget.objectName() == page_name or widget.objectName() == 'Project':
                    widget.setStyleSheet('color: white')
                else:
                    widget.setStyleSheet('color: rgba(255, 255, 255, 75)')


class WizardPage(QtWidgets.QWidget):

    def __init__(self, homepage_widget):
        super(WizardPage, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget

        layout = QtWidgets.QVBoxLayout()

        self.content_layout = QtWidgets.QVBoxLayout()

        # Buttons
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch()

        self.label_feedback = QtWidgets.QLabel('')
        self.button_back = QtWidgets.QPushButton('Back')
        self.button_next = QtWidgets.QPushButton('Next')
        self.button_cancel = QtWidgets.QPushButton('Cancel')

        self.button_back.clicked.connect(self._on_back_button_clicked)
        self.button_next.clicked.connect(self._on_next_button_clicked)
        self.button_cancel.clicked.connect(self._on_cancel_button_clicked)

        self.button_layout.addWidget(self.label_feedback)
        self.button_layout.addWidget(self.button_back)
        self.button_layout.addWidget(self.button_next)
        self.button_layout.addWidget(self.button_cancel)

        # Page setup
        layout.addLayout(self.content_layout)
        layout.addLayout(self.button_layout)
        self.setLayout(layout)

    def _on_back_button_clicked(self):
        pass

    def _on_next_button_clicked(self):
        pass

    def _on_cancel_button_clicked(self):
        self.homepage_widget.page.goto('/Home')


class WizardDialog(QtWidgets.QDialog):

    def __init__(self, page_widget):
        super(WizardDialog, self).__init__(page_widget)
        self.page_widget = page_widget
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.preset_type = ''

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20,20,20,20)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Base, palette.color(QtGui.QPalette.Window))
        self.setPalette(palette)

        self.content_layout = QtWidgets.QGridLayout()
        self.content_layout.setAlignment(QtCore.Qt.AlignTop)

        # Buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        self.button_presets = QtWidgets.QPushButton('Presets')
        self.button_action = QtWidgets.QPushButton('')
        self.button_cancel = QtWidgets.QPushButton('Cancel')

        self.button_action.clicked.connect(self._on_action_button_clicked)
        self.button_cancel.clicked.connect(self._on_cancel_button_clicked)

        self.button_action.setAutoDefault(False)
        self.button_cancel.setAutoDefault(False)

        self.import_action = QtWidgets.QAction('Import', self)
        self.export_action = QtWidgets.QAction('Export', self)
        
        self.import_action.triggered.connect(self._on_import_triggered)
        self.export_action.triggered.connect(self._on_export_triggered)
        
        self.presets_menu = QtWidgets.QMenu()
        self.presets_menu.addAction(self.import_action)
        self.presets_menu.addAction(self.export_action)
        self.button_presets.setMenu(self.presets_menu)

        self.button_layout.addWidget(self.button_presets)
        self.button_presets.hide()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.button_action)
        self.button_layout.addWidget(self.button_cancel)

        self.layout.addLayout(self.content_layout)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def _on_import_triggered(self):
        root = self.page_widget.parent().get_root(self.page_widget.parent().project_selected)
        if root is None:
            root = str(Path.home())
        
        path = QtWidgets.QFileDialog().getOpenFileName(self, 'Open File', dir=root, filter='JSON (*.json)')
        if path[0] == '':
            return {}
        
        f = open(path[0], 'r')
        presetJSON = json.load(f)

        for key in presetJSON:
            if key == 'preset_type':
                if presetJSON[key] != self.preset_type:
                    print('Wrong JSON preset')
                    break
            for i in range(self.content_layout.count()):
                widget = self.content_layout.itemAt(i).widget()
                if widget.objectName() == key:
                    if isinstance(widget, LineEdit):
                        widget.setText(presetJSON[key])
                    if isinstance(widget, QtWidgets.QComboBox):
                        widget.setCurrentText(presetJSON[key])
                    if isinstance(widget, QtWidgets.QCheckBox):
                        widget.setChecked(presetJSON[key])
                    if isinstance(widget, ObjectGroup):
                        values = presetJSON[key]
                        for v in values:
                            for index in range(widget.content_layout.count()):
                                group_widget = widget.content_layout.itemAt(index).widget()
                                if group_widget.objectName() == v:
                                    if isinstance(group_widget, LineEdit):
                                        group_widget.setText(values[v])
        
        return presetJSON

    def _on_export_triggered(self):
        presetJSON = {}
        presetJSON['preset_type'] = self.preset_type
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if widget.objectName() != '':
                if isinstance(widget, LineEdit):
                    presetJSON[widget.objectName()] = widget.text()
                if isinstance(widget, QtWidgets.QComboBox):
                    presetJSON[widget.objectName()] = widget.currentText()
                if isinstance(widget, QtWidgets.QCheckBox):
                    presetJSON[widget.objectName()] = widget.isChecked()
                if isinstance(widget, QtWidgets.QTreeWidget):
                    items = {}
                    for index in range(widget.topLevelItemCount()):
                        properties = vars(widget.topLevelItem(index))
                        properties = {k: v for k, v in properties.items() if type(v) == str or type(v) == bool}
                        items[index] = properties
                    presetJSON[widget.objectName()] = items
                if isinstance(widget, ObjectGroup):
                    inputs = {}
                    for index in range(widget.content_layout.count()):
                        group_widget = widget.content_layout.itemAt(index).widget()
                        if isinstance(group_widget, LineEdit):
                            inputs[group_widget.objectName()] = group_widget.text()
                    presetJSON[widget.objectName()] = inputs

        json_object = json.dumps(presetJSON, indent=4)

        root = self.page_widget.parent().get_root(self.page_widget.parent().project_selected)
        if root is None:
            root = str(Path.home())

        path = QtWidgets.QFileDialog().getSaveFileName(
            self,
            'Save File',
            dir=root + '/' + self.preset_type,
            filter='JSON (*.json)'
        )
        if path[0] != '':
            with open(path[0], "w") as outfile:
                outfile.write(json_object)

    def _on_action_button_clicked(self):
        pass

    def _on_cancel_button_clicked(self):
        self.close()


class AddProject(WizardDialog):

    def __init__(self, page_widget):
        super(AddProject, self).__init__(page_widget)
        self.button_action.setEnabled(False)

        self.content_layout.addWidget(LabelIcon(('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Name'), 0, 1, QtCore.Qt.AlignVCenter)
        self.project_name = LineEdit(placeholder='Cool project', options='project_name', mandatory=True, custom_widget=self, copy=True)
        self.content_layout.addWidget(self.project_name, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Type'), 1, 1, QtCore.Qt.AlignVCenter)
        self.project_type = LineEdit(value='libreflow.baseflow.Project', options='type', mandatory=True, custom_widget=self)
        self.content_layout.addWidget(self.project_type, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Project ID'), 2, 1, QtCore.Qt.AlignVCenter)
        self.input_id = LineEdit(value='id', placeholder='cool_project', options='underscore', mandatory=True, custom_widget=self)
        self.content_layout.addWidget(self.input_id, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Thumbnail'), 3, 1, QtCore.Qt.AlignVCenter)
        self.project_thumbnail = QtWidgets.QTextEdit('')
        self.project_thumbnail.setPlaceholderText('data:image/png;base64')
        self.content_layout.addWidget(self.project_thumbnail, 3, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Add')
    
    def sizeHint(self):
        return QtCore.QSize(600, 400)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit) == False:
                    continue
                if widget.property('error') == True or (widget.mandatory and widget.text() == ''):
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_action_button_clicked(self):
        check = True
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit) == False:
                    continue
                if widget.mandatory and widget.text() == '':
                    widget.setProperty('error', True)
                    widget.style().polish(widget)
                    error = '!!!\nERROR: This field must not be empty.'
                    widget.setToolTip(error)
                    self.refresh_buttons()
                    check = False
        
        if check:
            self.page_widget.parent().session.get_actor("Flow").create_project(
                self.input_id.text(), self.project_type.text()
            )
            self.page_widget.tree.refresh()
            self.page_widget.parent().set_project_name(self.input_id.text(), self.project_name.text())
            self.page_widget.parent().set_project_thumbnail(self.input_id.text(), self.project_thumbnail.toPlainText())
            self.close()


class EditProject(WizardDialog):

    def __init__(self, page_widget, item_name):
        super(EditProject, self).__init__(page_widget)
        self.item_name = item_name

        self.content_layout.addWidget(LabelIcon(('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Name'), 0, 1, QtCore.Qt.AlignVCenter)
        self.project_name = LineEdit(value=self.page_widget.parent().get_project_name(item_name), placeholder='Cool project', mandatory=True, custom_widget=self)
        self.content_layout.addWidget(self.project_name, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Thumbnail'), 1, 1, QtCore.Qt.AlignVCenter)
        self.project_thumbnail = QtWidgets.QTextEdit(self.page_widget.parent().get_project_thumbnail(item_name))
        self.project_thumbnail.setPlaceholderText('data:image/png;base64')
        self.content_layout.addWidget(self.project_thumbnail, 1, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Edit')
    
    def sizeHint(self):
        return QtCore.QSize(600, 330)
    
    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit) == False:
                    continue
                if widget.property('error') == True or (widget.mandatory and widget.text() == ''):
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_action_button_clicked(self):
        check = True
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit) == False:
                    continue
                if widget.mandatory and widget.text() == '':
                    widget.setProperty('error', True)
                    widget.style().polish(widget)
                    error = '!!!\nERROR: This field must not be empty.'
                    widget.setToolTip(error)
                    self.refresh_buttons()
                    check = False

        if check:
            self.page_widget.parent().set_project_name(self.item_name, self.project_name.text())
            self.page_widget.parent().set_project_thumbnail(self.item_name, self.project_thumbnail.toPlainText())
            self.page_widget.tree.refresh()
            self.close()


class ProjectItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, name, status):
        super(ProjectItem, self).__init__(tree)
        self.name = name
        self.status = status
        self.display_name = tree.page_widget.parent().get_project_name(name)

        self.refresh()
  
    def refresh(self):
        self.setIcon(0, self.get_icon(('icons.gui', 'team')))
        self.setText(0, self.display_name)
        self.setIcon(1, self.get_icon(('icons.status', self.status)))
        self.setText(1, self.status)
    
    @staticmethod
    def get_icon(icon_ref):
        return QtGui.QIcon(resources.get_icon(icon_ref))


class ProjectsList(QtWidgets.QTreeWidget):

    def __init__(self, page_widget):
        super(ProjectsList, self).__init__()
        self.page_widget = page_widget

        self.setHeaderLabels(self.get_columns())
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setStyleSheet('''QTreeView::item:selected {
            background-color: #223e55;
            color: white;
            }'''
        )
        self.setRootIsDecorated(False)
        
        self.refresh()

        self.selectionModel().selectionChanged.connect(self.on_item_select)
        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)

    def get_columns(self):
        return ('Name', 'Status', '')

    def refresh(self):
        self.blockSignals(True)
        self.clear()

        for name, infos in self.page_widget.parent().get_projects():
            if infos['status'] == 'Archived':
                continue

            item = ProjectItem(self, name, infos['status'])

            self.setItemWidget(item, 2, EditItemButton(self.page_widget, item.name, 'Project'))

        self.resizeColumnToContents(0)
        self.blockSignals(False)
    
    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.setCurrentItem(None)
        super(ProjectsList, self).mousePressEvent(event)

    def on_item_select(self, selected, deselected):
        for index in selected.indexes():
            self.page_widget.button_next.setEnabled(True)
        for index in deselected.indexes():
            if selected.indexes() == []:
                self.page_widget.button_next.setEnabled(False)


class GlobalSettings(WizardPage):

    def __init__(self, homepage_widget):
        super(GlobalSettings, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget
        self.setObjectName('Global settings')

        self.button_back.hide()
        self.button_next.setEnabled(False)

        list_widget = QtWidgets.QWidget()
        list_layout = QtWidgets.QGridLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_widget.setLayout(list_layout)

        self.tree = ProjectsList(self)
        list_layout.addWidget(self.tree, 0, 0, 2, 0)
        
        button_add = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add.clicked.connect(self._on_add_button_clicked)
        list_layout.addWidget(button_add, 1, 0, QtCore.Qt.AlignRight)

        self.content_layout.addWidget(list_widget)

    def _on_add_button_clicked(self):
        dialog = AddProject(self)
        dialog.exec()
    
    def _on_next_button_clicked(self):
        self.homepage_widget.project_selected = self.tree.currentItem().name
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        next_page = MongoDBServer(self.homepage_widget)
        self.homepage_widget.layout().addWidget(next_page, 3)
        self.homepage_widget.setup_steps.refresh(next_page.objectName())


class MongoDBServer(WizardPage):

    def __init__(self, homepage_widget):
        super(MongoDBServer, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget
        self.setObjectName('MongoDB')

        self.entity_store = self.homepage_widget.get_entity_store(self.homepage_widget.project_selected).oid()

        inputs_widget = QtWidgets.QWidget()
        self.inputs_layout = QtWidgets.QGridLayout()
        self.inputs_layout.setContentsMargins(0, 0, 0, 0)
       
        self.inputs_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.inputs_layout.addWidget(QtWidgets.QLabel('URI Oid'), 0, 1, QtCore.Qt.AlignVCenter)

        root_oid_input = LineEdit(value=re.match(r'^/[^/]*/', self.entity_store).group(0), options='read')
        root_oid_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.inputs_layout.addWidget(root_oid_input, 0, 2, QtCore.Qt.AlignVCenter)
        uri_oid_input = LineEdit(value=self.entity_store.replace(root_oid_input.text(), '') + '/uri', mandatory=True, custom_widget=self)
        self.inputs_layout.addWidget(uri_oid_input, 0, 3, QtCore.Qt.AlignVCenter)

        self.inputs_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.inputs_layout.addWidget(QtWidgets.QLabel('URI'), 1, 1, QtCore.Qt.AlignVCenter)
        self.uri = LineEdit(
            value=self.homepage_widget.session.cmds.Flow.get_value(self.entity_store + '/uri'),
            placeholder='mongodb://[username:password@]host1[:port1]',
            mandatory=True,
            custom_widget=self
        )
        self.inputs_layout.addWidget(self.uri, 1, 2, 1, 2, QtCore.Qt.AlignVCenter)

        if self.uri.text() == '':
            self.button_next.setEnabled(False)

        inputs_widget.setLayout(self.inputs_layout)

        self.content_layout.addStretch()
        self.content_layout.addWidget(inputs_widget)
        self.content_layout.addStretch()

    def refresh_buttons(self):
        for i in reversed(range(self.inputs_layout.count())):
            widget = self.inputs_layout.itemAt(i).widget()
            if widget:
                if widget.property('error') == True:
                    return self.button_next.setEnabled(False)
        
        return self.button_next.setEnabled(True)

    def _on_back_button_clicked(self):
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        back_page = GlobalSettings(self.homepage_widget)
        self.homepage_widget.layout().addWidget(back_page, 3)
        self.homepage_widget.setup_steps.refresh(back_page.objectName())

    def _on_next_button_clicked(self):
        self.homepage_widget.set_db_uri(self.entity_store, self.uri.text())
        self.label_feedback.setText('Checking...')
        QtWidgets.QApplication.processEvents()
        QtWidgets.QApplication.processEvents()

        try:
            info = self.homepage_widget.get_db_info(self.entity_store)
        except Exception as err:
            self.uri.setProperty('error', True)
            self.uri.style().polish(self.uri)
            self.uri.setToolTip('!!!\nCONNECTION ERROR: %s' % (err,))
            self.label_feedback.setText('')
        else:
            print('Connection looks OK')
            pprint.pprint(info)
            self.homepage_widget.layout().itemAt(2).widget().deleteLater()
            next_page = Kitsu(self.homepage_widget)
            self.homepage_widget.layout().addWidget(next_page, 3)
            self.homepage_widget.setup_steps.refresh(next_page.objectName())


class Kitsu(WizardPage):

    def __init__(self, homepage_widget):
        super(Kitsu, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget
        self.setObjectName('Kitsu')

        self.kitsu_config = self.homepage_widget.get_kitsu_config(self.homepage_widget.project_selected).oid()

        inputs_widget = QtWidgets.QWidget()
        self.inputs_layout = QtWidgets.QGridLayout()
        self.inputs_layout.setContentsMargins(0, 0, 0, 0)
       
        self.inputs_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.inputs_layout.addWidget(QtWidgets.QLabel('Server URL'), 0, 1, QtCore.Qt.AlignVCenter)
        self.server_url = LineEdit(mandatory=True, custom_widget=self)
        self.server_url.setText(self.homepage_widget.session.cmds.Flow.get_value(self.kitsu_config + '/server_url'))
        self.inputs_layout.addWidget(self.server_url, 0, 2, QtCore.Qt.AlignVCenter)

        self.inputs_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.inputs_layout.addWidget(QtWidgets.QLabel('Project name'), 1, 1, QtCore.Qt.AlignVCenter)
        self.project_name = LineEdit(mandatory=True, custom_widget=self)
        self.project_name.setText(self.homepage_widget.session.cmds.Flow.get_value(self.kitsu_config + '/project_name'))
        self.inputs_layout.addWidget(self.project_name, 1, 2, QtCore.Qt.AlignVCenter)

        if self.server_url.text() == '' or self.project_name.text() == '':
            self.button_next.setEnabled(False)

        self.inputs_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.inputs_layout.addWidget(QtWidgets.QLabel('Uploadable files'), 2, 1, QtCore.Qt.AlignVCenter)
        self.uploadable_files = LineEdit(placeholder='*.extension')
        self.uploadable_files.setText(self.homepage_widget.session.cmds.Flow.get_value(self.kitsu_config + '/uploadable_files'))
        self.inputs_layout.addWidget(self.uploadable_files, 2, 2, QtCore.Qt.AlignVCenter)

        inputs_widget.setLayout(self.inputs_layout)

        self.content_layout.addStretch()
        self.content_layout.addWidget(inputs_widget)
        self.content_layout.addStretch()

    def refresh_buttons(self):
        for i in reversed(range(self.inputs_layout.count())):
            widget = self.inputs_layout.itemAt(i).widget()
            if widget:
                if widget.property('error') == True:
                    return self.button_next.setEnabled(False)
        
        return self.button_next.setEnabled(True)

    def _on_back_button_clicked(self):
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        back_page = MongoDBServer(self.homepage_widget)
        self.homepage_widget.layout().addWidget(back_page, 3)
        self.homepage_widget.setup_steps.refresh(back_page.objectName())

    def _on_next_button_clicked(self):
        self.homepage_widget.session.cmds.Flow.set_value(
            self.kitsu_config + '/server_url', self.server_url.text()
        )
        self.homepage_widget.session.cmds.Flow.set_value(
            self.kitsu_config + '/project_name', self.project_name.text()
        )
        self.homepage_widget.session.cmds.Flow.set_value(
            self.kitsu_config + '/uploadable_files', self.uploadable_files.text()
        )

        self.label_feedback.setText('Checking...')
        QtWidgets.QApplication.processEvents()
        QtWidgets.QApplication.processEvents()

        host_valid = self.homepage_widget.update_kitsu_host(self.homepage_widget.project_selected, self.server_url.text())

        if host_valid == False:
            self.server_url.setProperty('error', True)
            self.server_url.style().polish(self.server_url)
            self.server_url.setToolTip('!!!\nERROR: Host is not valid')
            self.label_feedback.setText('')
            self.refresh_buttons()
            return

        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        next_page = UsersConfig(self.homepage_widget)
        self.homepage_widget.layout().addWidget(next_page, 3)
        self.homepage_widget.setup_steps.refresh(next_page.objectName())


class AddUser(WizardDialog):

    def __init__(self, page_widget):
        super(AddUser, self).__init__(page_widget)
        self.button_action.setEnabled(False)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('ID'), 0, 1, QtCore.Qt.AlignVCenter)
        self.user_id = LineEdit(options="user", mandatory=True, custom_widget=self)
        self.user_id.setObjectName('user_id')
        self.content_layout.addWidget(self.user_id, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Login'), 1, 1, QtCore.Qt.AlignVCenter)
        self.user_login = LineEdit(mandatory=True, custom_widget=self)
        self.user_login.setObjectName('user_login')
        self.content_layout.addWidget(self.user_login, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Kitsu login'), 2, 1, QtCore.Qt.AlignVCenter)
        self.user_kitsu_login = LineEdit(mandatory=True, custom_widget=self)
        self.user_kitsu_login.setObjectName('user_kitsu_login')
        self.content_layout.addWidget(self.user_kitsu_login, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Status'), 3, 1, QtCore.Qt.AlignVCenter)
        self.user_status = QtWidgets.QComboBox()
        self.user_status.addItem('User')
        self.user_status.addItem('Admin')
        self.user_status.addItem('Supervisor')
        self.user_status.setObjectName('user_status')
        self.content_layout.addWidget(self.user_status, 3, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Add')
    
    def sizeHint(self):
        return QtCore.QSize(250, 165)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if widget.property('error') == True:
                    return self.button_action.setEnabled(False)
                if isinstance(widget, LineEdit):
                    if not widget.text():
                        return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_action_button_clicked(self):
        self.page_widget.parent().add_user(
            self.page_widget.parent().project_selected,
            self.user_id.text(),
            self.user_login.text(),
            self.user_kitsu_login.text(),
            self.user_status.currentText()
        )

        self.page_widget.tree.refresh()
        self.close()


class EditUser(WizardDialog):

    def __init__(self, page_widget, item_oid):
        super(EditUser, self).__init__(page_widget)
        self.item_oid = item_oid

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Login'), 0, 1, QtCore.Qt.AlignVCenter)
        self.user_login = LineEdit(mandatory=True, custom_widget=self)
        self.user_login.setObjectName('user_login')
        self.user_login.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/login'))
        self.content_layout.addWidget(self.user_login, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Kitsu login'), 1, 1, QtCore.Qt.AlignVCenter)
        self.user_kitsu_login = LineEdit(mandatory=True, custom_widget=self)
        self.user_kitsu_login.setObjectName('user_kitsu_login')
        self.user_kitsu_login.setText(self.page_widget.parent().get_user_kitsu_login(item_oid))
        self.content_layout.addWidget(self.user_kitsu_login, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Status'), 2, 1, QtCore.Qt.AlignVCenter)
        self.user_status = QtWidgets.QComboBox()
        self.user_status.addItem('User')
        self.user_status.addItem('Admin')
        self.user_status.addItem('Supervisor')
        self.user_status.setObjectName('user_status')
        self.user_status.setCurrentText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/status'))
        self.content_layout.addWidget(self.user_status, 2, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Edit')
    
    def sizeHint(self):
        return QtCore.QSize(250, 135)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if widget.property('error') == True:
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_action_button_clicked(self):
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/login', self.user_login.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/status', self.user_status.currentText()
        )
        self.page_widget.parent().set_user_kitsu_login(
            self.item_oid, self.user_kitsu_login.text()
        )

        self.page_widget.tree.refresh()
        self.close()


class UserItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, user_id, login, icon):
        super(UserItem, self).__init__(tree)
        self.name = user_id
        self.user_id = user_id
        self.login = login
        self.icon = icon

        self.refresh()
  
    def refresh(self):
        self.setIcon(0, self.get_icon(self.icon))
        self.setText(0, self.user_id)
        self.setText(1, self.login)
    
    @staticmethod
    def get_icon(icon_ref):
        return QtGui.QIcon(resources.get_icon(icon_ref))


class UsersList(QtWidgets.QTreeWidget):

    def __init__(self, page_widget):
        super(UsersList, self).__init__()
        self.page_widget = page_widget

        self.setHeaderLabels(self.get_columns())
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setStyleSheet('''QTreeView::item:selected {
            background-color: #223e55;
            color: white;
            }'''
        )
        self.setRootIsDecorated(False)
        
        self.refresh()

        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
    
    def get_columns(self):
        return ('ID', 'Login')

    def refresh(self):
        self.blockSignals(True)
        self.clear()

        users = self.page_widget.parent().get_users(self.page_widget.parent().project_selected)
        users_infos = self.page_widget.parent().session.cmds.Flow.get_mapped_rows(users.oid())

        for user in users_infos:
            item = UserItem(self, user[1]['ID'], user[1]['Login'], user[1]['_style']['icon'])

            self.setItemWidget(item, 1, EditItemButton(self.page_widget, user[0], 'User'))

        self.blockSignals(False)
    
    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.setCurrentItem(None)
        super(UsersList, self).mousePressEvent(event)


class UsersConfig(WizardPage):

    def __init__(self, homepage_widget):
        super(UsersConfig, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget
        self.setObjectName('Users')

        list_widget = QtWidgets.QWidget()
        list_layout = QtWidgets.QGridLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_widget.setLayout(list_layout)

        self.tree = UsersList(self)
        list_layout.addWidget(self.tree, 0, 0, 2, 0)
        
        button_add = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add.clicked.connect(self._on_add_button_clicked)
        list_layout.addWidget(button_add, 1, 0, QtCore.Qt.AlignRight)

        self.content_layout.addWidget(list_widget)

    def _on_add_button_clicked(self):
        dialog = AddUser(self)
        dialog.exec()

    def _on_back_button_clicked(self):
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        back_page = Kitsu(self.homepage_widget)
        self.homepage_widget.layout().addWidget(back_page, 3)
        self.homepage_widget.setup_steps.refresh(back_page.objectName())

    def _on_next_button_clicked(self):
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        next_page = WorkingSites(self.homepage_widget)
        self.homepage_widget.layout().addWidget(next_page, 3)
        self.homepage_widget.setup_steps.refresh(next_page.objectName())


class AddApplication(WizardDialog):

    def __init__(self, tree):
        super(AddApplication, self).__init__(tree)
        self.tree = tree
        self.button_action.setEnabled(False)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Runner'), 0, 1, QtCore.Qt.AlignVCenter)
        self.runner = RunnersChoiceValue(self.tree)
        self.runner.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_layout.addWidget(self.runner, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Windows'), 1, 1, QtCore.Qt.AlignVCenter)
        self.windows_path = LineEdit(placeholder='C:\Program Files', options='path', custom_widget=self)
        self.content_layout.addWidget(self.windows_path, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Linux'), 2, 1, QtCore.Qt.AlignVCenter)
        self.linux_path = LineEdit(placeholder='/opt', options='path', custom_widget=self)
        self.content_layout.addWidget(self.linux_path, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Darwin'), 3, 1, QtCore.Qt.AlignVCenter)
        self.darwin_path = LineEdit(placeholder='/Applications', options='path', custom_widget=self)
        self.content_layout.addWidget(self.darwin_path, 3, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Add')
    
    def sizeHint(self):
        return QtCore.QSize(600, 212)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if widget.property('error') == True:
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)
    
    def _on_action_button_clicked(self):
        variable = self.runner.currentText().upper() + '_EXEC_PATH'
        item = ApplicationItem(
            self.tree,
            'NEW',
            variable,
            self.windows_path.text(),
            self.linux_path.text(),
            self.darwin_path.text()
        )
        item.setForeground(0, QtGui.QBrush(QtGui.QColor(100, 221, 80)))
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 1, EditItemButton(self.tree, item, 'Application'))
        self.tree.resizeColumnToContents(0)
        self.close()


class EditApplication(WizardDialog):

    def __init__(self, tree, item):
        super(EditApplication, self).__init__(tree)
        self.tree = tree
        self.item = item

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Runner'), 0, 1, QtCore.Qt.AlignVCenter)
        self.runner = RunnersChoiceValue(self.tree, self.item)
        self.runner.setDisabled(True)
        self.runner.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_layout.addWidget(self.runner, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Windows'), 1, 1, QtCore.Qt.AlignVCenter)
        self.windows_path = LineEdit(value=item.windows_path, placeholder='C:\Program Files', options='path', custom_widget=self)
        self.content_layout.addWidget(self.windows_path, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Linux'), 2, 1, QtCore.Qt.AlignVCenter)
        self.linux_path = LineEdit(value=item.linux_path, placeholder='/opt', options='path', custom_widget=self)
        self.content_layout.addWidget(self.linux_path, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Darwin'), 3, 1, QtCore.Qt.AlignVCenter)
        self.darwin_path = LineEdit(value=item.darwin_path, placeholder='/Applications', options='path', custom_widget=self)
        self.content_layout.addWidget(self.darwin_path, 3, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText("Edit")
    
    def sizeHint(self):
        return QtCore.QSize(600, 212)
    
    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if widget.property('error') == True:
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_action_button_clicked(self):
        if self.item.status != 'NEW':
            self.item.status = 'EDIT'
            self.item.setForeground(0, QtGui.QBrush(QtGui.QColor(221, 166, 80)))
        self.item.windows_path = self.windows_path.text()
        self.item.linux_path = self.linux_path.text()
        self.item.darwin_path = self.darwin_path.text()
        self.item.refresh()
        self.close()


class ApplicationItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, status, variable, windows, linux, darwin):
        super(ApplicationItem, self).__init__(tree)
        self.tree = tree
        
        self.status = status
        self.variable = variable
        self.windows_path = windows
        self.linux_path = linux
        self.darwin_path = darwin

        self.refresh()
  
    def refresh(self):
        name = self.variable.split('_EXEC_PATH')[0]

        for runner in self.tree.runners:
            if name == runner.runner_name().upper():
                if runner.runner_icon():
                    self.setIcon(0, self.get_icon(runner.runner_icon()))
                else:
                    self.setIcon(0, QtGui.QIcon())
                self.setText(0, runner.runner_name())
    
    @staticmethod
    def get_icon(icon_ref):
        return QtGui.QIcon(resources.get_icon(icon_ref))


class ApplicationsList(QtWidgets.QTreeWidget):

    def __init__(self, page_widget, site_oid=None):
        super(ApplicationsList, self).__init__()
        self.page_widget = page_widget
        self.site_oid = site_oid

        self.setHeaderLabels(self.get_columns())
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

        self.setStyleSheet('''QTreeView::item:selected {
            background-color: #223e55;
            color: white;
            }'''
        )
        self.setRootIsDecorated(False)

        self.runners = page_widget.parent().get_factory(page_widget.parent().project_selected).list_runner_types()

        if site_oid:
            self.refresh()
        
        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)

    def get_columns(self):
        return ('Application', '')
    
    def refresh(self):
        self.blockSignals(True)
        self.clear()

        for item_oid in self.page_widget.parent().get_site_environnement(self.site_oid):
            variable = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/variable')
            windows_path = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/value_windows')
            linux_path = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/value_linux')
            darwin_path = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/value_darwin')

            item = ApplicationItem(self, 'OK', variable, windows_path, linux_path, darwin_path)

            self.setItemWidget(item, 1, EditItemButton(self, item, 'Application'))

        self.blockSignals(False)

    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.setCurrentItem(None)
        super(ApplicationsList, self).mousePressEvent(event)

    def _on_remove_action_clicked(self, item):
        if item.status == 'REMOVE':
            item.status = 'OK'
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(185, 194, 200)))
            return

        if item.status == 'NEW':
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
            del item
            return

        for item_oid in self.page_widget.parent().get_site_environnement(self.site_oid):
            variable = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/variable')
            name = variable.split('_EXEC_PATH')[0]
            if item.text(0).upper() == name:
                item.status = 'REMOVE'
                item.setForeground(0, QtGui.QBrush(QtGui.QColor(221, 80, 80)))
                return

    def _on_context_menu(self, event):
        item = self.itemAt(event)

        if item is None:
            return

        context_menu = QtWidgets.QMenu(self)

        if item.status == 'REMOVE':
            remove = context_menu.addAction(QtGui.QIcon(resources.get_icon(('icons.gui', 'remove-symbol'))), 'Cancel')
        else:
            remove = context_menu.addAction(QtGui.QIcon(resources.get_icon(('icons.gui', 'remove-symbol'))), 'Remove')
        
        remove.triggered.connect(lambda checked=False, x=item: self._on_remove_action_clicked(x))

        context_menu.exec_(self.mapToGlobal(event))


class AddWorkingSite(WizardDialog):

    def __init__(self, page_widget):
        super(AddWorkingSite, self).__init__(page_widget)
        self.setObjectName('AddWorkingSite')
        self.button_action.setEnabled(False)
        self.button_presets.show()
        self.preset_type = 'working_site'

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Name'), 0, 1, QtCore.Qt.AlignVCenter)
        self.site_name = LineEdit(options='working_site', mandatory=True, custom_widget=self)
        self.site_name.setObjectName('site_name')
        self.content_layout.addWidget(self.site_name, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Type'), 1, 1, QtCore.Qt.AlignVCenter)
        self.site_type = QtWidgets.QComboBox()
        self.site_type.addItem('Studio')
        self.site_type.addItem('User')
        self.site_type.setObjectName('site_type')
        self.content_layout.addWidget(self.site_type, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Root Windows folder'), 2, 1, QtCore.Qt.AlignVCenter)
        self.win_root_folder = LineEdit(placeholder='C:\projets\projectname')
        self.win_root_folder.setObjectName('win_root_folder')
        self.content_layout.addWidget(self.win_root_folder, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Root Linux folder'), 3, 1, QtCore.Qt.AlignVCenter)
        self.linux_root_folder = LineEdit(placeholder='/projets/projectname')
        self.linux_root_folder.setObjectName('linux_root_folder')
        self.content_layout.addWidget(self.linux_root_folder, 3, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 4, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Root Darwin folder'), 4, 1, QtCore.Qt.AlignVCenter)
        self.darwin_root_folder = LineEdit()
        self.darwin_root_folder.setObjectName('darwin_root_folder')
        self.content_layout.addWidget(self.darwin_root_folder, 4, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 5, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Render pools'), 5, 1, QtCore.Qt.AlignVCenter)
        self.render_pools = LineEdit('[]')
        self.render_pools.setObjectName('render_pools')
        self.content_layout.addWidget(self.render_pools, 5, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 6, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Applications'), 6, 1, QtCore.Qt.AlignVCenter)
        self.applications = ApplicationsList(self.page_widget)
        self.applications.setObjectName('applications')
        self.applications.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_layout.addWidget(self.applications, 7, 0, 2, 3, QtCore.Qt.AlignVCenter)

        button_add_app = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add_app.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add_app.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add_app.clicked.connect(self._on_add_app_button_clicked)
        button_add_app.setAutoDefault(False)
        self.content_layout.addWidget(button_add_app, 8, 2, QtCore.Qt.AlignRight)

        afterfx_settings = ObjectGroup(self, 'After Effects settings')
        afterfx_settings.setObjectName('afterfx_settings')

        afterfx_settings.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        afterfx_settings.content_layout.addWidget(QtWidgets.QLabel('Render settings templates'), 0, 1, QtCore.Qt.AlignVCenter)
        self.ae_render_settings_templates = LineEdit('[]', placeholder='''[('default', 'lfs_compo_render')]''')
        self.ae_render_settings_templates.setObjectName('ae_render_settings_templates')
        afterfx_settings.content_layout.addWidget(self.ae_render_settings_templates, 0, 2, QtCore.Qt.AlignVCenter)

        afterfx_settings.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        afterfx_settings.content_layout.addWidget(QtWidgets.QLabel('Output module templates'), 1, 1, QtCore.Qt.AlignVCenter)
        self.ae_output_module_templates = LineEdit('[]', placeholder='''[('default', 'lfs_compo_output_png')]''')
        self.ae_output_module_templates.setObjectName('ae_output_module_templates')
        afterfx_settings.content_layout.addWidget(self.ae_output_module_templates, 1, 2, QtCore.Qt.AlignVCenter)

        afterfx_settings.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        afterfx_settings.content_layout.addWidget(QtWidgets.QLabel('Audio output module template'), 2, 1, QtCore.Qt.AlignVCenter)
        self.ae_output_module_audio = LineEdit(placeholder='''lfs_output_audio_wav''')
        self.ae_output_module_audio.setObjectName('ae_output_module_audio')
        afterfx_settings.content_layout.addWidget(self.ae_output_module_audio, 2, 2, QtCore.Qt.AlignVCenter)

        afterfx_settings.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        afterfx_settings.content_layout.addWidget(QtWidgets.QLabel('Composition name patterns'), 3, 1, QtCore.Qt.AlignVCenter)
        self.ae_comp_name_patterns = LineEdit('[]', placeholder='''['{film}_{sequence}_{shot}']''')
        self.ae_comp_name_patterns.setObjectName('ae_comp_name_patterns')
        afterfx_settings.content_layout.addWidget(self.ae_comp_name_patterns, 3, 2, QtCore.Qt.AlignVCenter)
        
        self.content_layout.addWidget(afterfx_settings, 10, 0, 1, 3, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Add')
    
    def sizeHint(self):
        return QtCore.QSize(600, 600)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if widget.property('error') == True:
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_import_triggered(self):
        presetJSON = super(AddWorkingSite, self)._on_import_triggered()

        for key in presetJSON:
            if key != 'applications':
                continue
            for i in range(self.content_layout.count()):
                widget = self.content_layout.itemAt(i).widget()
                if widget.objectName() == key:
                    items = presetJSON[key]
                    for index in items:
                        app = False
                        for a in range(self.applications.topLevelItemCount()):
                            if self.applications.topLevelItem(a).variable == items[index]['variable']:
                                app = True
                                break
                        if not app:
                            item = ApplicationItem(
                                self.applications,
                                'NEW',
                                items[index]['variable'],
                                items[index]['windows_path'],
                                items[index]['linux_path'],
                                items[index]['darwin_path']
                            )
                            item.setForeground(0, QtGui.QBrush(QtGui.QColor(100, 221, 80)))
                            self.applications.addTopLevelItem(item)
                            self.applications.setItemWidget(item, 1, EditItemButton(self.applications, item, 'Application'))
                            self.applications.resizeColumnToContents(0)

    def _on_add_app_button_clicked(self):
        add_app_dialog = AddApplication(self.applications)
        add_app_dialog.exec()
    
    def _on_action_button_clicked(self):
        site = self.page_widget.parent().add_working_site(self.page_widget.parent().project_selected, self.site_name.text())
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/short_name', self.site_name.text().lower()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/site_type', self.site_type.currentText()
        )

        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/root_windows_folder', self.win_root_folder.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/root_linux_folder', self.linux_root_folder.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/root_darwin_folder', self.darwin_root_folder.text()
        )

        if self.render_pools.text() != '[]':
            for i, pool in enumerate(ast.literal_eval(self.render_pools.text())):
                self.page_widget.parent().session.cmds.Flow.call(
                    site.oid() + '/pool_names', 'add', [pool, i], {}
                )

        for i in range(self.applications.topLevelItemCount()):
            item = self.applications.topLevelItem(i)
            if item.status == 'NEW':
                self.page_widget.parent().session.cmds.Flow.call(
                    site.oid() + '/site_environment', 'add', [item.variable], {}
                )
                self.page_widget.parent().session.cmds.Flow.set_value(
                    site.oid() + '/site_environment/' + item.variable + '/variable', item.variable
                )
                self.page_widget.parent().session.cmds.Flow.set_value(
                    site.oid() + '/site_environment/' + item.variable + '/value_windows', item.windows_path
                )
                self.page_widget.parent().session.cmds.Flow.set_value(
                    site.oid() + '/site_environment/' + item.variable + '/value_linux', item.linux_path
                )
                self.page_widget.parent().session.cmds.Flow.set_value(
                    site.oid() + '/site_environment/' + item.variable + '/value_darwin', item.darwin_path
                )
                print('NEW ', item.variable)

        if self.ae_render_settings_templates.text() != '[]':
            for render, template_name in ast.literal_eval(self.ae_render_settings_templates.text()):
                self.page_widget.parent().session.cmds.Flow.call(
                    site.oid() + '/ae_render_settings_templates', 'set_key', [render, template_name], {}
                )

        if self.ae_output_module_templates.text() != '[]':
            for output, template_name in ast.literal_eval(self.ae_output_module_templates.text()):
                self.page_widget.parent().session.cmds.Flow.call(
                    site.oid() + '/ae_output_module_templates', 'set_key', [output, template_name], {}
                )

        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/ae_output_module_audio', self.ae_output_module_audio.text()
        )

        if self.ae_comp_name_patterns.text() != '[]':
            for i, comp in enumerate(ast.literal_eval(self.ae_comp_name_patterns.text())):
                self.page_widget.parent().session.cmds.Flow.call(
                    site.oid() + '/ae_comp_name_patterns', 'add', [comp, i], {}
                )

        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/configured', True
        )

        self.page_widget.tree.refresh()
        self.close()


class EditWorkingSite(WizardDialog):

    def __init__(self, page_widget, item_oid):
        super(EditWorkingSite, self).__init__(page_widget)
        self.setObjectName('EditWorkingSite')
        self.button_presets.show()
        self.preset_type = 'working_site'
        self.item_oid = item_oid

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Type'), 0, 1, QtCore.Qt.AlignVCenter)
        self.site_type = QtWidgets.QComboBox()
        self.site_type.addItem('Studio')
        self.site_type.addItem('User')
        self.site_type.setObjectName('site_type')
        self.site_type.setCurrentText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/site_type'))
        self.content_layout.addWidget(self.site_type, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Root Windows folder'), 1, 1, QtCore.Qt.AlignVCenter)
        self.win_root_folder = LineEdit(placeholder='C:\projets\projectname')
        self.win_root_folder.setObjectName('win_root_folder')
        self.win_root_folder.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/root_windows_folder'))
        self.content_layout.addWidget(self.win_root_folder, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Root Linux folder'), 2, 1, QtCore.Qt.AlignVCenter)
        self.linux_root_folder = LineEdit(placeholder='/projets/projectname')
        self.linux_root_folder.setObjectName('linux_root_folder')
        self.linux_root_folder.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/root_linux_folder'))
        self.content_layout.addWidget(self.linux_root_folder, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Root Darwin folder'), 3, 1, QtCore.Qt.AlignVCenter)
        self.darwin_root_folder = LineEdit()
        self.darwin_root_folder.setObjectName('darwin_root_folder')
        self.darwin_root_folder.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/root_darwin_folder'))
        self.content_layout.addWidget(self.darwin_root_folder, 3, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 4, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Render pools'), 4, 1, QtCore.Qt.AlignVCenter)
        self.render_pools = LineEdit('[]')
        self.render_pools.setObjectName('render_pools')
        self.render_pools.setText(str(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/pool_names')))
        self.content_layout.addWidget(self.render_pools, 4, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 5, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Applications'), 5, 1, QtCore.Qt.AlignVCenter)
        self.applications = ApplicationsList(self.page_widget, item_oid)
        self.applications.setObjectName('applications')
        self.applications.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_layout.addWidget(self.applications, 6, 0, 2, 3, QtCore.Qt.AlignVCenter)

        button_add_app = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add_app.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add_app.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add_app.clicked.connect(self._on_add_app_button_clicked)
        button_add_app.setAutoDefault(False)
        self.content_layout.addWidget(button_add_app, 7, 2, QtCore.Qt.AlignRight)

        afterfx_settings = ObjectGroup(self, 'After Effects settings')
        afterfx_settings.setObjectName('afterfx_settings')

        afterfx_settings.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        afterfx_settings.content_layout.addWidget(QtWidgets.QLabel('Render settings templates'), 0, 1, QtCore.Qt.AlignVCenter)
        self.ae_render_settings_templates = LineEdit(str(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/ae_render_settings_templates')))
        self.ae_render_settings_templates.setObjectName('ae_render_settings_templates')
        afterfx_settings.content_layout.addWidget(self.ae_render_settings_templates, 0, 2, QtCore.Qt.AlignVCenter)

        afterfx_settings.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        afterfx_settings.content_layout.addWidget(QtWidgets.QLabel('Output module templates'), 1, 1, QtCore.Qt.AlignVCenter)
        self.ae_output_module_templates = LineEdit(str(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/ae_output_module_templates')))
        self.ae_output_module_templates.setObjectName('ae_output_module_templates')
        afterfx_settings.content_layout.addWidget(self.ae_output_module_templates, 1, 2, QtCore.Qt.AlignVCenter)

        afterfx_settings.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        afterfx_settings.content_layout.addWidget(QtWidgets.QLabel('Audio output module template'), 2, 1, QtCore.Qt.AlignVCenter)
        self.ae_output_module_audio = LineEdit(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/ae_output_module_audio'))
        self.ae_output_module_audio.setObjectName('ae_output_module_audio')
        afterfx_settings.content_layout.addWidget(self.ae_output_module_audio, 2, 2, QtCore.Qt.AlignVCenter)

        afterfx_settings.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        afterfx_settings.content_layout.addWidget(QtWidgets.QLabel('Composition name patterns'), 3, 1, QtCore.Qt.AlignVCenter)
        self.ae_comp_name_patterns = LineEdit(str(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/ae_comp_name_patterns')))
        self.ae_comp_name_patterns.setObjectName('ae_comp_name_patterns')
        afterfx_settings.content_layout.addWidget(self.ae_comp_name_patterns, 3, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(afterfx_settings, 9, 0, 1, 3, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Edit')
    
    def sizeHint(self):
        return QtCore.QSize(600, 600)
    
    def _on_import_triggered(self):
        presetJSON = super(EditWorkingSite, self)._on_import_triggered()

        for key in presetJSON:
            if key != 'applications':
                continue
            for i in range(self.content_layout.count()):
                widget = self.content_layout.itemAt(i).widget()
                if widget.objectName() == key:
                    items = presetJSON[key]
                    for index in items:
                        app = None
                        for a in range(self.applications.topLevelItemCount()):
                            if self.applications.topLevelItem(a).variable == items[index]['variable']:
                                app = self.applications.topLevelItem(a)
                                break
                        if app is None:
                            item = ApplicationItem(
                                self.applications,
                                'NEW',
                                items[index]['variable'],
                                items[index]['windows_path'],
                                items[index]['linux_path'],
                                items[index]['darwin_path']
                            )
                            item.setForeground(0, QtGui.QBrush(QtGui.QColor(100, 221, 80)))
                            self.applications.addTopLevelItem(item)
                            self.applications.setItemWidget(item, 1, EditItemButton(self.applications, item, 'Application'))
                            self.applications.resizeColumnToContents(0)
                        else:
                            properties = vars(app)
                            properties = {k: v for k, v in properties.items() if type(v) == str}
                            items[index]['status'] = 'OK'
                            if properties == items[index]:
                                continue
                            else:
                                app.status = 'EDIT'
                                app.setForeground(0, QtGui.QBrush(QtGui.QColor(221, 166, 80)))
                                app.windows_path = items[index]['windows_path']
                                app.linux_path = items[index]['linux_path']
                                app.darwin_path = items[index]['darwin_path']
                                app.refresh()
                                self.applications.resizeColumnToContents(0)

    def _on_add_app_button_clicked(self):
        add_app_dialog = AddApplication(self.applications)
        add_app_dialog.exec()
    
    def _on_action_button_clicked(self):
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/site_type', self.site_type.currentText()
        )

        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/root_windows_folder', self.win_root_folder.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/root_linux_folder', self.linux_root_folder.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/root_darwin_folder', self.darwin_root_folder.text()
        )

        self.page_widget.parent().session.cmds.Flow.call(
            self.item_oid + '/pool_names', 'revert_to_default', [], {}
        )
        if self.render_pools.text() != '[]':
            for i, pool in enumerate(ast.literal_eval(self.render_pools.text())):
                self.page_widget.parent().session.cmds.Flow.call(
                    self.item_oid + '/pool_names', 'add', [pool, i], {}
                )

        status_order = ['REMOVE', 'EDIT', 'NEW']

        for status in status_order:
            for i in range(self.applications.topLevelItemCount()):
                item = self.applications.topLevelItem(i)
                if item.status == status:
                    if status == 'REMOVE':
                        self.page_widget.parent().session.cmds.Flow.call(
                            self.item_oid + '/site_environment', 'remove', [item.variable], {}
                        )
                        print('REMOVE ', item.variable)
                    if status == 'EDIT':
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/site_environment/' + item.variable + '/value_windows', item.windows_path
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/site_environment/' + item.variable + '/value_linux', item.linux_path
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/site_environment/' + item.variable + '/value_darwin', item.darwin_path
                        )
                        print('EDIT ', item.variable)
                    if status == 'NEW':
                        self.page_widget.parent().session.cmds.Flow.call(
                            self.item_oid + '/site_environment', 'add', [item.variable], {}
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/site_environment/' + item.variable + '/variable', item.variable
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/site_environment/' + item.variable + '/value_windows', item.windows_path
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/site_environment/' + item.variable + '/value_linux', item.linux_path
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/site_environment/' + item.variable + '/value_darwin', item.darwin_path
                        )
                        print('NEW ', item.variable)

        self.page_widget.parent().session.cmds.Flow.call(
            self.item_oid + '/ae_render_settings_templates', 'set', [''], {}
        )
        if self.ae_render_settings_templates.text() != '[]':
            for render, template_name in ast.literal_eval(self.ae_render_settings_templates.text()):
                self.page_widget.parent().session.cmds.Flow.call(
                    self.item_oid + '/ae_render_settings_templates', 'set_key', [render, template_name], {}
                )

        self.page_widget.parent().session.cmds.Flow.call(
            self.item_oid + '/ae_output_module_templates', 'set', [''], {}
        )
        if self.ae_output_module_templates.text() != '[]':
            for output, template_name in ast.literal_eval(self.ae_output_module_templates.text()):
                self.page_widget.parent().session.cmds.Flow.call(
                    self.item_oid + '/ae_output_module_templates', 'set_key', [output, template_name], {}
                )

        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/ae_output_module_audio', self.ae_output_module_audio.text()
        )

        self.page_widget.parent().session.cmds.Flow.call(
            self.item_oid + '/ae_comp_name_patterns', 'revert_to_default', [], {}
        )
        if self.ae_comp_name_patterns.text() != '[]':
            for i, comp in enumerate(ast.literal_eval(self.ae_comp_name_patterns.text())):
                self.page_widget.parent().session.cmds.Flow.call(
                    self.item_oid + '/ae_comp_name_patterns', 'add', [comp, i], {}
                )

        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/configured', True
        )

        self.page_widget.tree.refresh()
        self.close()


class WorkingSiteItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, name, icon):
        super(WorkingSiteItem, self).__init__(tree)
        self.name = name
        self.icon = icon

        self.refresh()
  
    def refresh(self):
        self.setIcon(0, self.get_icon(self.icon))
        self.setText(0, self.name)
    
    @staticmethod
    def get_icon(icon_ref):
        return QtGui.QIcon(resources.get_icon(icon_ref))


class WorkingSitesList(QtWidgets.QTreeWidget):

    def __init__(self, page_widget):
        super(WorkingSitesList, self).__init__()
        self.page_widget = page_widget
        self.current_site = False

        self.setHeaderLabels(self.get_columns())
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setStyleSheet('''QTreeView::item:selected {
            background-color: #223e55;
            color: white;
            }'''
        )
        self.setRootIsDecorated(False)
        
        self.refresh()

        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
    
    def get_columns(self):
        return ('Site', '')

    def refresh(self):
        self.blockSignals(True)
        self.clear()

        working_sites = self.page_widget.parent().get_working_sites(self.page_widget.parent().project_selected)
        ws_infos = self.page_widget.parent().session.cmds.Flow.get_mapped_rows(working_sites.oid())

        for site in ws_infos:
            item = WorkingSiteItem(self, site[1]['Site'], site[1]['_style']['icon'])

            self.setItemWidget(item, 1, EditItemButton(self.page_widget, site[0], 'WorkingSite'))

        for i in range(self.topLevelItemCount()):
            if self.topLevelItem(i).name == os.environ['KABARET_SITE_NAME']:
                self.current_site = True

        self.blockSignals(False)
    
    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.setCurrentItem(None)
        super(WorkingSitesList, self).mousePressEvent(event)


class WorkingSites(WizardPage):

    def __init__(self, homepage_widget):
        super(WorkingSites, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget
        self.setObjectName('Working sites')

        list_widget = QtWidgets.QWidget()
        list_layout = QtWidgets.QGridLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_widget.setLayout(list_layout)

        self.tree = WorkingSitesList(self)
        list_layout.addWidget(self.tree, 0, 0, 2, 0)
        
        button_add = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add.clicked.connect(self._on_add_button_clicked)
        list_layout.addWidget(button_add, 1, 0, QtCore.Qt.AlignRight)

        self.content_layout.addWidget(list_widget)

        if self.tree.current_site == False:
            self.button_layout.insertWidget(self.button_layout.count() - 5, QtWidgets.QLabel('⚠️ Current site not created'))

    def _on_add_button_clicked(self):
        dialog = AddWorkingSite(self)
        dialog.exec()

    def _on_back_button_clicked(self):
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        back_page = UsersConfig(self.homepage_widget)
        self.homepage_widget.layout().addWidget(back_page, 3)
        self.homepage_widget.setup_steps.refresh(back_page.objectName())

    def _on_next_button_clicked(self):
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        next_page = ExchangeSites(self.homepage_widget)
        self.homepage_widget.layout().addWidget(next_page, 3)
        self.homepage_widget.setup_steps.refresh(next_page.objectName())


class AddExchangeSite(WizardDialog):

    def __init__(self, page_widget):
        super(AddExchangeSite, self).__init__(page_widget)
        self.button_action.setEnabled(False)
        self.button_presets.show()
        self.preset_type = 'exchange_site'

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Name'), 0, 1, QtCore.Qt.AlignVCenter)
        self.site_name = LineEdit(options='exchange_site', mandatory=True, custom_widget=self)
        self.site_name.setObjectName('site_name')
        self.content_layout.addWidget(self.site_name, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Server URL'), 1, 1, QtCore.Qt.AlignVCenter)
        self.server_url = LineEdit(placeholder='0:0:0:0:8888', mandatory=True, custom_widget=self)
        self.server_url.setObjectName('server_url')
        self.content_layout.addWidget(self.server_url, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Login'), 2, 1, QtCore.Qt.AlignVCenter)
        self.server_login = LineEdit(placeholder='admin', mandatory=True, custom_widget=self)
        self.server_login.setObjectName('server_login')
        self.content_layout.addWidget(self.server_login, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Password'), 3, 1, QtCore.Qt.AlignVCenter)
        self.server_password = LineEdit(options='password', mandatory=True, custom_widget=self)
        self.server_password.setObjectName('server_password')
        self.content_layout.addWidget(self.server_password, 3, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 4, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Bucket name'), 4, 1, QtCore.Qt.AlignVCenter)
        self.bucket_name = LineEdit(mandatory=True, custom_widget=self)
        self.bucket_name.setObjectName('bucket_name')
        self.content_layout.addWidget(self.bucket_name, 4, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 5, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Enable TLS'), 5, 1, QtCore.Qt.AlignVCenter)
        self.enable_tls = QtWidgets.QCheckBox()
        self.enable_tls.setObjectName('enable_tls')
        self.content_layout.addWidget(self.enable_tls, 5, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText("Add")
    
    def sizeHint(self):
        return QtCore.QSize(400, 212)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit) == False:
                    continue
                if widget.property('error') == True or (widget.mandatory and widget.text() == ''):
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_action_button_clicked(self):
        site = self.page_widget.parent().add_exchange_site(self.page_widget.parent().project_selected, self.site_name.text())
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/short_name', self.site_name.text().lower()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/configured', True
        )

        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/server_url', self.server_url.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/server_login', self.server_login.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/server_password', self.server_password.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/bucket_name', self.bucket_name.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            site.oid() + '/enable_tls', self.enable_tls.isChecked()
        )

        self.page_widget.tree.refresh()
        self.page_widget.combobox.refresh()
        self.close()


class EditExchangeSite(WizardDialog):

    def __init__(self, page_widget, item_oid):
        super(EditExchangeSite, self).__init__(page_widget)
        self.button_presets.show()
        self.preset_type = 'exchange_site'
        self.item_oid = item_oid

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Server URL'), 0, 1, QtCore.Qt.AlignVCenter)
        self.server_url = LineEdit(mandatory=True, custom_widget=self)
        self.server_url.setObjectName('server_url')
        self.server_url.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/server_url'))
        self.content_layout.addWidget(self.server_url, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Login'), 1, 1, QtCore.Qt.AlignVCenter)
        self.server_login = LineEdit(mandatory=True, custom_widget=self)
        self.server_login.setObjectName('server_login')
        self.server_login.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/server_login'))
        self.content_layout.addWidget(self.server_login, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Password'), 2, 1, QtCore.Qt.AlignVCenter)
        self.server_password = LineEdit(options='password', mandatory=True, custom_widget=self)
        self.server_password.setObjectName('server_password')
        self.server_password.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/server_password'))
        self.content_layout.addWidget(self.server_password, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Bucket name'), 3, 1, QtCore.Qt.AlignVCenter)
        self.bucket_name = LineEdit(mandatory=True, custom_widget=self)
        self.bucket_name.setObjectName('bucket_name')
        self.bucket_name.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/bucket_name'))
        self.content_layout.addWidget(self.bucket_name, 3, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 4, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Enable TLS'), 4, 1, QtCore.Qt.AlignVCenter)
        self.enable_tls = QtWidgets.QCheckBox()
        self.enable_tls.setObjectName('enable_tls')
        self.enable_tls.setChecked(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/enable_tls'))
        self.content_layout.addWidget(self.enable_tls, 4, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Edit')
    
    def sizeHint(self):
        return QtCore.QSize(400, 212)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit) == False:
                    continue
                if widget.property('error') == True or (widget.mandatory and widget.text() == ''):
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)
    
    def _on_action_button_clicked(self):
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/server_url', self.server_url.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/server_login', self.server_login.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/server_password', self.server_password.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/bucket_name', self.bucket_name.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/enable_tls', self.enable_tls.isChecked()
        )

        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/configured', True
        )

        self.page_widget.tree.refresh()
        self.page_widget.combobox.refresh()
        self.close()


class ExchangeSiteItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, name, icon):
        super(ExchangeSiteItem, self).__init__(tree)
        self.name = name
        self.icon = icon

        self.refresh()
  
    def refresh(self):
        self.setIcon(0, self.get_icon(self.icon))
        self.setText(0, self.name)
    
    @staticmethod
    def get_icon(icon_ref):
        return QtGui.QIcon(resources.get_icon(icon_ref))


class ExchangeSitesList(QtWidgets.QTreeWidget):

    def __init__(self, page_widget):
        super(ExchangeSitesList, self).__init__()
        self.page_widget = page_widget

        self.setHeaderLabels(self.get_columns())
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setStyleSheet('''QTreeView::item:selected {
            background-color: #223e55;
            color: white;
            }'''
        )
        self.setRootIsDecorated(False)
        
        self.refresh()

        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
    
    def get_columns(self):
        return ('Server', '')

    def refresh(self):
        self.blockSignals(True)
        self.clear()

        exchange_sites = self.page_widget.parent().get_exchange_sites(self.page_widget.parent().project_selected)
        es_infos = self.page_widget.parent().session.cmds.Flow.get_mapped_rows(exchange_sites.oid())

        for site in es_infos:
            item = ExchangeSiteItem(self, site[1]['Site'], site[1]['_style']['icon'])

            self.setItemWidget(item, 1, EditItemButton(self.page_widget, site[0], 'ExchangeSite'))

        self.blockSignals(False)
    
    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.setCurrentItem(None)
        super(ExchangeSitesList, self).mousePressEvent(event)


class ExchangeSites(WizardPage):

    def __init__(self, homepage_widget):
        super(ExchangeSites, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget
        self.setObjectName('Files')

        list_widget = QtWidgets.QWidget()
        list_layout = QtWidgets.QGridLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)

        self.tree = ExchangeSitesList(self)
        list_layout.addWidget(self.tree, 0, 0, 2, 0)

        button_add = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add.clicked.connect(self._on_add_button_clicked)
        list_layout.addWidget(button_add, 1, 2, QtCore.Qt.AlignRight)

        list_widget.setLayout(list_layout)

        choice_value_widget = QtWidgets.QWidget()
        choice_value_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        choice_value_layout = QtWidgets.QGridLayout()
        choice_value_layout.setContentsMargins(0, 0, 0, 0)

        choice_value_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        choice_value_layout.addWidget(QtWidgets.QLabel('Current exchange site'), 0, 1, QtCore.Qt.AlignVCenter)
        self.combobox = CurrentExchangeSite(self)
        self.combobox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        choice_value_layout.addWidget(self.combobox, 0, 2, QtCore.Qt.AlignVCenter)

        choice_value_widget.setLayout(choice_value_layout)

        self.content_layout.addWidget(list_widget)
        self.content_layout.addWidget(choice_value_widget)

    def _on_add_button_clicked(self):
        dialog = AddExchangeSite(self)
        dialog.exec()

    def _on_back_button_clicked(self):
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        back_page = WorkingSites(self.homepage_widget)
        self.homepage_widget.layout().addWidget(back_page, 3)
        self.homepage_widget.setup_steps.refresh(back_page.objectName())

    def _on_next_button_clicked(self):
        if self.combobox.currentText() != '':
            self.homepage_widget.set_exchange_site(self.homepage_widget.project_selected, self.combobox.currentText())
        
        exchange_site = self.homepage_widget.get_exchange_site(self.homepage_widget.project_selected)
        ret = None
        self.label_feedback.setText('Checking...')
        QtWidgets.QApplication.processEvents()
        QtWidgets.QApplication.processEvents()

        ret = self.homepage_widget.session.cmds.Flow.call(
            exchange_site.oid() + '/sync_manager', 'check_connection', {}, {}
        )

        if ret is not None:
            self.combobox.setProperty('error', True)
            self.combobox.setStyleSheet('border-color: red;')
            self.combobox.style().polish(self)
            self.combobox.setToolTip('!!!\nCONNECTION ERROR: %s' % (ret,))
            self.label_feedback.setText('')
        else:
            print('Connection looks OK')
            self.homepage_widget.layout().itemAt(2).widget().deleteLater()
            next_page = FilesManagement(self.homepage_widget)
            self.homepage_widget.layout().addWidget(next_page, 3)
            self.homepage_widget.setup_steps.refresh(next_page.objectName())


class FilesManagement(WizardPage):

    def __init__(self, homepage_widget):
        super(FilesManagement, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget
        self.project_settings = self.homepage_widget.get_project_settings(self.homepage_widget.project_selected)
        self.setObjectName('Files')

        inputs_widget = QtWidgets.QWidget()
        self.inputs_layout = QtWidgets.QGridLayout()
        self.inputs_layout.setContentsMargins(0, 0, 0, 0)
       
        self.inputs_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.inputs_layout.addWidget(QtWidgets.QLabel('Path Format'), 0, 1, QtCore.Qt.AlignVCenter)
        self.path_format = LineEdit(mandatory=True, custom_widget=self)
        self.path_format_item = self.homepage_widget.get_path_format(self.homepage_widget.project_selected)
        self.path_format.setText(self.homepage_widget.session.cmds.Flow.get_value(self.path_format_item.oid() + '/value'))
        self.inputs_layout.addWidget(self.path_format, 0, 2, QtCore.Qt.AlignVCenter)

        self.inputs_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.inputs_layout.addWidget(QtWidgets.QLabel('Non Editable Files'), 1, 1, QtCore.Qt.AlignVCenter)
        self.non_editable_files = LineEdit(placeholder='*.extension')
        self.non_editable_files.setText(self.homepage_widget.session.cmds.Flow.get_value(
            self.project_settings.oid() + '/non_editable_files'))
        self.inputs_layout.addWidget(self.non_editable_files, 1, 2, QtCore.Qt.AlignVCenter)

        self.inputs_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.inputs_layout.addWidget(QtWidgets.QLabel('Auto Upload'), 2, 1, QtCore.Qt.AlignVCenter)
        self.auto_upload = LineEdit(placeholder='*.extension')
        self.auto_upload.setText(self.homepage_widget.session.cmds.Flow.get_value(
            self.project_settings.oid() + '/auto_upload'))
        self.inputs_layout.addWidget(self.auto_upload, 2, 2, QtCore.Qt.AlignVCenter)

        self.inputs_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.inputs_layout.addWidget(QtWidgets.QLabel('Enable File Lock'), 3, 1, QtCore.Qt.AlignVCenter)
        self.enable_file_lock = QtWidgets.QCheckBox()
        self.enable_file_lock.setChecked(self.homepage_widget.session.cmds.Flow.get_value(
            self.project_settings.oid() + '/enable_file_lock'))
        self.inputs_layout.addWidget(self.enable_file_lock, 3, 2, QtCore.Qt.AlignVCenter)

        inputs_widget.setLayout(self.inputs_layout)

        self.content_layout.addStretch()
        self.content_layout.addWidget(inputs_widget)
        self.content_layout.addStretch()

    def refresh_buttons(self):
        for i in reversed(range(self.inputs_layout.count())):
            widget = self.inputs_layout.itemAt(i).widget()
            if widget:
                if widget.property('error') == True:
                    return self.button_next.setEnabled(False)
        
        return self.button_next.setEnabled(True)

    def _on_back_button_clicked(self):
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        back_page = ExchangeSites(self.homepage_widget)
        self.homepage_widget.layout().addWidget(back_page, 3)
        self.homepage_widget.setup_steps.refresh(back_page.objectName())

    def _on_next_button_clicked(self):
        self.label_feedback.setText('Loading...')
        QtWidgets.QApplication.processEvents()
        QtWidgets.QApplication.processEvents()

        self.path_format_item.edit.value.set(self.path_format.text())
        self.path_format_item.edit.run("Save")

        self.homepage_widget.session.cmds.Flow.set_value(
            self.project_settings.oid() + '/non_editable_files', self.non_editable_files.text()
        )
        self.homepage_widget.session.cmds.Flow.set_value(
            self.project_settings.oid() + '/auto_upload', self.auto_upload.text()
        )
        self.homepage_widget.session.cmds.Flow.set_value(
            self.project_settings.oid() + '/enable_file_lock', self.enable_file_lock.isChecked()
        )

        # self.label_feedback.setText('')

        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        next_page = TasksManager(self.homepage_widget)
        self.homepage_widget.layout().addWidget(next_page, 3)
        self.homepage_widget.setup_steps.refresh(next_page.objectName())


class AddDefaultTask(WizardDialog):

    def __init__(self, page_widget):
        super(AddDefaultTask, self).__init__(page_widget)
        self.setObjectName('AddDefaultTask')
        self.button_presets.show()
        self.preset_type = 'default_task'
        self.button_action.setEnabled(False)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Display Name'), 0, 1, QtCore.Qt.AlignVCenter)
        self.display_name = LineEdit(options='default_task', mandatory=True, custom_widget=self, copy=True)
        self.display_name.setObjectName('display_name')
        self.content_layout.addWidget(self.display_name, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Task Name'), 1, 1, QtCore.Qt.AlignVCenter)
        self.input_id = LineEdit(options='underscore', mandatory=True, custom_widget=self)
        self.content_layout.addWidget(self.input_id, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Template'), 2, 1, QtCore.Qt.AlignVCenter)
        self.template = QtWidgets.QComboBox()
        self.template.setObjectName('template')
        task_templates = self.page_widget.parent().get_task_templates(self.page_widget.parent().project_selected)
        for template in task_templates:
            self.template.addItem(template[1]['Name'])
        self.content_layout.addWidget(self.template, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Position'), 3, 1, QtCore.Qt.AlignVCenter)
        self.position = LineEdit(value='0', placeholder='0', options='digit', mandatory=True, custom_widget=self)
        self.position.setObjectName('position')
        self.content_layout.addWidget(self.position, 3, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 4, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Path format'), 4, 1, QtCore.Qt.AlignVCenter)
        self.path_format = LineEdit(
            value=None, placeholder='{film}/{sequence}/{shot}/{task}/{file_mapped_name}/{revision}/{file_base_name}',
            custom_widget=self)
        self.path_format.setObjectName('path_format')
        self.content_layout.addWidget(self.path_format, 4, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 5, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Enabled'), 5, 1, QtCore.Qt.AlignVCenter)
        self.enabled = QtWidgets.QCheckBox()
        self.enabled.setObjectName('enabled')
        self.enabled.setChecked(True)
        self.content_layout.addWidget(self.enabled, 5, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 6, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Optional'), 6, 1, QtCore.Qt.AlignVCenter)
        self.optional = QtWidgets.QCheckBox()
        self.optional.setObjectName('optional')
        self.content_layout.addWidget(self.optional, 6, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Add')
    
    def sizeHint(self):
        return QtCore.QSize(380, 270)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit) == False:
                    continue
                if widget.property('error') == True or (widget.mandatory and widget.text() == ''):
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)
    
    def _on_action_button_clicked(self):
        self.page_widget.parent().session.cmds.Flow.call(
            self.page_widget.task_manager.oid() + '/default_tasks', 'add_default_task', 
            [
                self.input_id.text(),
                self.display_name.text(),
                self.template.currentText(),
                int(self.position.text()),
                self.path_format.text() or None,
                self.enabled.isChecked(),
                self.optional.isChecked()
            ], {}
        )

        self.page_widget.dft_tree.refresh()
        self.close()


class EditDefaultTask(WizardDialog):

    def __init__(self, page_widget, item_oid):
        super(EditDefaultTask, self).__init__(page_widget)
        self.setObjectName('EditDefaultTask')
        self.button_presets.show()
        self.preset_type = 'default_task'
        self.item_oid = item_oid

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Display Name'), 0, 1, QtCore.Qt.AlignVCenter)
        self.display_name = LineEdit(mandatory=True, custom_widget=self)
        self.display_name.setObjectName('display_name')
        self.display_name.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/display_name'))
        self.content_layout.addWidget(self.display_name, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Template'), 1, 1, QtCore.Qt.AlignVCenter)
        self.template = QtWidgets.QComboBox()
        self.template.setObjectName('template')
        task_templates = self.page_widget.parent().get_task_templates(self.page_widget.parent().project_selected)
        for template in task_templates:
            self.template.addItem(template[1]['Name'])
        self.template.setCurrentText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/template'))
        self.content_layout.addWidget(self.template, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Position'), 2, 1, QtCore.Qt.AlignVCenter)
        self.position = LineEdit(placeholder='0', options='digit', mandatory=True, custom_widget=self)
        self.position.setObjectName('position')
        self.position.setText(str(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/position')))
        self.content_layout.addWidget(self.position, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Enabled'), 3, 1, QtCore.Qt.AlignVCenter)
        self.enabled = QtWidgets.QCheckBox()
        self.enabled.setObjectName('enabled')
        self.enabled.setChecked(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/enabled'))
        self.content_layout.addWidget(self.enabled, 3, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 4, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Optional'), 4, 1, QtCore.Qt.AlignVCenter)
        self.optional = QtWidgets.QCheckBox()
        self.optional.setObjectName('optional')
        self.optional.setChecked(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/optional'))
        self.content_layout.addWidget(self.optional, 4, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 5, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Color'), 5, 1, QtCore.Qt.AlignVCenter)
        self.color = QtWidgets.QComboBox()
        self.color.setObjectName('color')
        self.color_edit = LineEdit()
        self.color_edit.setStyleSheet('QLineEdit { border: none; padding: 0px; }')
        self.color.setLineEdit(self.color_edit)
        self.color_edit.setText(str(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/color')))
        colors = self.page_widget.parent().get_template_colors(self.page_widget.parent().project_selected)
        for color in colors:
            self.color.addItem(color)
        self.content_layout.addWidget(self.color, 5, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 6, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Icon'), 6, 1, QtCore.Qt.AlignVCenter)
        self.icon = LineEdit()
        self.icon.setObjectName('icon')
        self.icon.setText(str(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/icon')))
        self.content_layout.addWidget(self.icon, 6, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 7, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Files'), 7, 1, QtCore.Qt.AlignVCenter)
        self.files = FilesList(self.page_widget, self, item_oid)
        self.files.setObjectName('files')
        self.files.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_layout.addWidget(self.files, 8, 0, 2, 3, QtCore.Qt.AlignVCenter)

        button_add_file = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add_file.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add_file.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add_file.clicked.connect(self._on_add_file_button_clicked)
        button_add_file.setAutoDefault(False)
        self.content_layout.addWidget(button_add_file, 9, 2, QtCore.Qt.AlignRight)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 10, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Path format'), 10, 1, QtCore.Qt.AlignVCenter)
        self.path_format = LineEdit(custom_widget=self)
        self.path_format.setObjectName('path_format')
        self.path_format.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/path_format'))
        self.content_layout.addWidget(self.path_format, 10, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Edit')
    
    def sizeHint(self):
        return QtCore.QSize(600, 535)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit) == False:
                    continue
                if widget.property('error') == True or (widget.mandatory and widget.text() == ''):
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_import_triggered(self):
        presetJSON = super(EditDefaultTask, self)._on_import_triggered()

        for key in presetJSON:
            if key != 'files':
                continue
            for i in range(self.content_layout.count()):
                widget = self.content_layout.itemAt(i).widget()
                if widget.objectName() == key:
                    items = presetJSON[key]
                    for index in items:
                        file_item = None
                        for f in range(self.files.topLevelItemCount()):
                            if self.files.topLevelItem(f).name == items[index]['name']:
                                file_item = self.files.topLevelItem(f)
                                break
                        if file_item is None:
                            item = FileItem(
                                self.files,
                                'NEW',
                                items[index]['name'],
                                items[index]['file_name'],
                                items[index]['path_format'],
                                items[index]['enabled'],
                                items[index]['optional']
                            )
                            item.setForeground(1, QtGui.QBrush(QtGui.QColor(100, 221, 80)))
                            self.files.addTopLevelItem(item)
                            self.files.setItemWidget(item, 2, EditItemButton(self.files, item, 'TaskFile'))
                            self.files.resizeColumnToContents(1)
                        else:
                            properties = vars(file_item)
                            properties = {k: v for k, v in properties.items() if type(v) == str or type(v) == bool}
                            items[index]['status'] = 'OK'
                            if properties == items[index]:
                                continue
                            else:
                                file_item.status = 'EDIT'
                                file_item.setForeground(1, QtGui.QBrush(QtGui.QColor(221, 166, 80)))
                                file_item.windows_path = items[index]['windows_path']
                                file_item.linux_path = items[index]['linux_path']
                                file_item.darwin_path = items[index]['darwin_path']
                                file_item.refresh()
                                self.files.resizeColumnToContents(1)

    def _on_add_file_button_clicked(self):
        add_app_dialog = AddFile(self.files)
        add_app_dialog.exec()

    def _on_action_button_clicked(self):
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/display_name', self.display_name.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/template', self.template.currentText()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/path_format', self.path_format.text()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/position', int(self.position.text())
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/enabled', self.enabled.isChecked()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/optional', self.optional.isChecked()
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/color', self.color_edit.text() or None
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/icon', eval(self.icon.text())
        )

        status_order = ['REMOVE', 'EDIT', 'NEW']

        for status in status_order:
            for i in range(self.files.topLevelItemCount()):
                item = self.files.topLevelItem(i)
                if item.status == status:
                    if status == 'REMOVE':
                        self.page_widget.parent().session.cmds.Flow.call(
                            self.item_oid + '/files/edits', 'remove', [item.name], {}
                        )
                        print('RESET ', item.name)
                    if status == 'EDIT':
                        if self.page_widget.parent().session.cmds.Flow.call(
                            self.item_oid + '/files/edits', 'has_mapped_name', [item.name], {}
                        ):
                            dft_file = self.item_oid + '/files/edits/' + item.name
                        else:
                            dft_file = self.page_widget.parent().session.cmds.Flow.call(
                                self.item_oid + '/files/edits', 'add', [item.name], {}
                            )
                            dft_file = dft_file.oid()
                            self.page_widget.parent().session.cmds.Flow.set_value(
                                dft_file + '/file_name', item.file_name
                            )
                        
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            dft_file + '/path_format', item.path_format or None
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            dft_file + '/enabled', item.enabled
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            dft_file + '/optional', item.optional
                        )
                        print('EDIT ', item.name)
                    if status == 'NEW':
                        self.page_widget.parent().session.cmds.Flow.call(
                            self.item_oid + '/files/edits', 'add', [item.name], {}
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/edits/' + item.name + '/file_name', item.file_name
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/edits/' + item.name + '/path_format', item.path_format
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/edits/' + item.name + '/enabled', item.enabled
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/edits/' + item.name + '/optional', item.optional
                        )
                        print('NEW ', item.name)

        self.page_widget.dft_tree.refresh()
        self.close()


class DefaultTasksWarning(QtWidgets.QWidget):

    def __init__(self, page_widget):
        super(DefaultTasksWarning, self).__init__(page_widget)
        self.page_widget = page_widget

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.frame = QtWidgets.QFrame()
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setStyleSheet('''
            background-color: #2b2b2b;
            border: 1px solid #22222b;
        ''')

        self.asset = QtWidgets.QWidget()
        asset_lo = QtWidgets.QVBoxLayout()
        icon = QtGui.QIcon(resources.get_icon(('icons.gui', 'exclamation-sign')))
        pixmap = icon.pixmap(QtCore.QSize(128, 128))
        self.icon_lbl = QtWidgets.QLabel('')
        self.icon_lbl.setPixmap(pixmap)
        self.label = QtWidgets.QLabel('You need to create a task template first')

        asset_lo.addWidget(self.icon_lbl, 0, QtCore.Qt.AlignCenter)
        asset_lo.addWidget(self.label, 1, QtCore.Qt.AlignCenter)
        self.asset.setLayout(asset_lo)
        
        glo = QtWidgets.QGridLayout()
        glo.setContentsMargins(0,0,0,0)
        glo.addWidget(self.frame, 0, 0, 3, 0)
        glo.addWidget(self.asset, 1, 0, QtCore.Qt.AlignCenter)
        self.setLayout(glo)


class DefaultTaskItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, name, icon):
        super(DefaultTaskItem, self).__init__(tree)
        self.name = name
        self.icon = icon

        self.refresh()
  
    def refresh(self):
        self.setIcon(0, self.get_icon(self.icon))
        self.setText(0, self.name)
    
    @staticmethod
    def get_icon(icon_ref):
        return QtGui.QIcon(resources.get_icon(icon_ref))


class DefaultTasksList(QtWidgets.QTreeWidget):

    def __init__(self, page_widget):
        super(DefaultTasksList, self).__init__()
        self.page_widget = page_widget

        self.setHeaderLabels(self.get_columns())
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setStyleSheet('''QTreeView::item:selected {
            background-color: #223e55;
            color: white;
            }'''
        )
        self.setRootIsDecorated(False)
        
        self.refresh()

        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
    
    def get_columns(self):
        return ('Name', '')

    def refresh(self):
        self.blockSignals(True)
        self.clear()

        default_tasks = self.page_widget.parent().get_default_tasks(self.page_widget.parent().project_selected)

        for task in default_tasks:
            item = DefaultTaskItem(self, task[1]['Name'], task[1]['_style']['icon'])

            self.setItemWidget(item, 1, EditItemButton(self.page_widget, task[0], 'DefaultTask'))

        self.resizeColumnToContents(0)
        self.blockSignals(False)
    
    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.setCurrentItem(None)
        super(DefaultTasksList, self).mousePressEvent(event)


class AddFile(WizardDialog):

    def __init__(self, tree):
        super(AddFile, self).__init__(tree)
        self.tree = tree
        self.button_action.setEnabled(False)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('File Name'), 0, 1, QtCore.Qt.AlignVCenter)
        self.file_name = LineEdit(placeholder='layout.blend', mandatory=True, custom_widget=self)
        self.content_layout.addWidget(self.file_name, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Path Format'), 1, 1, QtCore.Qt.AlignVCenter)
        self.path_format = LineEdit(
            value='',
            placeholder='{film}/{shot}/{file}/{revision}',
            custom_widget=self
        )
        self.content_layout.addWidget(self.path_format, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Enabled'), 2, 1, QtCore.Qt.AlignVCenter)
        self.enabled = QtWidgets.QCheckBox()
        self.enabled.setChecked(True)
        self.content_layout.addWidget(self.enabled, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Optional'), 3, 1, QtCore.Qt.AlignVCenter)
        self.optional = QtWidgets.QCheckBox()
        self.optional.setChecked(False)
        self.content_layout.addWidget(self.optional, 3, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText("Add")
    
    def sizeHint(self):
        return QtCore.QSize(700, 205)
    
    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit) == False:
                    continue
                if widget.property('error') == True or (widget.mandatory and widget.text() == ''):
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_action_button_clicked(self):
        item = FileItem(
            self.tree,
            'NEW',
            self.file_name.text().replace('.', '_'),
            self.file_name.text(),
            self.path_format.text() or None,
            self.enabled.isChecked(),
            self.optional.isChecked()
        )
        item.setForeground(1, QtGui.QBrush(QtGui.QColor(100, 221, 80)))
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 2, EditItemButton(self.tree, item, 'TaskFile'))
        self.tree.resizeColumnToContents(1)
        self.close()


class EditFile(WizardDialog):

    def __init__(self, tree, item):
        super(EditFile, self).__init__(tree)
        self.tree = tree
        self.item = item

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('File Name'), 0, 1, QtCore.Qt.AlignVCenter)
        self.file_name = LineEdit(value=item.file_name, placeholder='layout.blend', mandatory=True, custom_widget=self)
        if self.tree.action_widget is not None:
            self.file_name.setReadOnly(True)
        self.content_layout.addWidget(self.file_name, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Path Format'), 1, 1, QtCore.Qt.AlignVCenter)
        self.path_format = LineEdit(value=item.path_format, placeholder='{film}/{shot}/{file}/{revision}', custom_widget=self)
        self.content_layout.addWidget(self.path_format, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Enabled'), 2, 1, QtCore.Qt.AlignVCenter)
        self.enabled = QtWidgets.QCheckBox()
        self.enabled.setChecked(item.enabled)
        self.content_layout.addWidget(self.enabled, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Optional'), 3, 1, QtCore.Qt.AlignVCenter)
        self.optional = QtWidgets.QCheckBox()
        self.optional.setChecked(item.optional)
        self.content_layout.addWidget(self.optional, 3, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText("Edit")
    
    def sizeHint(self):
        return QtCore.QSize(700, 205)
    
    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if widget.property('error') == True:
                    return self.button_action.setEnabled(False)
        
        return self.button_action.setEnabled(True)

    def _on_action_button_clicked(self):
        if self.item.status != 'NEW':
            self.item.status = 'EDIT'
            self.item.setForeground(1, QtGui.QBrush(QtGui.QColor(221, 166, 80)))
        self.item.file_name = self.file_name.text()
        self.item.path_format = self.path_format.text()
        self.item.enabled = self.enabled.isChecked()
        self.item.optional = self.optional.isChecked()
        self.item.refresh()
        self.tree.resizeColumnToContents(1)
        self.close()


class FileItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, status, name, file_name, path_format, enabled, optional):
        super(FileItem, self).__init__(tree)
        self.tree = tree
        
        self.status = status
        self.name = name
        self.file_name = file_name
        self.path_format = path_format
        self.enabled = enabled
        self.optional = optional

        self.refresh()
  
    def refresh(self):
        self.setIcon(0, self.get_icon((
            'icons.gui',
            'check' if self.enabled else 'check-box-empty'
        )))
        self.setText(1, self.file_name)
        _, ext = os.path.splitext(self.file_name)

        if ext:
            icon = CHOICES_ICONS.get(
                ext[1:], ('icons.gui', 'text-file-1')
            )
            self.setIcon(1, self.get_icon(icon))
        else:
            self.setIcon(1, self.get_icon(('icons.gui', 'folder-white-shape')))
    
    @staticmethod
    def get_icon(icon_ref):
        return QtGui.QIcon(resources.get_icon(icon_ref))


class FilesList(QtWidgets.QTreeWidget):

    def __init__(self, page_widget, action_widget=None, template_oid=None):
        super(FilesList, self).__init__()
        self.page_widget = page_widget
        self.action_widget = action_widget
        self.template_oid = template_oid

        self.setHeaderLabels(self.get_columns())
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

        self.setStyleSheet('''QTreeView::item:selected {
            background-color: #223e55;
            color: white;
            }'''
        )
        self.setRootIsDecorated(False)

        if template_oid:
            self.refresh()
        
        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)

    def get_columns(self):
        return ('Enabled', 'File', '')
    
    def refresh(self):
        self.blockSignals(True)
        self.clear()

        for item_oid in self.page_widget.parent().get_default_files(self.template_oid):
            name = os.path.basename(item_oid)
            file_name = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/file_name')
            path_format = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/path_format')
            enabled = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/enabled')
            optional = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/optional')

            item = FileItem(self, 'OK', name, file_name, path_format, enabled, optional)

            self.setItemWidget(item, 2, EditItemButton(self, item, 'TaskFile'))

        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
        self.blockSignals(False)

    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.setCurrentItem(None)
        super(FilesList, self).mousePressEvent(event)

    def _on_remove_action_clicked(self, item):
        if item.status == 'REMOVE':
            item.status = 'OK'
            item.setForeground(1, QtGui.QBrush(QtGui.QColor(185, 194, 200)))
            return

        if item.status == 'NEW':
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
            del item
            return

        for item_oid in self.page_widget.parent().get_default_files(self.template_oid):
            file_name = self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/file_name')
            if item.text(1) == file_name:
                item.status = 'REMOVE'
                item.setForeground(1, QtGui.QBrush(QtGui.QColor(221, 80, 80)))
                return

    def _on_context_menu(self, event):
        item = self.itemAt(event)

        if item is None:
            return

        context_menu = QtWidgets.QMenu(self)

        if item.status == 'REMOVE':
            remove = context_menu.addAction(QtGui.QIcon(resources.get_icon(('icons.gui', 'remove-symbol'))), 'Cancel')
        else:
            if self.action_widget is not None:
                label = 'Reset to default'
            else:
                label = 'Remove'
            remove = context_menu.addAction(QtGui.QIcon(resources.get_icon(('icons.gui', 'remove-symbol'))), label)
        
        remove.triggered.connect(lambda checked=False, x=item: self._on_remove_action_clicked(x))

        context_menu.exec_(self.mapToGlobal(event))


class AddTaskTemplate(WizardDialog):

    def __init__(self, page_widget):
        super(AddTaskTemplate, self).__init__(page_widget)
        self.setObjectName('AddTaskTemplate')
        self.button_presets.show()
        self.preset_type = 'task_template'
        self.button_action.setEnabled(False)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Name'), 0, 1, QtCore.Qt.AlignVCenter)
        self.template_name = LineEdit(options='task_template', mandatory=True, custom_widget=self)
        self.template_name.setObjectName('template_name')
        self.template_name.textChanged.connect(self._on_template_name_changed)
        self.content_layout.addWidget(self.template_name, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Color'), 1, 1, QtCore.Qt.AlignVCenter)
        self.color = QtWidgets.QComboBox()
        self.color.setObjectName('color')
        self.color_edit = LineEdit(custom_widget=self)
        self.color_edit.setStyleSheet('QLineEdit { border: none; padding: 0px; }')
        self.color.setLineEdit(self.color_edit)
        colors = self.page_widget.parent().get_template_colors(self.page_widget.parent().project_selected)
        for color in colors:
            self.color.addItem(color)
        if self.color.currentText() == '':
            self.color.setProperty('error', True)
            self.color.style().polish(self.color)
        self.content_layout.addWidget(self.color, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Icon'), 2, 1, QtCore.Qt.AlignVCenter)
        self.icon = LineEdit()
        self.icon.setObjectName('icon')
        self.icon.setText("('icons.gui', 'cog-wheel-silhouette')")
        self.content_layout.addWidget(self.icon, 2, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 3, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Files'), 3, 1, QtCore.Qt.AlignVCenter)
        self.files = FilesList(self.page_widget)
        self.files.setObjectName('files')
        self.files.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_layout.addWidget(self.files, 4, 0, 2, 3, QtCore.Qt.AlignVCenter)

        button_add_file = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add_file.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add_file.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add_file.clicked.connect(self._on_add_file_button_clicked)
        button_add_file.setAutoDefault(False)
        self.content_layout.addWidget(button_add_file, 5, 2, QtCore.Qt.AlignRight)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 6, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Path format'), 6, 1, QtCore.Qt.AlignVCenter)
        self.path_format = LineEdit(custom_widget=self)
        self.path_format.setObjectName('path_format')
        self.content_layout.addWidget(self.path_format, 6, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Add')
    
    def sizeHint(self):
        return QtCore.QSize(600, 395)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, LineEdit):
                    if widget.property('error') == True or (widget.mandatory and widget.text() == ''):
                        return self.button_action.setEnabled(False)
                if isinstance(widget, QtWidgets.QComboBox):
                    if isinstance(widget.lineEdit(), LineEdit):
                        if (
                            widget.lineEdit().property('error') == True
                            or (widget.lineEdit().mandatory and widget.lineEdit().text() == '')
                        ):
                            widget.setProperty('error', True)
                            widget.style().polish(widget)
                            return self.button_action.setEnabled(False)
                        else:
                            widget.setProperty('error', False)
                            widget.style().polish(widget)
        
        return self.button_action.setEnabled(True)
    
    def _on_template_name_changed(self, value):
        original_text = value.lower()
        original_text = re.sub(r'[^a-zA-Z0-9_]+', '', original_text)
        underscore_text = re.sub('\s+', '_', original_text)
        self.template_name.setText(underscore_text)

    def _on_import_triggered(self):
        presetJSON = super(AddTaskTemplate, self)._on_import_triggered()

        for key in presetJSON:
            if key != 'files':
                continue
            for i in range(self.content_layout.count()):
                widget = self.content_layout.itemAt(i).widget()
                if widget.objectName() == key:
                    items = presetJSON[key]
                    for index in items:
                        file_item = False
                        for f in range(self.files.topLevelItemCount()):
                            if self.files.topLevelItem(f).name == items[index]['name']:
                                file_item = True
                                break
                        if not file_item:
                            item = FileItem(
                                self.files,
                                'NEW',
                                items[index]['name'],
                                items[index]['file_name'],
                                items[index]['path_format'],
                                items[index]['enabled'],
                                items[index]['optional']
                            )
                            item.setForeground(1, QtGui.QBrush(QtGui.QColor(100, 221, 80)))
                            self.files.addTopLevelItem(item)
                            self.files.setItemWidget(item, 2, EditItemButton(self.files, item, 'TaskFile'))
                            self.files.resizeColumnToContents(1)

    def _on_add_file_button_clicked(self):
        add_app_dialog = AddFile(self.files)
        add_app_dialog.exec()

    def _on_action_button_clicked(self):
        template = self.page_widget.parent().session.cmds.Flow.call(
            self.page_widget.task_manager.oid() + '/task_templates', 'add_task_template', 
            [
                self.template_name.text(),
                self.color.currentText() or None,
                self.path_format.text() or None
            ], {}
        )

        self.page_widget.parent().session.cmds.Flow.set_value(
            template.oid() + '/icon', eval(self.icon.text())
        )

        for i in range(self.files.topLevelItemCount()):
            item = self.files.topLevelItem(i)
            if item.status == 'NEW':
                self.page_widget.parent().session.cmds.Flow.call(
                    template.oid() + '/files', 'add', [item.name], {}
                )
                self.page_widget.parent().session.cmds.Flow.set_value(
                    template.oid() + '/files/' + item.name + '/file_name', item.file_name
                )
                self.page_widget.parent().session.cmds.Flow.set_value(
                    template.oid() + '/files/' + item.name + '/path_format', item.path_format
                )
                self.page_widget.parent().session.cmds.Flow.set_value(
                    template.oid() + '/files/' + item.name + '/enabled', item.enabled
                )
                self.page_widget.parent().session.cmds.Flow.set_value(
                    template.oid() + '/files/' + item.name + '/optional', item.optional
                )

                print('NEW ', item.name)

        self.page_widget.template_tree.refresh()
        self.page_widget.refresh_dft_list_access()
        self.close()


class EditTaskTemplate(WizardDialog):

    def __init__(self, page_widget, item_oid):
        super(EditTaskTemplate, self).__init__(page_widget)
        self.setObjectName('EditTaskTemplate')
        self.button_presets.show()
        self.preset_type = 'task_template'
        self.item_oid = item_oid

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Color'), 0, 1, QtCore.Qt.AlignVCenter)
        self.color = QtWidgets.QComboBox()
        self.color.setObjectName('color')
        self.color_edit = LineEdit(custom_widget=self)
        self.color_edit.setStyleSheet('QLineEdit { border: none; padding: 0px; }')
        self.color.setLineEdit(self.color_edit)
        self.color_edit.setText(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/color'))
        colors = self.page_widget.parent().get_template_colors(self.page_widget.parent().project_selected)
        for color in colors:
            self.color.addItem(color)
        self.content_layout.addWidget(self.color, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Icon'), 1, 1, QtCore.Qt.AlignVCenter)
        self.icon = LineEdit()
        self.icon.setObjectName('icon')
        self.icon.setText(str(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/icon')))
        self.content_layout.addWidget(self.icon, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Files'), 2, 1, QtCore.Qt.AlignVCenter)
        self.files = FilesList(self.page_widget, template_oid=item_oid)
        self.files.setObjectName('files')
        self.files.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_layout.addWidget(self.files, 3, 0, 2, 3, QtCore.Qt.AlignVCenter)

        button_add_file = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add_file.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add_file.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add_file.clicked.connect(self._on_add_file_button_clicked)
        button_add_file.setAutoDefault(False)
        self.content_layout.addWidget(button_add_file, 4, 2, QtCore.Qt.AlignRight)

        self.content_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')), 5, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Path format'), 5, 1, QtCore.Qt.AlignVCenter)
        self.path_format = LineEdit(custom_widget=self)
        self.path_format.setObjectName('path_format')
        self.path_format.setText(str(self.page_widget.parent().session.cmds.Flow.get_value(item_oid + '/path_format')))
        self.content_layout.addWidget(self.path_format, 5, 2, QtCore.Qt.AlignVCenter)

        self.button_action.setText('Edit')
    
    def sizeHint(self):
        return QtCore.QSize(600, 370)

    def refresh_buttons(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                if isinstance(widget, QtWidgets.QComboBox):
                    if isinstance(widget.lineEdit(), LineEdit):
                        if (
                            widget.lineEdit().property('error') == True 
                            or (widget.lineEdit().mandatory and widget.lineEdit().text() == '')
                        ):
                            widget.setProperty('error', True)
                            widget.style().polish(widget)
                            return self.button_action.setEnabled(False)
                        else:
                            widget.setProperty('error', False)
                            widget.style().polish(widget)
        
        return self.button_action.setEnabled(True)

    def _on_import_triggered(self):
        presetJSON = super(EditTaskTemplate, self)._on_import_triggered()

        for key in presetJSON:
            if key != 'files':
                continue
            for i in range(self.content_layout.count()):
                widget = self.content_layout.itemAt(i).widget()
                if widget.objectName() == key:
                    items = presetJSON[key]
                    for index in items:
                        file_item = None
                        for f in range(self.files.topLevelItemCount()):
                            if self.files.topLevelItem(f).name == items[index]['name']:
                                file_item = self.files.topLevelItem(f)
                                break
                        if file_item is None:
                            item = FileItem(
                                self.files,
                                'NEW',
                                items[index]['name'],
                                items[index]['file_name'],
                                items[index]['path_format'],
                                items[index]['enabled'],
                                items[index]['optional']
                            )
                            item.setForeground(1, QtGui.QBrush(QtGui.QColor(100, 221, 80)))
                            self.files.addTopLevelItem(item)
                            self.files.setItemWidget(item, 2, EditItemButton(self.files, item, 'TaskFile'))
                            self.files.resizeColumnToContents(1)
                        else:
                            properties = vars(file_item)
                            properties = {k: v for k, v in properties.items() if type(v) == str or type(v) == bool}
                            items[index]['status'] = 'OK'
                            if properties == items[index]:
                                continue
                            else:
                                file_item.status = 'EDIT'
                                file_item.setForeground(1, QtGui.QBrush(QtGui.QColor(221, 166, 80)))
                                file_item.windows_path = items[index]['windows_path']
                                file_item.linux_path = items[index]['linux_path']
                                file_item.darwin_path = items[index]['darwin_path']
                                file_item.refresh()
                                self.files.resizeColumnToContents(1)

    def _on_add_file_button_clicked(self):
        add_app_dialog = AddFile(self.files)
        add_app_dialog.exec()
       
    def _on_action_button_clicked(self):
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/color', self.color_edit.text() or None
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/icon', eval(self.icon.text())
        )
        self.page_widget.parent().session.cmds.Flow.set_value(
            self.item_oid + '/path_format', self.path_format.text()
        )

        status_order = ['REMOVE', 'EDIT', 'NEW']

        for status in status_order:
            for i in range(self.files.topLevelItemCount()):
                item = self.files.topLevelItem(i)
                if item.status == status:
                    if status == 'REMOVE':
                        self.page_widget.parent().session.cmds.Flow.call(
                            self.item_oid + '/files', 'remove', [item.name], {}
                        )
                        print('REMOVE ', item.name)
                    if status == 'EDIT':
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/' + item.name + '/file_name', item.file_name
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/' + item.name + '/path_format', item.path_format
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/' + item.name + '/enabled', item.enabled
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/' + item.name + '/optional', item.optional
                        )
                        print('EDIT ', item.name)
                    if status == 'NEW':
                        self.page_widget.parent().session.cmds.Flow.call(
                            self.item_oid + '/files', 'add', [item.name], {}
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/' + item.name + '/file_name', item.file_name
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/' + item.name + '/path_format', item.path_format or None
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/' + item.name + '/enabled', item.enabled
                        )
                        self.page_widget.parent().session.cmds.Flow.set_value(
                            self.item_oid + '/files/' + item.name + '/optional', item.optional
                        )
                        print('NEW ', item.name)

        self.page_widget.template_tree.refresh()
        self.close()


class TaskTemplateItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, name, icon):
        super(TaskTemplateItem, self).__init__(tree)
        self.name = name
        self.icon = icon

        self.refresh()
  
    def refresh(self):
        self.setIcon(0, self.get_icon(self.icon))
        self.setText(0, self.name)
    
    @staticmethod
    def get_icon(icon_ref):
        return QtGui.QIcon(resources.get_icon(icon_ref))


class TaskTemplatesList(QtWidgets.QTreeWidget):

    def __init__(self, page_widget):
        super(TaskTemplatesList, self).__init__()
        self.page_widget = page_widget

        self.setHeaderLabels(self.get_columns())
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setStyleSheet('''QTreeView::item:selected {
            background-color: #223e55;
            color: white;
            }'''
        )
        self.setRootIsDecorated(False)
        
        self.refresh()

        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)
    
    def get_columns(self):
        return ('Name', '')

    def refresh(self):
        self.blockSignals(True)
        self.clear()

        task_templates = self.page_widget.parent().get_task_templates(self.page_widget.parent().project_selected)

        for template in task_templates:
            item = DefaultTaskItem(self, template[1]['Name'], template[1]['_style']['icon'])

            self.setItemWidget(item, 1, EditItemButton(self.page_widget, template[0], 'TaskTemplate'))

        self.resizeColumnToContents(0)
        self.blockSignals(False)
    
    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.setCurrentItem(None)
        super(TaskTemplatesList, self).mousePressEvent(event)


class TasksManager(WizardPage):

    def __init__(self, homepage_widget):
        super(TasksManager, self).__init__(homepage_widget)
        self.homepage_widget = homepage_widget
        self.setObjectName('Tasks')
        self.task_manager = self.homepage_widget.get_task_manager(self.homepage_widget.project_selected)
        
        # Default Tasks
        self.title_widget = QtWidgets.QWidget()
        self.title_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)

        self.title_layout.addWidget(LabelIcon(icon=('icons.flow', 'input')))
        self.title_layout.addWidget(QtWidgets.QLabel('Default Tasks'), QtCore.Qt.AlignLeft)

        self.title_widget.setLayout(self.title_layout)
        self.content_layout.addWidget(self.title_widget)

        # Default Tasks List
        dft_list_layout = QtWidgets.QGridLayout()
        dft_list_layout.setContentsMargins(0, 0, 0, 0)

        self.dft_tree = DefaultTasksList(self)
        self.warning = DefaultTasksWarning(self)
        dft_list_layout.addWidget(self.dft_tree, 0, 0, 2, 0)
        dft_list_layout.addWidget(self.warning, 0, 0, 2, 0)
        
        self.button_add = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        self.button_add.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        self.button_add.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.button_add.clicked.connect(self._on_add_dft_button_clicked)
        dft_list_layout.addWidget(self.button_add, 1, 0, QtCore.Qt.AlignRight)

        self.content_layout.addLayout(dft_list_layout)

        # Task Templates
        self.title_widget2 = QtWidgets.QWidget()
        self.title_widget2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.title_layout2 = QtWidgets.QHBoxLayout()
        self.title_layout2.setContentsMargins(0, 0, 0, 0)

        self.title_layout2.addWidget(LabelIcon(icon=('icons.flow', 'input')))
        self.title_layout2.addWidget(QtWidgets.QLabel('Task Templates'), QtCore.Qt.AlignLeft)

        self.title_widget2.setLayout(self.title_layout2)
        self.content_layout.addWidget(self.title_widget2)

        # Task Templates List
        template_list_layout = QtWidgets.QGridLayout()
        template_list_layout.setContentsMargins(0, 0, 0, 0)

        self.template_tree = TaskTemplatesList(self)
        template_list_layout.addWidget(self.template_tree, 0, 0, 2, 0)
        
        button_add2 = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'plus-black-symbol'))), ''
        )
        button_add2.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button_add2.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button_add2.clicked.connect(self._on_add_template_button_clicked)
        template_list_layout.addWidget(button_add2, 1, 0, QtCore.Qt.AlignRight)

        self.content_layout.addLayout(template_list_layout)

        self.refresh_dft_list_access()

    def refresh_dft_list_access(self):
        if self.template_tree.topLevelItemCount() == 0:
            self.dft_tree.hide()
            self.button_add.hide()
        else:
            self.warning.hide()
            self.dft_tree.show()
            self.button_add.show()

    def _on_add_dft_button_clicked(self):
        dialog = AddDefaultTask(self)
        dialog.exec()

    def _on_add_template_button_clicked(self):
        dialog = AddTaskTemplate(self)
        dialog.exec()

    def _on_back_button_clicked(self):
        self.homepage_widget.layout().itemAt(2).widget().deleteLater()
        back_page = FilesManagement(self.homepage_widget)
        self.homepage_widget.layout().addWidget(back_page, 3)
        self.homepage_widget.setup_steps.refresh(back_page.objectName())

    def _on_next_button_clicked(self):
        self.homepage_widget.page.goto('/Home')


class EditItemButton(QtWidgets.QWidget):

    def __init__(self, page_widget, item, item_type):
        super(EditItemButton, self).__init__(page_widget)
        self.page_widget = page_widget
        self.item_type = item_type

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        button = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'settings'))), ''
        )
        button.setStyleSheet('qproperty-iconSize: 13px; padding: 3px;')
        button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button.clicked.connect(lambda checked=False, x=item: self._on_edit_button_clicked(x))
            
        layout.addStretch()
        layout.addWidget(button)
        self.setLayout(layout)

    def _on_edit_button_clicked(self, item):
        if self.item_type == "Project":
            dialog = EditProject(self.page_widget, item)
        if self.item_type == "User":
            dialog = EditUser(self.page_widget, item)
        if self.item_type == "WorkingSite":
            dialog = EditWorkingSite(self.page_widget, item)
        if self.item_type == "Application":
            dialog = EditApplication(self.page_widget, item)
        if self.item_type == "ExchangeSite":
            dialog = EditExchangeSite(self.page_widget, item)
        if self.item_type == "DefaultTask":
            dialog = EditDefaultTask(self.page_widget, item)
        if self.item_type == "TaskFile":
            dialog = EditFile(self.page_widget, item)
        if self.item_type == "TaskTemplate":
            dialog = EditTaskTemplate(self.page_widget, item)
        dialog.exec()


class WizardHomePageWidget(CustomPageWidget):

    def build(self):
        self.project_selected = ''
        self.setStyleSheet(STYLESHEET)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        base_layout = QtWidgets.QHBoxLayout()

        # First page init
        self.current_page = GlobalSettings(self)
        
        # Setup steps
        self.setup_steps = SetupSteps(self)

        # Line separator
        separator = QtWidgets.QFrame()
        separator.setFrameStyle(QtWidgets.QFrame.VLine | QtWidgets.QFrame.Plain)

        # Base setup
        base_layout.addWidget(self.setup_steps, 1)
        base_layout.addWidget(separator, 2)
        base_layout.addWidget(self.current_page, 3)
        self.setLayout(base_layout)

        self.setup_steps.refresh()

    def sizeHint(self):
        return QtCore.QSize(0, 3840)

    # Global settings
    def get_projects(self):
        return self.session.cmds.Flow.call(
            '/Home', 'get_projects', {}, {}
        )

    def get_project_settings(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'settings', {}, {}
        )

    def get_project_name(self, name):
        return self.session.cmds.Flow.get_value(self.get_project_settings(name).oid() + '/project_nice_name')

    def set_project_name(self, name, value):
        return self.session.cmds.Flow.set_value(self.get_project_settings(name).oid() + '/project_nice_name', value)
    
    def get_project_thumbnail(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_project_thumbnail', {}, {}
        )

    def set_project_thumbnail(self, name, value):
        return self.session.cmds.Flow.set_value(self.get_project_settings(name).oid() + '/project_thumbnail', value)

    # MongoDB
    def get_entity_store(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_entity_store', {}, {}
        )

    def get_db_info(self, entity_store):
        return self.session.cmds.Flow.call(
            entity_store, 'get_db_info', {}, {}
        )

    def set_db_uri(self, entity_store, value):
        return self.session.cmds.Flow.set_value(entity_store + '/uri', value)

    # Kitsu
    def get_kitsu_config(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'kitsu_config', {}, {}
        )

    def update_kitsu_host(self, name, server_url):
        return self.session.cmds.Flow.call(
            '/' + name, 'update_kitsu_host', {server_url}, {}
        )

    # Users
    def get_users(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_users', {}, {}
        )
    
    def get_user_kitsu_login(self, user_oid):
        kitsu_api = self.session.cmds.Flow.call(
            '/' + user_oid.split('/')[1], 'kitsu_api', {}, {}
        )
        return self.session.cmds.Flow.call(
            kitsu_api.oid(), 'get_user_login', [user_oid.split('/')[-1]], {}
        )
    
    def set_user_kitsu_login(self, user_oid, kitsu_login):
        kitsu_api = self.session.cmds.Flow.call(
            '/' + user_oid.split('/')[1], 'kitsu_api', {}, {}
        )
        return self.session.cmds.Flow.call(
            kitsu_api.oid(), 'set_user_login', [user_oid.split('/')[-1], kitsu_login], {}
        )

    def add_user(self, project_name, user_id, login, kitsu_login, status):
        users_map = self.get_users(project_name)
        # Add user
        self.session.cmds.Flow.call(
            users_map.oid(), 'add_user', [user_id, login, status], {}
        )
        # Set user Kitsu login
        kitsu_api = self.session.cmds.Flow.call(
            '/' + project_name, 'kitsu_api', {}, {}
        )
        self.session.cmds.Flow.call(
            kitsu_api.oid(), 'set_user_login', [user_id, kitsu_login or None], {}
        )

    # Working sites
    def get_working_sites(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_working_sites', {}, {}
        )

    def add_working_site(self, project_name, value):
        site_map = self.get_working_sites(project_name)
        return self.session.cmds.Flow.call(
            site_map.oid(), 'add', [value], {}
        )

    def get_root(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_root', {}, {}
        )

    def get_site_environnement(self, site_oid):
        return self.session.cmds.Flow.get_mapped_oids(site_oid + "/site_environment")

    def get_factory(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_factory', {}, {}
        )

    # Exchange sites
    def get_exchange_sites(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_exchange_sites', {}, {}
        )

    def get_exchange_site(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_exchange_site', {}, {}
        )

    def set_exchange_site(self, name, site_name):
        return self.session.cmds.Flow.call(
            '/' + name, 'set_exchange_site', {site_name}, {}
        )

    def add_exchange_site(self, project_name, value):
        site_map = self.get_exchange_sites(project_name)
        return self.session.cmds.Flow.call(
            site_map.oid(), 'add', [value], {}
        )
    
    # Files management
    def get_contextual_dict(self, name, context_name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_contextual_view', [context_name], {}
        )
    
    def get_path_format(self, project_name):
        contextual_dict = self.get_contextual_dict(project_name, "settings")
        path_format = None
        for item in contextual_dict.mapped_items():
            if item.value_name.get() == "path_format":
                path_format = item
                break
        return path_format

    # Task Manager
    def get_task_manager(self, name):
        return self.session.cmds.Flow.call(
            '/' + name, 'get_task_manager', {}, {}
        )

    def get_default_tasks(self, name):
        mng = self.get_task_manager(name)
        return self.session.cmds.Flow.get_mapped_rows(mng.oid() + '/default_tasks')

    def get_task_templates(self, name):
        mng = self.get_task_manager(name)
        return self.session.cmds.Flow.get_mapped_rows(mng.oid() + '/task_templates')

    def get_template_colors(self, name):
        mng = self.get_task_manager(name)
        return self.session.cmds.Flow.get_value(mng.oid() + '/template_colors')

    def get_default_files(self, template_oid):
        return self.session.cmds.Flow.get_mapped_oids(template_oid + "/files")
