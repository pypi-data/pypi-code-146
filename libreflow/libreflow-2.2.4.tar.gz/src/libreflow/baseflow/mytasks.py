import time
import pprint
import collections
from kabaret import flow
from .users import PresetSessionValue


class TaskItem(flow.Object):

    _action            = flow.Parent(3)

    task_id            = flow.SessionParam()
    task_type          = flow.SessionParam()
    task_status        = flow.SessionParam()
    task_oid           = flow.SessionParam()
    entity_id          = flow.SessionParam()
    entity_type        = flow.SessionParam() # Asset or Shot
    entity_type_name   = flow.SessionParam() # Asset Type or Sequence name
    entity_name        = flow.SessionParam() # Asset or Shot name
    entity_description = flow.SessionParam().ui(editor='textarea')
    shot_frames        = flow.SessionParam()
    dft_task_name      = flow.SessionParam()
    primary_files      = flow.SessionParam(list)
    is_bookmarked      = flow.SessionParam().ui(editor='bool')

    def set_shot_duration(self):
        data = self._action.kitsu.gazu_api.get_shot_data(self.entity_name.get(), self.entity_type_name.get())
        return self.shot_frames.set(data['nb_frames'])

    def find_default_task(self):
        dft_tasks = self._action.task_mgr.default_tasks.mapped_items()
        for task in dft_tasks:
            if self.task_type.get() in task.kitsu_tasks.get():
                self.dft_task_name.set(task.name())

    def set_task_oid(self):
        if self.entity_type.get() == 'Shot':
            films = self.root().project().films.mapped_items()
            if films:
                film = films[0]
                if film.sequences.has_mapped_name(self.entity_type_name.get()):
                    sequence = film.sequences[self.entity_type_name.get()]
                    if sequence.shots.has_mapped_name(self.entity_name.get()):
                        shot = sequence.shots[self.entity_name.get()]
                        if shot.tasks.has_mapped_name(self.dft_task_name.get()):
                            task = shot.tasks[self.dft_task_name.get()]
                            self.task_oid.set(task.oid())
                            self.primary_files.set(task.get_primary_files())
                        else:
                            self.task_oid.set(shot.oid())
        else:
            asset_types = self.root().project().asset_types
            if asset_types.has_mapped_name(self.entity_type_name.get()):
                asset_type = asset_types[self.entity_type_name.get()]
                if asset_type.assets.has_mapped_name(self.entity_name.get()):
                    asset = asset_type.assets[self.entity_name.get()]
                    if asset.tasks.has_mapped_name(self.dft_task_name.get()):
                        task = asset.tasks[self.dft_task_name.get()]
                        self.task_oid.set(task.oid())
                        self.primary_files.set(task.get_primary_files())
                    else:
                        self.task_oid.set(asset.oid())


