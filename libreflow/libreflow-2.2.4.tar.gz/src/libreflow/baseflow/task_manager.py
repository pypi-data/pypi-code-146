import os
import time
from kabaret import flow
from kabaret.flow_contextual_dict import get_contextual_dict
from kabaret.app.ui.gui.icons import gui

from ..resources.icons import gui, libreflow
from .runners import CHOICES_ICONS


DEFAULT_PATH_FORMAT = '{film}/{sequence}/{shot}/{task}/{file_mapped_name}/{revision}/{film}_{sequence}_{shot}_{file_base_name}'


def get_icon(file_name):
    _, ext = os.path.splitext(file_name)
    icon = ('icons.gui', 'folder-white-shape')
    if ext:
        icon = CHOICES_ICONS.get(
            ext[1:], ('icons.gui', 'text-file-1')
        ) 

    return icon


# Task default files
# -------------------------


class SelectDefaultFileAction(flow.Action):

    _default_file = flow.Parent()
    _map          = flow.Parent(2)

    def needs_dialog(self):
        return False
    
    def allow_context(self, context):
        return False
    
    def run(self, button):
        if self._default_file.exists.get():
            return
        
        self._default_file.create.set(
            not self._default_file.create.get()
        )
        self._map.touch()


class TaskDefaultFileViewItem(flow.SessionObject):
    """
    Describes a default file to be created in the list of
    files of a task.
    """
    file_name   = flow.Param()
    path_format = flow.Param()
    create      = flow.BoolParam()
    exists      = flow.BoolParam()

    select      = flow.Child(SelectDefaultFileAction)


class TaskDefaultFileView(flow.DynamicMap):

    _task = flow.Parent(2)

    def __init__(self, parent, name):
        super(TaskDefaultFileView, self).__init__(parent, name)
        self._cache = None
        self._cache_ttl = 5
        self._cache_birth = None
        self._cache_key = None

    @classmethod
    def mapped_type(cls):
        return TaskDefaultFileViewItem

    def mapped_names(self, page_num=0, page_size=None):
        cache_key = (page_num, page_size)
        if (
            self._cache is None
            or self._cache_key != cache_key
            or self._cache_birth < time.time() - self._cache_ttl
        ):
            self._mng.children.clear()

            mgr = self.root().project().get_task_manager()
            default_files = mgr.get_task_files(
                self._task.name(), enabled_only=True
            )

            self._cache = {}

            for file_name, path_format, optional in default_files:
                n = file_name.replace('.', '_')
                self._cache[n] = dict(
                    file_name=file_name,
                    path_format=path_format,
                    create=not optional,
                    exists=self._file_exists(file_name)
                )
            
            self._cache_birth = time.time()
            self._cache_key = cache_key
        
        return self._cache.keys()
    
    def columns(self):
        return ['Do create', 'File']
    
    def _configure_child(self, child):
        self.mapped_names()
        child.file_name.set(self._cache[child.name()]['file_name'])
        child.path_format.set(self._cache[child.name()]['path_format'])
        child.create.set(self._cache[child.name()]['create'])
        child.exists.set(self._cache[child.name()]['exists'])
    
    def _fill_row_cells(self, row, item):
        row['Do create'] = ''
        row['File'] = item.file_name.get()
    
    def _fill_row_style(self, style, item, row):
        style['File_icon'] = get_icon(item.file_name.get())
        style['Do create_activate_oid'] = item.select.oid()

        if item.exists.get():
            style['Do create_icon'] = ('icons.gui', 'check-box-empty-dark')
            for col in self.columns():
                style['%s_foreground-color' % col] = '#4e5255'
        elif item.create.get():
            style['Do create_icon'] = ('icons.gui', 'check')
        else:
            style['Do create_icon'] = ('icons.gui', 'check-box-empty')
    
    def _file_exists(self, file_name):
        name, ext = os.path.splitext(file_name)
        if ext:
            exists = self._task.files.has_file(name, ext[1:])
        else:
            exists = self._task.files.has_folder(name)
        return exists


