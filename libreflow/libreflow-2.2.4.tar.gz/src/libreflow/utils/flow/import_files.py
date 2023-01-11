import os
import shutil
import re
import pprint

from kabaret import flow


class FileItem(flow.Object):

    file_name          = flow.SessionParam()
    file_preset_name   = flow.SessionParam()
    file_format        = flow.SessionParam()
    file_path          = flow.SessionParam()
    file_target        = flow.SessionParam()
    file_target_format = flow.SessionParam()
    file_status        = flow.SessionParam()
    file_comment       = flow.SessionParam()
    rev_version        = flow.SessionParam()
    task_name          = flow.SessionParam()

    _action            = flow.Parent(3)

    def get_files_choices(self):
        choices = []
        for dft_file in self._action.task_mgr.default_tasks[self.task_name.get()].files.edits.mapped_items():
            if self.file_format.get():
                if not '.' in dft_file.file_name.get():
                    continue
                else:
                    name, ext = dft_file.file_name.get().split('.')
                    if ext == self.file_format.get():
                        choices.append(dft_file.file_name.get())
            else:
                if '.' in dft_file.file_name.get():
                    continue
                else:
                    choices.append(dft_file.file_name.get())
        return choices

    def check_revision(self, task=None):
        if task is None:
            if self.task_name.get() != '':
                task = self.root().get_object(self.file_target.get())
            else:
                return

        f = None
        rev = None
        
        if self.file_format.get():
            preset_name, ext = os.path.splitext(self.file_preset_name.get())
            if task.files.has_file(preset_name, self.file_format.get()):
                f = task.files[preset_name+'_'+self.file_format.get()]
                rev = f.get_head_revision()
        else:
            if task.files.has_folder(self.file_preset_name.get()):
                f = task.files[self.file_preset_name.get()]
                rev = f.get_head_revision()

        if f is None:
            self.rev_version.set('v001')
            return self.file_status.set('NEW')
        else:
            if rev:
                ver = int(rev.name().replace('v', ''))
                ver = 'v' + f'{(ver + 1):03}'
                self.rev_version.set(ver)
            else:
                self.rev_version.set('v001')
        return self.file_status.set('OK')
        

class FilesMap(flow.Map):

    @classmethod
    def mapped_type(cls):
        return FileItem

    def columns(self):
        return ["Name", "Target", "Revision"]

    def _configure_child(self, child):
        child.file_target.set('')
        child.file_comment.set('')
        child.task_name.set('')

    def _fill_row_cells(self, row, item):
        row["Name"] = item.file_name.get()
        row["Target"] = item.file_target.get()
        row["Revision"] = item.rev_version.get()


class ImportFilesSettings(flow.Object):

    files_map = flow.Child(FilesMap)
    upload_revision = flow.BoolParam()