class MyTasksMap(flow.DynamicMap):

    _settings = flow.Parent()
    _action = flow.Parent(2)

    def __init__(self, parent, name):
        super(MyTasksMap, self).__init__(parent, name)
        self._cache = None
        self._cache_ttl = self._settings.cache_ttl.get()
        self._cache_birth = -1
        self._cache_key = None

    @classmethod
    def mapped_type(cls):
        return TaskItem

    def columns(self):
        return ['Task', 'Status', 'Type', 'Type Name', 'Name']

    def mapped_names(self, page_num=0, page_size=None):
        cache_key = (page_num, page_size)
        if (
            self._cache is None
            or time.time() - self._cache_birth > self._cache_ttl
            or self._cache_key != cache_key
        ):
            self._mng.children.clear()
            kitsu_tasks = self._action.kitsu.gazu_api.get_assign_tasks()
            if 'DONE' in self._settings.task_statues_filter.get():
                kitsu_tasks += self._action.kitsu.gazu_api.get_done_tasks()

            self._cache = {}

            for i, item in enumerate(kitsu_tasks):
                data = {}
                # Filter
                if item['task_status_short_name'].upper() not in self._settings.task_statues_filter.get():
                    continue
                if 'task_type_for_entity' in item:
                    if item['task_type_for_entity'] == "Asset":
                        if item['entity_type_name'] == 'x':
                            continue
                        if item['task_type_name'] == 'FDT':
                            continue

                        data.update(dict(
                            task_id=item['id'], 
                            task_type=item['task_type_name'],
                            task_status=item['task_status_short_name'],
                            entity_id=item['entity_id'],
                            entity_type=item['task_type_for_entity'],
                            entity_type_name=item['entity_type_name'],
                            entity_name=item['entity_name'],
                            entity_description=item['entity_description'],
                            updated_date=item['updated_at']
                        ))
                    else:
                        data.update(dict(
                            task_id=item['id'], 
                            task_type=item['task_type_name'],
                            task_status=item['task_status_short_name'],
                            entity_id=item['entity_id'],
                            entity_type=item['entity_type_name'],
                            entity_type_name=item['sequence_name'],
                            entity_name=item['entity_name'],
                            entity_description=item['entity_description'],
                            updated_date=item['updated_at']
                        ))
                else:
                    data.update(dict(
                        task_id=item['id'], 
                        task_type=item['task_type_name'],
                        task_status=item['task_status_short_name'],
                        entity_type=item['entity_type_name'],
                        entity_type_name=item['sequence_name'],
                        entity_name=item['entity_name'],
                        entity_description=item['entity_description'],
                        updated_date=item['updated_at']
                    ))
                self._cache['task'+str(i)] = data

            bookmarks = self.root().project().get_user().bookmarks.mapped_items()

            for b in bookmarks:
                data = {}

                oid = b.goto_oid.get()
                oid_splited = self.root().session().cmds.Flow.split_oid(oid, True, self.root().project().oid())
                if '/films' in oid:
                    sequence_name = oid_splited[1][0].split(':')[1]
                    shot_name = oid_splited[2][0].split(':')[1]
                    task_name = oid_splited[3][0].split(':')[1]

                    entity = self._action.kitsu.gazu_api.get_shot_data(shot_name, sequence_name)

                if '/asset_types' in oid:
                    asset_name = oid_splited[1][0].split(':')[1]
                    task_name = oid_splited[2][0].split(':')[1]

                    entity = self._action.kitsu.gazu_api.get_asset_data(asset_name)

                kitsu_task_name = self._action.task_mgr.default_tasks[task_name].kitsu_tasks.get()[0]
                task_data = self._action.kitsu.gazu_api.get_task(entity, kitsu_task_name)

                key_exist = [key for key,data in self._cache.items() if data['task_id'] == task_data['id']]
                if key_exist:
                    key = key_exist[0]
                    self._cache[key]['task_oid'] = oid
                    self._cache[key]['dft_task_name'] = task_name
                    self._cache[key]['is_bookmarked'] = True
                    continue

                if task_data['task_type']['for_entity'] == "Asset":
                    data.update(dict(
                        task_id=task_data['id'], 
                        task_type=task_data['task_type']['name'],
                        task_status=task_data['task_status']['short_name'],
                        task_oid=oid,
                        entity_id=task_data['entity_id'],
                        entity_type=task_data['task_type']['for_entity'],
                        entity_type_name=task_data['entity_type']['name'],
                        entity_name=task_data['entity']['name'],
                        entity_description=task_data['entity']['description'],
                        updated_date=task_data['updated_at'],
                        dft_task_name=task_name,
                        is_bookmarked=True
                    ))
                else:
                    data.update(dict(
                        task_id=task_data['id'], 
                        task_type=task_data['task_type']['name'],
                        task_status=task_data['task_status']['short_name'],
                        task_oid=oid,
                        entity_id=task_data['entity_id'],
                        entity_type=task_data['entity_type']['name'],
                        entity_type_name=task_data['sequence']['name'],
                        entity_name=task_data['entity']['name'],
                        entity_description=task_data['entity']['description'],
                        updated_date=task_data['updated_at'],
                        dft_task_name=task_name,
                        is_bookmarked=True
                    ))
                i = i + 1
                self._cache['task'+str(i)] = data

            # Sorting
            if self._settings.task_sorted.get() == 'Entity name':
                self._cache = collections.OrderedDict(sorted(
                    self._cache.items(),
                    key=lambda data: (data[1]['entity_type_name'], data[1]['entity_name']
                )))
            elif self._settings.task_sorted.get() == 'Status':
                self._cache = collections.OrderedDict(sorted(
                    self._cache.items(),
                    key=lambda data: data[1]['task_status']
                ))
            elif self._settings.task_sorted.get() == 'Latest update':
                self._cache = collections.OrderedDict(sorted(
                    self._cache.items(),
                    key=lambda data: data[1]['updated_date'],
                    reverse=True
                ))
           
            self._cache_key = cache_key
            self._cache_birth = time.time()

        return self._cache.keys()
    
    def touch(self):
        self._cache = None
        super(MyTasksMap, self).touch()

    def _configure_child(self, child):
        child.task_id.set(self._cache[child.name()]['task_id'])
        child.task_type.set(self._cache[child.name()]['task_type'])
        child.task_status.set(self._cache[child.name()]['task_status'])
        child.entity_id.set(self._cache[child.name()]['entity_id'])
        child.entity_type.set(self._cache[child.name()]['entity_type'])
        child.entity_type_name.set(self._cache[child.name()]['entity_type_name'])
        child.entity_name.set(self._cache[child.name()]['entity_name'])
        child.entity_description.set(self._cache[child.name()]['entity_description'])

        if 'is_bookmarked' in self._cache[child.name()]:
            child.task_oid.set(self._cache[child.name()]['task_oid'])
            child.dft_task_name.set(self._cache[child.name()]['dft_task_name'])
            child.is_bookmarked.set(self._cache[child.name()]['is_bookmarked'])
            child.primary_files.set(self.root().session().cmds.Flow.call(
                self._cache[child.name()]['task_oid'], 'get_primary_files', {}, {}
            ))
        else:
            child.find_default_task()
            child.set_task_oid()

        if self._cache[child.name()]['entity_type'] == 'Shot':
            child.set_shot_duration()

    def _fill_row_cells(self, row, item):
        row["Task"] = item.task_type.get()
        row["Status"] = item.task_status.get()
        row["Type"] = item.entity_type.get()
        row["Type Name"] = item.entity_type_name.get()
        row["Name"] = item.entity_name.get()