class CreateTaskDefaultFiles(flow.Action):

    files = flow.Child(TaskDefaultFileView)

    _task = flow.Parent()

    def get_buttons(self):
        task = self._task.name()
        self.message.set(f'<h2>Create {task} default files</h2>')
        return ['Create', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        for df in self.files.mapped_items():
            if df.create.get() and not df.exists.get():
                self._create_file(df)
    
    def _create_file(self, default_file):
        file_name = default_file.file_name.get()
        name, ext = os.path.splitext(file_name)
        if ext:
            self._task.files.add_file(
                name, ext[1:],
                display_name=file_name,
                tracked=True,
                default_path_format=default_file.path_format.get()
            )
        else:
            self._task.files.add_folder(
                name,
                display_name=file_name,
                tracked=True,
                default_path_format=default_file.path_format.get()
            )


# Default file presets
# -------------------------


class FileTypeValue(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'

    def choices(self):
        return ['Inputs', 'Outputs', 'Works']


class PathFormatValue(flow.values.SessionValue):

    def revert_to_default(self):
        settings = get_contextual_dict(self, 'settings')
        path_format = settings.get('path_format')
        if path_format is None:
            super(PathFormatValue, self).revert_to_default()
        else:
            self.set(path_format)


class CreateDefaultFileAction(flow.Action):
    """
    Allows to create a default file in the parent map.
    """

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    file_name   = flow.SessionParam('').ui(
        placeholder='layout.blend'
    )
    file_type   = flow.SessionParam(None, FileTypeValue)
    path_format = flow.SessionParam(DEFAULT_PATH_FORMAT, PathFormatValue).ui(
        placeholder='{film}/{shot}/{file}/{revision}'
    )
    enabled     = flow.SessionParam(True).ui(editor='bool')
    optional    = flow.SessionParam(False).ui(editor='bool')
    is_primary_file = flow.SessionParam(False).ui(editor='bool')

    _map = flow.Parent()

    def get_buttons(self):
        self.message.set('<h2>Create a default file</h2>')
        self.path_format.revert_to_default()
        return ['Add', 'Cancel']
   
    def run(self, button):
        if button == 'Cancel':
            return
        elif not self._filename_is_valid():
            return self.get_result(close=False)
        
        mapped_name = self.file_name.get().replace('.', '_')
        path_format = self.path_format.get() or None # Consider empty path format as undefined

        df = self._map.add(mapped_name)
        df.file_name.set(self.file_name.get())
        df.file_type.set(self.file_type.get())
        df.enabled.set(self.enabled.get())
        df.optional.set(self.optional.get())
        df.is_primary_file.set(self.is_primary_file.get())
        df.path_format.set(path_format)

        self._map.touch()
    
    def _filename_is_valid(self):
        title = '<h2>Create a default file</h2>'

        if self.file_name.get() == '':
            self.message.set((
                f'{title}<font color=#D66700>'
                'File name must not be empty.</font>'
            ))
            return False
        
        for df in self._map.mapped_items():
            if self.file_name.get() == df.file_name.get():
                self.message.set((
                    f'{title}<font color=#D66700>A default file '
                    f'named <b>{self.file_name.get()}</b> already '
                    'exists. Please choose another name.</font>'
                ))
                return False
        
        return True


class DefaultFile(flow.Object):
    """
    Defines a preset used to create a file in the project.
    """

    file_name   = flow.Param()
    file_type   = flow.Param()
    path_format = flow.Param()
    enabled     = flow.BoolParam(False)
    optional    = flow.BoolParam(False)
    is_primary_file = flow.BoolParam(False)


class DefaultFiles(flow.Map):

    add_dft_file = flow.Child(CreateDefaultFileAction).ui(
        label='Add default file'
    )

    @classmethod
    def mapped_type(cls):
        return DefaultFile
    
    def columns(self):
        return ['Enabled', 'Name']
    
    def _fill_row_cells(self, row, item):
        row['Name'] = item.file_name.get()
        row['Enabled'] = ''
    
    def _fill_row_style(self, style, item, row):
        style['Name_icon'] = get_icon(item.file_name.get())
        style['Enabled_icon'] = (
            'icons.gui',
            'check' if item.enabled.get() else 'check-box-empty'
        )


# Task UI types
# -------------------------


class TaskColor(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'

    def choices(self):
        mgr = self.root().project().get_task_manager()
        return mgr.template_colors.get()
    
    def update_default_value(self):
        choices = self.choices()
        if choices:
            self._value = choices[0]
        self.touch()


class EditTaskColorAction(flow.Action):

    color = flow.SessionParam(None, TaskColor)

    _task_color = flow.Parent()

    def get_buttons(self):
        self.color.update_default_value()
        return ['Save', 'Cancel']
    
    def allow_context(self, context):
        return context and context.endswith('.inline')
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        self._task_color.set(self.color.get())


class EditableTaskColor(flow.values.Value):

    edit = flow.Child(EditTaskColorAction)


# Default tasks
# -------------------------


class KitsuTaskName(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'

    def choices(self):
        return sorted(self.root().project().kitsu_api().get_task_types())
    
    def update_default_value(self):
        choices = self.choices()
        if choices:
            self._value = choices[0]
        self.touch()


class AddKitsuTaskNameAction(flow.Action):

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    kitsu_task = flow.SessionParam(None, KitsuTaskName)

    _value = flow.Parent()

    def get_buttons(self):
        self.kitsu_task.update_default_value()
        return ['Add', 'Cancel']
    
    def allow_context(self, context):
        return context and context.endswith('.inline')
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        self._value.add(self.kitsu_task.get().split(' - ')[1], 0)


class ExistingKitsuTaskNames(flow.values.SessionValue):

    DEFAULT_EDITOR = 'multichoice'
    STRICT_CHOICES = False

    _task_names = flow.Parent(2)

    def choices(self):
        return self._task_names.get()


class RemoveKitsuTaskNameAction(flow.Action):

    ICON = ('icons.gui', 'minus-button')

    kitsu_tasks = flow.SessionParam(list, ExistingKitsuTaskNames)

    _value = flow.Parent()

    def get_buttons(self):
        self.kitsu_tasks.revert_to_default()
        return ['Confirm', 'Cancel']
    
    def allow_context(self, context):
        return context and context.endswith('.inline')
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        for name in self.kitsu_tasks.get():
            self._value.remove(name)


class EditableKitsuTaskNames(flow.values.OrderedStringSetValue):

    add_action = flow.Child(AddKitsuTaskNameAction).ui(label='Add')
    remove_action = flow.Child(RemoveKitsuTaskNameAction).ui(label='Remove')


class EditDefaultTaskFile(flow.Action):
    """
    Allows to edit a default task's file.
    """

    ICON = ('icons.libreflow', 'edit-blank')

    path_format = flow.SessionParam(DEFAULT_PATH_FORMAT, PathFormatValue).ui(
        placeholder='{film}/{shot}/{file}/{revision}'
    )
    file_type   = flow.SessionParam(None, FileTypeValue)
    enabled     = flow.SessionParam().ui(editor='bool')
    optional    = flow.SessionParam().ui(editor='bool')

    _dft_file   = flow.Parent()
    _map        = flow.Parent(2)
    _dft_task   = flow.Parent(3)

    def get_buttons(self):
        self.message.set(f'<h2>Edit default file {self._dft_file.file_name.get()}</h2>')
        self.file_type.set(self._dft_file.file_type.get())
        self.path_format.set(self._dft_file.path_format.get())
        self.enabled.set(self._dft_file.enabled.get())
        self.optional.set(self._dft_file.optional.get())

        buttons = ['Save']
        mgr = self.root().project().get_task_manager()
        task_template = mgr.task_templates[self._dft_task.template.get()]

        if task_template.files.has_mapped_name(self._dft_file.name()):
            buttons.append('Restore default')
        
        return buttons + ['Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return

        if button == 'Restore default':
            self._map.edits.remove(self._dft_file.name())
        else:
            if self._map.edits.has_mapped_name(self._dft_file.name()):
                dft_file = self._map.edits[self._dft_file.name()]
            else:
                mgr = self.root().project().get_task_manager()
                task_template = mgr.task_templates[self._dft_task.template.get()]
                file_name = task_template.files[self._dft_file.name()].file_name.get()
                dft_file = self._map.edits.add(self._dft_file.name())
                dft_file.file_name.set(file_name)
            
            dft_file.file_type.set(self.file_type.get())
            dft_file.path_format.set(self.path_format.get())
            dft_file.enabled.set(self.enabled.get())
            dft_file.optional.set(self.optional.get())


        self._map.touch()


class RemoveDefaultTaskFile(flow.Action):
    """
    Allows to remove a default task's file.
    """

    ICON = ('icons.gui', 'remove-symbol')

    _dft_file   = flow.Parent()
    _map        = flow.Parent(2)
    _task       = flow.Parent(3)
    _mgr        = flow.Parent(5)

    def allow_context(self, context):
        return context and self._dft_file.is_edit.get()

    def get_buttons(self):
        self.message.set(
            f'Remove <b>{self._dft_file.file_name.get()}</b> '
            f'from task <b>{self._task.name()}</b> files ?'
        )
        return ['Confirm', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return

        self._map.edits.remove(self._dft_file.name())
        if self._mgr.default_files.has_key(self._dft_file.name()):
            store = self._mgr.default_files.get_key(self._dft_file.name())
            if self._task.name() in store:
                store.remove(self._task.name())
                if not store:
                    self._mgr.default_files.del_key(self._dft_file.name())
                else:
                    self._mgr.default_files.set_key(self._dft_file.name(), store)
        self._map.touch()


class AddDefaultTaskFileEdit(flow.Action):
    """
    Allows to add a file in the files of a default task.
    """

    file_name   = flow.SessionParam('').ui(label='Name')
    file_type   = flow.SessionParam(None, FileTypeValue)
    path_format = flow.SessionParam(DEFAULT_PATH_FORMAT, PathFormatValue)
    enabled     = flow.SessionParam(True).ui(editor='bool')
    optional    = flow.SessionParam(False).ui(editor='bool')
    is_primary_file = flow.SessionParam(False).ui(editor='bool')

    _map = flow.Parent()
    _task = flow.Parent(2)
    _mgr = flow.Parent(4)

    def get_buttons(self):
        self.message.set('<h2>Add default task file</h2>')
        self.path_format.revert_to_default()
        return ['Add', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        elif not self._filename_is_valid():
            self.message.set((
                f'<font color=#D66700>A default file '
                f'named <b>{self.file_name.get()}</b> already '
                'exists. Please choose another name.</font>'
            ))
            return self.get_result(close=False)
        
        file_name = self.file_name.get()
        df = self._map.edits.add(file_name.replace('.', '_'))
        df.file_name.set(self.file_name.get())
        df.file_type.set(self.file_type.get())
        df.path_format.set(self.path_format.get())
        df.enabled.set(self.enabled.get())
        df.optional.set(self.optional.get())
        df.is_primary_file.set(self.is_primary_file.get())

        if self._mgr.default_files.has_key(file_name):
            store = self._mgr.default_files.get_key(file_name)
            if self._task.name() not in store:
                store.append(self._task.name())
                self._mgr.default_files.set_key(file_name, store)
        else:
            self._mgr.default_files.set_key(file_name, [self._task.name()])

        self._map.touch()
    
    def _filename_is_valid(self):
        title = '<h2>Add default task file</h2>'

        if self.file_name.get() == '':
            self.message.set((
                f'{title}<font color=#D66700>'
                'File name must not be empty.</font>'
            ))
            return False
        
        for df in self._map.mapped_items():
            if self.file_name.get() == df.file_name.get():
                self.message.set((
                    f'{title}<font color=#D66700>A default file '
                    f'named <b>{self.file_name.get()}</b> already '
                    'exists. Please choose another name.</font>'
                ))
                return False
        
        return True


class DefaultTaskFile(flow.SessionObject):

    file_name   = flow.Param().ui(editable=False)
    path_format = flow.Param().ui(editable=False)
    file_type   = flow.Param().ui(editable=False)
    enabled     = flow.BoolParam().ui(editable=False)
    optional    = flow.BoolParam().ui(editable=False)
    is_primary_file = flow.BoolParam().ui(editable=False)
    is_edit     = flow.BoolParam().ui(editable=False)

    edit        = flow.Child(EditDefaultTaskFile)
    remove      = flow.Child(RemoveDefaultTaskFile)


class DefaultTaskFiles(flow.DynamicMap):

    edits = flow.Child(DefaultFiles).ui(hidden=True)

    add_dft_file = flow.Child(AddDefaultTaskFileEdit).ui(label='Add default file')

    _default_task = flow.Parent()

    def mapped_names(self, page_num=0, page_size=None):
        self._mng.children.clear()

        mgr = self.root().project().get_task_manager()
        task_template = mgr.task_templates[self._default_task.template.get()]
        default_names = task_template.files.mapped_names()
        edit_names = set(self.edits.mapped_names())

        self._cache = {}

        # Collect default files (potentially edited)
        for name in default_names:
            data = {}
            if name in edit_names:
                default_file = self.edits[name]
                # Path format evaluation order: edit > default task > template file > template
                path_format = (
                    default_file.path_format.get()
                    or self._default_task.path_format.get()
                    or task_template.files[name].path_format.get()
                    or task_template.path_format.get()
                )
                data['is_edit'] = True
                edit_names.remove(name)
            else:
                default_file = task_template.files[name]
                path_format = default_file.path_format.get() or task_template.path_format.get()
                data['is_edit'] = False
            data.update(dict(
                file_name=default_file.file_name.get(),
                file_type=default_file.file_type.get(),
                path_format=path_format,
                enabled=default_file.enabled.get(),
                optional=default_file.optional.get(),
                is_primary_file=default_file.is_primary_file.get()
            ))
            self._cache[name] = data
        
        # Collect remaining edits
        for name in edit_names:
            default_file = self.edits[name]
            # Path format evaluation order: edit > default task > template
            path_format = (
                default_file.path_format.get()
                or self._default_task.path_format.get()
                or task_template.path_format.get()
            )
            data = dict(
                file_name=default_file.file_name.get(),
                file_type=default_file.file_type.get(),
                path_format=path_format,
                enabled=default_file.enabled.get(),
                optional=default_file.optional.get(),
                is_primary_file=default_file.is_primary_file.get(),
                is_edit=True
            )
            self._cache[name] = data
        
        for name in self._cache:
            primary_files = self._default_task.primary_files.get()
            if self._cache[name]['enabled'] and self._cache[name]['is_primary_file']:
                if self._cache[name]['file_name'] not in self._default_task.primary_files.get():
                    primary_files.append(self._cache[name]['file_name'])
                    self._default_task.primary_files.set(primary_files)

            if mgr.default_files.has_key(self._cache[name]['file_name']):
                store = mgr.default_files.get_key(self._cache[name]['file_name'])
                if self._default_task.name() in store:
                    continue
                else:
                    store.append(self._default_task.name())
                    mgr.default_files.set_key(self._cache[name]['file_name'], store)
            else:
                mgr.default_files.set_key(self._cache[name]['file_name'], [self._default_task.name()])
        
        return self._cache.keys()
    
    @classmethod
    def mapped_type(cls):
        return DefaultTaskFile
    
    def _configure_child(self, child):
        child.file_name.set(self._cache[child.name()]['file_name'])
        child.file_type.set(self._cache[child.name()]['file_type'])
        child.path_format.set(self._cache[child.name()]['path_format'])
        child.enabled.set(self._cache[child.name()]['enabled'])
        child.optional.set(self._cache[child.name()]['optional'])
        child.is_primary_file.set(self._cache[child.name()]['is_primary_file'])
        child.is_edit.set(self._cache[child.name()]['is_edit'])
    
    def columns(self):
        return ['Enabled', 'Name']
    
    def _fill_row_cells(self, row, item):
        row['Name'] = item.file_name.get()
        row['Enabled'] = ''
    
    def _fill_row_style(self, style, item, row):
        style['Name_icon'] = get_icon(item.file_name.get())
        style['Enabled_icon'] = (
            'icons.gui',
            'check' if item.enabled.get() else 'check-box-empty'
        )
        style['activate_oid'] = item.edit.oid()


class TaskTemplateName(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'

    def choices(self):
        mgr = self.root().project().get_task_manager()
        return mgr.task_templates.mapped_names()
    
    def update_default_value(self):
        choices = self.choices()
        if choices:
            self._value = choices[0]
        self.touch()


class EditTaskTemplateNameAction(flow.Action):

    template = flow.SessionParam(None, TaskTemplateName)

    _task_template = flow.Parent()

    def get_buttons(self):
        self.template.update_default_value()
        return ['Save', 'Cancel']
    
    def allow_context(self, context):
        return context and context.endswith('.inline')
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        self._task_template.set(self.template.get())


class EditableTaskTemplateName(flow.values.Value):

    edit = flow.Child(EditTaskTemplateNameAction)


class CreateDefaultTaskAction(flow.Action):

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    task_name    = flow.SessionParam('')
    display_name = flow.SessionParam('')
    template     = flow.SessionParam(None, TaskTemplateName)
    position     = flow.SessionParam(0).ui(editor='int')
    path_format  = flow.SessionParam('')
    enabled      = flow.SessionParam(True).ui(
        editor='bool',
        tooltip='Dictates if the task must appear in the UI by default')
    optional     = flow.SessionParam(False).ui(
        editor='bool',
        tooltip='Dictates if the task must be created automatically')

    _map      = flow.Parent()

    def get_buttons(self):
        self.template.update_default_value()

        if len(self.template.choices()) == 0:
            self.message.set((
                '<h2>Add default task</h2>'
                '<font color=#D5000D>Please add a template '
                'before creating a default task.</font>'
            ))
            return ['Cancel']
        
        self.message.set('<h2>Add default task</h2>')
        return ['Add', 'Cancel']

    def run(self, button):
        if button == 'Cancel':
            return
        
        self._map.add_default_task(
            self.task_name.get(),
            self.display_name.get(),
            self.template.get(),
            self.position.get(),
            self.path_format.get() or None,
            self.enabled.get(),
            self.optional.get()
        )


class KitsuTasksMultiChoiceValue(flow.values.SessionValue):

    DEFAULT_EDITOR = 'multichoice'

    _action = flow.Parent()

    def choices(self):       
        return self._action.tasksData.get()


class CreateKitsuTasksPage1(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    tasksData = flow.Computed(cached=True, store_value=False).ui(hidden=True)
    tasksChoice = flow.Param([], KitsuTasksMultiChoiceValue).ui(label='Tasks')

    _map = flow.Parent()
    _mgr = flow.Parent(2)

    def get_buttons(self):
        self.tasksData.touch()
        self.message.set('<h2>Select tasks to create</h2>')
        return ['Select', 'Cancel']

    def compute_child_value(self, child_value):
        if child_value is self.tasksData:
            task_types = sorted(self.root().project().kitsu_api().get_task_types())
            task_types = [t for t in task_types
            if t.split(' - ')[1] != "FDT"
            if self._mgr.task_templates.has_mapped_name(t.split(' - ')[0].lower())
            if self._mgr.default_tasks.has_mapped_name(t.split(' - ')[1].lower()) == False]

            for t in task_types:
                task_type, task_name = t.split(' - ')
                for dft_task in self._mgr.default_tasks.mapped_items():
                    if task_name in dft_task.kitsu_tasks.get():
                        task_types.remove(t)
                        break
            
            self.tasksData.set(task_types)
   
    def run(self, button):
        if button == 'Cancel':
            return
        
        return self.get_result(next_action=self._map.add_kitsu_tasks_page2.oid())


class KitsuTaskData(flow.Object):

    task_type = flow.Param().ui(editable=False)
    task_name = flow.Param()


class KitsuTasksChoices(flow.DynamicMap):

    _map = flow.Parent(2)

    def __init__(self, parent, name):
        super(KitsuTasksChoices, self).__init__(parent, name)
        self.tasks = None

    @classmethod
    def mapped_type(cls):
        return KitsuTaskData
    
    def mapped_names(self, page_num=0, page_size=None):
        choices = self._map.add_kitsu_tasks.tasksChoice.get()

        self.tasks = {}
        for i, task in enumerate(choices):
            data = {}
            data.update(dict(
                task_type=task.split(' - ')[0],
                task_name=task.split(' - ')[1]
            ))
            self.tasks['task'+str(i)] = data
        
        return self.tasks.keys()

    def columns(self):
        return ['Type', 'Name']

    def _configure_child(self, child):
        child.task_type.set(self.tasks[child.name()]['task_type'])
        child.task_name.set(self.tasks[child.name()]['task_name'])

    def _fill_row_cells(self, row, item):
        row['Type'] = item.task_type.get()
        row['Name'] = item.task_name.get()


class CreateKitsuTasksPage2(flow.Action):

    tasks = flow.Child(KitsuTasksChoices).ui(expanded=True)

    _map = flow.Parent()
    _mgr = flow.Parent(2)

    def allow_context(self, context):
        return context and context.endswith('.details')

    def get_buttons(self):
        self.message.set('<h2>Rename tasks if needed</h2>')
        return ['Create tasks', 'Back']

    def run(self, button):
        if button == 'Back':
            return self.get_result(next_action=self._map.add_kitsu_tasks.oid())
        
        for item in self.tasks.mapped_items():
            if not self._mgr.default_tasks.has_mapped_name(item.task_name.get().lower()):
                t = self._mgr.default_tasks.add_default_task(
                    item.task_name.get().lower(),
                    item.task_name.get(),
                    item.task_type.get().lower()
                )
                t.kitsu_tasks.add(item.task_name.get(), 0)
            else:
                continue
            
            print(f'Create default task: {item.task_name.get()}')
        
        self._mgr.default_tasks.touch()


class DefaultTask(flow.Object):
    """
    Defines a set of presets used to create a task in the project.

    These presets include UI elements (display name and position),
    dictate if the associated tasks are enabled in the project and
    optional at creation time.
    In addition, each default task has a task template, and holds
    a set of parameters and a list of default files used to
    override the template's defaults.
    """

    display_name = flow.Param()
    position     = flow.IntParam(0)
    enabled      = flow.BoolParam(True)
    optional     = flow.BoolParam(False)

    # Template and parameters overriding its configuration
    template     = flow.Param(None, EditableTaskTemplateName).ui(editable=False)
    color        = flow.Param(None, EditableTaskColor)
    icon         = flow.Param()
    files        = flow.Child(DefaultTaskFiles).ui(expanded=True)
    path_format  = flow.Param()
    primary_files = flow.Param([]).ui(editable=False)
    kitsu_tasks   = flow.OrderedStringSetParam(EditableKitsuTaskNames).ui(editable=False)
    priority_actions  = flow.Param()

    subtasks     = flow.OrderedStringSetParam()

    assignation_enabled = flow.BoolParam(True)

    def get_color(self):
        color = self.color.get()

        if not color:
            mgr = self.root().project().get_task_manager()
            tp = mgr.task_templates[self.template.get()]
            color = tp.color.get()
        
        return color

    def get_icon(self):
        icon = self.icon.get()

        if not icon:
            mgr = self.root().project().get_task_manager()
            tp = mgr.task_templates[self.template.get()]
            icon = tp.icon.get()
        
        return tuple(icon)
    
    def get_primary_file_names(self):
        names = self.primary_files.get()

        if not names:
            mgr = self.root().project().get_task_manager()
            tp = mgr.task_templates[self.template.get()]
            names = tp.primary_files.get()
        
        return names or None
    
    def get_display_name(self):
        return self.display_name.get()
    
    def get_path_format(self):
        '''
        Returns the path format of this default task if defined,
        or the path format of its template otherwise.
        '''
        path_format = self.path_format.get()
        
        if path_format is None:
            mgr = self.root().project().get_task_manager()
            tp = mgr.task_templates[self.template.get()]
            path_format = tp.path_format.get()
        
        return path_format


class DefaultTasks(flow.Map):

    add_dft_task = flow.Child(CreateDefaultTaskAction).ui(
        label='Add default task'
    )
    add_kitsu_tasks = flow.Child(CreateKitsuTasksPage1)
    add_kitsu_tasks_page2 = flow.Child(CreateKitsuTasksPage2).ui(hidden=True)

    @classmethod
    def mapped_type(cls):
        return DefaultTask

    def add_default_task(self, name, display_name, template_name, position=-1, path_format=None, enabled=True, optional=False):
        if position < 0:
            position = len(self)
        
        dt = self.add(name)
        dt.display_name.set(display_name)
        dt.position.set(position)
        dt.template.set(template_name)
        dt.path_format.set(path_format)
        dt.enabled.set(enabled)
        dt.optional.set(optional)
        self._mapped_names.set_score(name, position)
        
        self.touch()
        return dt
    
    def _fill_row_cells(self, row, item):
        row['Name'] = item.display_name.get()
    
    def _fill_row_style(self, style, item, row):
        style['icon'] = item.get_icon()
        style['background-color'] = item.get_color()


# Task templates
# -------------------------


class CreateTaskTemplateAction(flow.Action):

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    template_name = flow.SessionParam('').ui(label='Name')
    color         = flow.SessionParam(None, TaskColor)
    path_format   = flow.SessionParam('')

    _map = flow.Parent()

    def get_buttons(self):
        self.color.update_default_value()
        self.message.set('<h2>Add task template</h2>')
        return ['Add', 'Cancel']

    def run(self, button):
        if button == 'Cancel':
            return
        
        tt = self._map.add_task_template(
            self.template_name.get(),
            self.color.get(),
            self.path_format.get() or None
        )
        self._map.touch()


class TaskTemplate(flow.Object):
    """
    A task template defines a generic task configuration,
    which can be overriden by default tasks.
    """
    
    color = flow.Param(None, EditableTaskColor)
    icon  = flow.Param(('icons.gui', 'cog-wheel-silhouette'))
    files = flow.Child(DefaultFiles).ui(expanded=True)
    path_format = flow.Param()
    primary_files = flow.Computed(None).ui(editable=False)

    def compute_child_value(self, child_value):
        if child_value is self.primary_files:
            files = []
            for dft_file in self.files.mapped_items():
                if dft_file.enabled.get() and dft_file.is_primary_file.get():
                    files.append(dft_file.file_name.get())
            
            self.primary_files.set(files)


class TaskTemplates(flow.Map):

    add_template = flow.Child(CreateTaskTemplateAction)

    @classmethod
    def mapped_type(cls):
        return TaskTemplate

    def add_task_template(self, template_name, color, path_format=None):
        template = self.add(template_name.lower())
        template.color.set(color)
        template.path_format.set(path_format)
        
        self.touch()
        return template
    
    def _fill_row_style(self, style, item, row):
        style['icon'] = item.icon.get()
        style['background-color'] = item.color.get()


# Task creation
# -------------------------


class SelectDefaultFileAction(flow.Action):

    _default_file = flow.Parent()
    _map          = flow.Parent(2)

    def needs_dialog(self):
        return False
    
    def allow_context(self, context):
        return False
    
    def run(self, button):
        if self._default_file.exists.get():
            return
        
        self._default_file.create.set(
            not self._default_file.create.get()
        )
        self._map.touch()


class DefaultTaskViewItem(flow.SessionObject):
    """
    Describes a default task to be created in the list of
    files of a task.
    """
    task_name    = flow.Param()
    display_name = flow.Param()
    create       = flow.BoolParam()
    exists       = flow.Computed(cached=True)
    icon         = flow.Param()

    select       = flow.Child(SelectDefaultFileAction)

    _tasks       = flow.Parent(3)

    def compute_child_value(self, child_value):
        if child_value is self.exists:
            exists = self._tasks.has_mapped_name(self.task_name.get())
            self.exists.set(exists)


class DefaultTaskView(flow.DynamicMap):
    '''
    Lists the default tasks defined in the task manager that
    can be added to a task collection.
    
    Tasks defined as not optional in the manager's default
    tasks are preselected; tasks which already exist in the
    collection appear greyed out.
    '''

    _action = flow.Parent()
    _tasks = flow.Parent(2)

    def __init__(self, parent, name):
        super(DefaultTaskView, self).__init__(parent, name)
        self._cache = None
        self._cache_names = None
        self._cache_key = None

    @classmethod
    def mapped_type(cls):
        return DefaultTaskViewItem

    def mapped_names(self, page_num=0, page_size=None):
        cache_key = (page_num, page_size)
        if (
            self._cache is None
            or self._cache_key != cache_key
        ):
            mgr = self.root().project().get_task_manager()
            default_tasks = self._tasks.get_default_tasks()

            self._cache = {}
            self._cache_names = []
            positions = {}

            for dt in default_tasks:
                task_name = dt.name()
                self._cache[task_name] = dict(
                    task_name=task_name,
                    display_name=mgr.get_task_display_name(task_name),
                    create=not dt.optional.get(),
                    icon=mgr.get_task_icon(task_name),
                )
                self._cache_names.append(task_name)
                positions[task_name] = dt.position.get()
            
            self._cache_names.sort(key=lambda n: positions[n])
            self._cache_key = cache_key
        
        return self._cache_names
    
    def columns(self):
        return ['Do create', 'Task']

    def refresh(self):
        self._cache = None
        for t in self.mapped_items():
            t.exists.touch()
        self.touch()
    
    def _configure_child(self, child):
        self.mapped_names()
        child.task_name.set(self._cache[child.name()]['task_name'])
        child.display_name.set(self._cache[child.name()]['display_name'])
        child.create.set(self._cache[child.name()]['create'])
        child.icon.set(self._cache[child.name()]['icon'])
    
    def _fill_row_cells(self, row, item):
        row['Do create'] = ''
        row['Task'] = item.display_name.get()
    
    def _fill_row_style(self, style, item, row):
        style['Do create_activate_oid'] = item.select.oid()

        if item.exists.get():
            style['Task_icon'] = item.icon.get()
            style['Do create_icon'] = ('icons.gui', 'check-box-empty-dark')
            for col in self.columns():
                style['%s_foreground-color' % col] = '#4e5255'
        else:
            style['Task_icon'] = item.icon.get()
            if item.create.get():
                style['Do create_icon'] = ('icons.gui', 'check')
            else:
                style['Do create_icon'] = ('icons.gui', 'check-box-empty')


class ManageTasksAction(flow.Action):
    """
    Allows to create tasks among the default tasks defined
    in the project's task manager.
    """

    tasks = flow.Child(DefaultTaskView)

    _map = flow.Parent()

    def get_buttons(self):
        self.tasks.refresh()
        if self.all_tasks_exist():
            return ['Close']
        
        return ['Create', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel' or button == 'Close':
            return
        
        mgr = self.root().project().get_task_manager()
        
        for dt in self.tasks.mapped_items():
            if dt.create.get() and not dt.exists.get():
                t = self._map.add(dt.name())
                t.display_name.set(dt.display_name.get())
        
        self._map.touch()
    
    def child_value_changed(self, child_value):
        if child_value is self.select_all:
            b = self.select_all.get()

            for dt in self.tasks.mapped_items():
                if not dt.exists.get():
                    dt.create.set(b)
            
            self.tasks.touch()
    
    def all_tasks_exist(self):
        return all([
            t.exists.get()
            for t in self.tasks.mapped_items()
        ])


# Task manager
# -------------------------


class TaskManager(flow.Object):
    """
    The task manager embeds an ordered list of default task
    names and a list of task templates
    """

    default_files = flow.HashParam().ui(hidden=True)
    default_tasks  = flow.Child(DefaultTasks).ui(expanded=True)
    task_templates = flow.Child(TaskTemplates).ui(expanded=True)
    template_colors = flow.OrderedStringSetParam().ui(hidden=True)

    def get_task_color(self, task_name):
        dt = self.default_tasks[task_name]
        return dt.get_color()
    
    def get_task_icon(self, task_name):
        dt = self.default_tasks[task_name]
        return dt.get_icon()
    
    def get_task_display_name(self, task_name):
        dt = self.default_tasks[task_name]
        return dt.get_display_name()
    
    def get_task_path_format(self, task_name):
        dt = self.default_tasks[task_name]
        return dt.get_path_format()
    
    def get_task_primary_file_names(self, task_name):
        dt = self.default_tasks[task_name]
        return dt.get_primary_file_names()
    
    def get_template_default_tasks(self, template_name):
        return [
            dt for dt in self.default_tasks.mapped_items()
            if dt.template.get() == template_name
        ]
    
    def get_subtasks(self, task_name):
        dt = self.default_tasks[task_name]
        return dt.subtasks.get()
    
    def is_assignation_enabled(self, task_name):
        dt = self.default_tasks[task_name]
        return dt.assignation_enabled.get()

    def get_task_files(self, task_name, enabled_only=False):
        """
        Returns a list of tuples describing the default files
        of a task with the given name.
        
        Tuples follow the layout (<file name>, <path format>).
        """
        files = []
        if self.default_tasks.has_mapped_name(task_name):
            dt = self.default_tasks[task_name]
            files = [
                (
                    df.file_name.get(),
                    df.path_format.get(),
                    df.optional.get(),
                )
                for df in dt.files.mapped_items()
                if not enabled_only or df.enabled.get()
            ]
        
        return files