class ImportFilesAction(flow.Action):

    ICON = ('icons.gui', 'file')

    paths = flow.SessionParam([]).ui(hidden=True)
    settings = flow.Child(ImportFilesSettings)

    def __init__(self, parent, name):
        super(ImportFilesAction, self).__init__(parent, name)
        self.kitsu = self.root().project().admin.kitsu
        self.task_mgr = self.root().project().get_task_manager()
        self.settings.files_map.clear()

    def check_files(self, paths):
        for path in paths:
            file_name = os.path.split(path)[1]
            file_match = file_name
            print(file_name)
            preset = None
            target_oid = None
            task_entity = None
            for dft_file, task_names in self.task_mgr.default_files.get():
                if dft_file in file_name:
                    preset = dft_file
                    file_match = file_match.replace(preset, '')
                    if file_match.endswith('_'):
                        file_match = file_match[:-1]
                    print(preset)
                    break
            if preset:
                for dft_task_name in task_names:
                    entity_type = self.task_mgr.default_tasks[dft_task_name].template.get()
                    base_entity = False

                    if entity_type == 'shot':
                        films_names = sorted(self.root().project().films.mapped_names(), reverse=True)
                        film = None
                        for f in films_names:
                            if file_match.startswith(f):
                                print(f)
                                film = self.root().project().films[f]
                                file_match = file_match.replace(f+'_', '')
                                target_oid = film.oid()
                                base_entity = True
                                break
                        
                        if not film:
                            film = self.root().project().films[films_names[-1]]
                            print(film.name())
                            target_oid = film.oid()

                        sequences = sorted(self.kitsu.gazu_api.get_sequences_data(), key=lambda s: s['name'], reverse=True)
                        seq = next((seq for seq in sequences if file_match.startswith(seq['name'])), None)
                        if seq:
                            seq_name = seq['name']
                            print(seq_name)
                            file_match = file_match.replace(seq_name+'_', '')
                            shots = sorted(self.kitsu.gazu_api.get_shots_data(seq), key=lambda s: s['name'], reverse=True)
                            shot = next((shot for shot in shots if file_match.startswith(shot['name'])), None)
                            if shot:
                                shot_name = shot['name']
                                print(shot_name)
                        
                            if film.sequences.has_mapped_name(seq_name):
                                sequence = film.sequences[seq_name]
                                target_oid = sequence.oid()
                                if shot:
                                    if sequence.shots.has_mapped_name(shot_name):
                                        sh = sequence.shots[shot_name]
                                        target_oid = sh.oid()
                                        if sh.tasks.has_mapped_name(dft_task_name):
                                            task_entity = sh.tasks[dft_task_name]
                                            target_oid = task_entity.oid()
                                            break

                    if entity_type == 'asset':
                        assets = sorted(self.kitsu.gazu_api.get_assets_data(), key=lambda a: a['name'], reverse=True)
                        asset = next((asset for asset in assets if file_match.endswith(asset['name'])), None)
                        if asset:
                            asset_name = asset['name']
                            print(asset_name)
                            asset_type_name = self.kitsu.gazu_api.get_entity_type_data(asset['entity_type_id'])['name']
                            print(asset_type_name)
                        
                            if self.root().project().asset_types.has_mapped_name(asset_type_name):
                                asset_type = self.root().project().asset_types[asset_type_name]
                                target_oid = asset_type.oid()
                                base_entity = True
                                if asset_type.assets.has_mapped_name(asset_name):
                                    a = asset_type.assets[asset_name]
                                    target_oid = a.oid()
                                    if a.tasks.has_mapped_name(dft_task_name):
                                        task_entity = a.tasks[dft_task_name]
                                        target_oid = task_entity.oid()
                                        break

                    if base_entity:
                        break

            f = self.settings.files_map.add(file_name.replace('.', '_'))
            f.file_name.set(file_name)
            if preset:
                f.file_preset_name.set(preset)
            if os.path.isfile(path):
                f.file_format.set(file_name.split('.')[-1])
            f.file_path.set(path)
            f.file_target.set(target_oid)
            if target_oid is None:
                f.file_status.set('Unknown')
            elif target_oid and task_entity is None:
                f.file_status.set('Warning')
            if task_entity:
                dft_task_file = self.task_mgr.default_tasks[task_entity.name()].files[preset.replace('.', '_')]
                f.file_target_format.set(dft_task_file.path_format.get())
                f.task_name.set(task_entity.name())
                f.check_revision(task_entity)

    def check_new_target(self, target):
        if 'tasks/' in target:
            oid, task_name = target.split('/tasks/')
            try:
                entity = self.root().get_object(oid)
                for task in entity.tasks.mapped_names():
                    if task == task_name:
                        return task_name
            except flow.exceptions.MappedNameError:
                return None
        return None

    def import_files(self, files):
        for f in files:
            print('ImportFiles :: {file} - Import started'.format(file=f.file_name.get()))

            target = self.root().get_object(f.file_target.get())

            if f.file_status.get() == 'OK':
                file_entity = target.files[f.file_preset_name.get().replace('.', '_')]
            else:
                if f.file_format.get():
                    file_entity = target.files.add_file(
                        f.file_preset_name.get().split('.')[0],
                        f.file_format.get(),
                        tracked=True,
                        default_path_format=f.file_target_format.get()
                    )
                    print('ImportFiles :: File created')
                else:
                    file_entity = target.files.add_folder(
                        f.file_preset_name.get(),
                        tracked=True,
                        default_path_format=f.file_target_format.get()
                    )
                    print('ImportFiles :: Folder created')
    
            r = self._create_revision(file_entity)
            revision_path = r.get_path()
            revision_name = r.name()

            if f.file_comment.get() != '':
                r.comment.set(f.file_comment.get())
            
            if f.file_format.get():
                shutil.copy2(f.file_path.get(), revision_path)
            else:
                shutil.copytree(f.file_path.get(), revision_path)
            
            print('ImportFiles :: Revision created')

            if self.settings.upload_revision.get() == True:
                self._upload_revision(r)

            self.settings.files_map.remove(f.name())
        
        print('ImportFiles :: Import complete!')

    def _create_revision(self, f):
        r = f.add_revision()
        revision_path = r.get_path()
        f.last_revision_oid.set(r.oid())
        os.makedirs(os.path.dirname(revision_path), exist_ok=True)

        return r

    def _upload_revision(self, revision):
        current_site = self.root().project().get_current_site()
        job = current_site.get_queue().submit_job(
            job_type='Upload',
            init_status='WAITING',
            emitter_oid=revision.oid(),
            user=self.root().project().get_user_name(),
            studio=current_site.name(),
        )

        self.root().project().get_sync_manager().process(job)

    def _fill_ui(self, ui):
        ui['custom_page'] = 'libreflow.baseflow.ui.importfiles.ImportFilesWidget'