class MyTasksSettings(flow.Object):

    tasks               = flow.Child(MyTasksMap)
    task_statues_filter = flow.SessionParam([], PresetSessionValue)
    task_sorted         = flow.SessionParam(None, PresetSessionValue)
    cache_ttl           = flow.Param(120)

    def check_default_values(self):
        self.task_statues_filter.apply_preset()
        self.task_sorted.apply_preset()

    def update_presets(self):
        self.task_statues_filter.update_preset()
        self.task_sorted.update_preset()


class MyTasks(flow.Object):

    settings = flow.Child(MyTasksSettings)

    def __init__(self, parent, name):
        super(MyTasks, self).__init__(parent, name)
        self.kitsu = self.root().project().admin.kitsu
        self.task_mgr = self.root().project().get_task_manager()
        self.settings.check_default_values()

    def get_tasks(self, force_update=False):
        if force_update:
            self.settings.tasks.touch()
        return self.settings.tasks.mapped_items()

    def get_task_statutes(self, short_name):
        return self.kitsu.gazu_api.get_task_statutes(short_name)

    def get_task_status(self, short_name):
        return self.kitsu.gazu_api.get_task_status(short_name=short_name)

    def get_task_comments(self, task_id):
        return self.kitsu.gazu_api.get_all_comments_for_task(task_id)

    def get_server_url(self):
        url = self.kitsu.gazu_api.get_server_url()
        if url.endswith('/'):
            url = url[:-1]
        return url
    
    def get_project_id(self):
        return self.kitsu.gazu_api.get_project_id()

    def get_project_oid(self):
        return self.root().project().oid()

    def get_project_fps(self):
        return self.kitsu.gazu_api.get_project_fps()

    def is_uploadable(self, file_name):
        return self.kitsu.is_uploadable(file_name)

    def set_task_status(self, task_id, task_status_name, comment, files):
        return self.kitsu.gazu_api.set_task_status(task_id, task_status_name, comment, files)

    def upload_preview(self, entity_id, task_name, task_status_name, file_path, comment):
        return self.kitsu.gazu_api.upload_preview(entity_id, task_name, task_status_name, file_path, comment)

    def toggle_bookmark(self, oid):
        bookmarks = self.root().project().get_user().bookmarks

        if bookmarks.has_bookmark(oid):
            self.root().session().log_debug("Remove %s to bookmarks" % oid)
            bookmarks.remove_bookmark(oid)
            return False
        else:
            self.root().session().log_debug("Add %s to bookmarks" % oid)
            bookmarks.add_bookmark(oid)
            return True

    def _fill_ui(self, ui):
        ui["custom_page"] = "libreflow.baseflow.ui.mytasks.MyTasksPageWidget"
