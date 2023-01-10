import os
from ml_metadata.proto import Artifact
from mlmd.dataset_manager_scheme import ArtifactType, ExecutionType, ContextType
from mlmd.dataset_manager_dao import *
from dataset_management.utils import generate_version_id
from dataset_management.blob import _upload_blob, get_bucket_name, list_blob, _download_blob
import datetime
from multiprocessing import Array, cpu_count, Pool
from mlmd.metadata_dao import get_all_tenants, get_annotation_stats, get_image_metadata, get_model_info_by_dataset, get_tenant_id, get_training_history, insert_image_log_bulk, insert_image_metadata_bulk, get_image_executions_by_version, get_all_tenants
from .triggers import ApiTrigger
from mlmd.gservice_dao import get_user_info

class Dataset():
    def __init__(self, datasetname, version="latest") -> None:        
        self.username = get_user_info()["email"]
        dataset = get_artifact_by_type_and_name(ArtifactType.DATASET, datasetname)
        if dataset is None:
            raise Exception("Dataset {} not found".format(datasetname))
        self.metadata = dataset.properties
        self.datasetname = dataset.name
        self.created_at = datetime.datetime.fromtimestamp(dataset.create_time_since_epoch//1000.0)
        self.id = dataset.id
        self.version = version
        if self.version == "latest":
            self.version = self.metadata["latest_version"].string_value
        self.uncommitted_version = self.metadata["uncommitted_version"].string_value
        self.filelist = None
        self.global_annotations = None
        self.global_changelist = None

    def __str__(self) -> str:
        return str({
            "name": self.datasetname,
            "version": self.version,
            "tags": self.metadata["tags"].string_value,
            "created_by": self.metadata["created_by"].string_value,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def get_gcs_path(self):
        return "gs://{}".format(get_bucket_name(self.datasetname))

    def list_staged_executions(self):
        tobe_committed_ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)
        return [{
            "execution": get_type_name_from_id(exe.type_id),
            "file_location": exe.properties["file_location"].string_value,
            "tenant": exe.properties["tenant"].string_value,
            "annotation": exe.properties["annotation"].string_value,
            "executed_by": exe.properties["executed_by"].string_value,
            "executed_at": datetime.datetime.fromtimestamp(exe.create_time_since_epoch//1000.0).strftime("%Y-%m-%d %H:%M:%S")
        } for exe in get_executions_by_context(tobe_committed_ctx.id)]


    def list_versions(self, short=False):
        if short:
            return [ctx.name for ctx in get_contexts_by_artifact(ContextType.COMMIT_DATASET_VERSION, self.id) if ctx.properties["committed_by"].string_value != ""]            
        return [
            {"version": ctx.name,
             "committed_by": ctx.properties["committed_by"].string_value,
             "commit_message": ctx.properties["commit_message"].string_value,
             "prev_version": ctx.properties["prev_ref"].string_value,
             "created_at": datetime.datetime.fromtimestamp(ctx.create_time_since_epoch//1000.0).strftime("%Y-%m-%d %H:%M:%S")
            } for ctx in get_contexts_by_artifact(ContextType.COMMIT_DATASET_VERSION, self.id) if ctx.properties["committed_by"].string_value != ""]

    def add_files_from_generator(self, generator, override=False):
        blobnamelist = {blob.name for blob in list_blob(get_bucket_name(self.datasetname))}
        arglist = []
        metadata_list = []
        tenants = get_all_tenants()
        for filepath, filename, annotation, tenant, metadata in generator():
            metadata_list.append((filename, tenants[tenant], self.id, annotation, metadata))
            if override == False:
                if filename in blobnamelist:
                    continue
            arglist.append((filename, self.datasetname, filepath, {"annotation": annotation, "tenant": tenant}))
        if self.__upload_files(arglist) is None:
            print("Override option is being set to {}".format(override))
        exe_id = create_execution(ExecutionType.ADD_FILES_TO_DATASET, {
                "executed_by": self.username,
            })
        return self.__create_image_metadata(exe_id, metadata_list)

    def update_metadata_from_generator(self, generator):
        metadata_list = []
        for filename, metadata in generator():
            metadata_list.append((metadata, self.id, filename))
        create_execution(ExecutionType.UPDATE_METADATA_DATASET, {
                "executed_by": self.username,
            })
        from mlmd.metadata_dao import update_image_metadata_bulk
        return update_image_metadata_bulk(metadata_list)
    
    def update_annotation_from_generator(self, generator):
        data_arr = []
        for filename, annotation in generator():
            data_arr.append((annotation, self.id, filename))
        create_execution(ExecutionType.UPDATE_ANNOTATION_DATASET, {
                "executed_by": self.username,
            })
        from mlmd.metadata_dao import update_image_annotation_bulk
        return update_image_annotation_bulk(data_arr)

    def add_files_from_dir(self, _dir, override=False, annotation=None, tenant="unknown"):
        if _dir is None or os.path.isdir(_dir) == False:
            raise Exception("Data dir {} not valid".format(_dir))

        tenant_id = get_tenant_id(tenant)
        if tenant_id is None:
            raise Exception("Tenant {} is invalid".format(tenant))

        blobnamelist = {blob.name for blob in list_blob(get_bucket_name(self.datasetname))}
        metadata_list = []
        arglist = [] 
        for f in os.listdir(_dir):
            if not os.path.isfile(os.path.join(_dir, f)):
                continue
            metadata_list.append((f, tenant_id, self.id, annotation, None))
            if override == True or (override == False and f not in blobnamelist):
                arglist.append((f, self.datasetname, _dir, {"annotation": annotation, "tenant": tenant}))
        
        if self.__upload_files(arglist) is None:
            print("Override option is being set to {}".format(override))
        exe_id = create_execution(ExecutionType.ADD_FILES_TO_DATASET, {
            "executed_by": self.username,
            "file_location": os.uname()[1] + ":" + os.path.abspath(_dir),
            "tenant": tenant,
            "annotation": annotation})        
        return self.__create_image_metadata(exe_id, metadata_list)
    
    def __upload_files(self, arglist):
        if len(arglist) <= 0:
            print("No file to upload")
            return None
        proc_count = cpu_count()
        if len(arglist) < cpu_count():
            proc_count = len(arglist)
        print("{} is being uploaded by {} processes...".format(len(arglist), proc_count))
        p = Pool(proc_count)
        r = p.map(_upload_blob, arglist)
        p.close()
        p.join()
        success_list = []
        for i,_ in enumerate(r):
            if r[i] == False:
                print("Failed to update {} in changelist".format(self.changelist[i][0]))
            else:
                success_list.append(r[i])
        print("Successfully uploaded {} files".format(len(success_list)))
        return True

    def __create_image_metadata(self, exe_id, metadata_list):
        print("Creating image metadata...")
        if exe_id is None:
            print("No execution failed to be created (image metadata and image log not inserted)")
            return 
        #insert image metadata
        if len(metadata_list) > 0:
            image_metadata_ids = insert_image_metadata_bulk(metadata_list, return_ids=True)
            # execution and image artifacts link
            log_metadata = [(image_id, exe_id, self.uncommitted_version, self.id) for image_id in image_metadata_ids]
            if len(log_metadata) > 0:
                insert_image_log_bulk(log_metadata)

        # version and execution link
        ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)
        create_association_attribution(ctx.id, exe_id, None)
        print("Execution [{}] created".format(exe_id))
        return True

    def remove_files(self, filelist):
        if filelist is None or len(filelist) <= 0:
            return None
        exe_id = create_execution(ExecutionType.REMOVE_FILES_FROM_DATASET, {"executed_by": self.username})
        #insert image metadata
        image_names = [(image_name,) for image_name in filelist]
        image_metadata = get_image_metadata(image_names, self.id)
        image_metadata_ids = [item[0] for item in image_metadata]
        if len(image_metadata) > 0:
            log_metadata = [(image_id, exe_id, self.uncommitted_version, self.id) for image_id in image_metadata_ids]
            if len(log_metadata) > 0:
                insert_image_log_bulk(log_metadata)

        ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)
        return create_association_attribution(ctx.id, exe_id, None)

    def commit_version(self, commit_message="", trigger=None, ref_version=None):
        # update uncommited version to become official version
        tobe_committed_ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)

        if len(get_executions_by_context(tobe_committed_ctx.id)) <= 0:
            print("Nothing to commit")
            return False

        tobe_committed_ctx.properties["committed_by"].string_value = self.username
        tobe_committed_ctx.properties["prev_ref"].string_value = self.version if ref_version is None else ref_version
        tobe_committed_ctx.properties["commit_message"].string_value = commit_message
        update_context(tobe_committed_ctx)
        committed_version_id = tobe_committed_ctx.name
        # new uncommited version ref to committed version and its link
        new_uncommitted_version_id = generate_version_id()
        context_id = create_context(ContextType.COMMIT_DATASET_VERSION, new_uncommitted_version_id, None, self.version)
        create_association_attribution(context_id, None, self.id)

        update_artifact(ArtifactType.DATASET, self.datasetname, None, committed_version_id, new_uncommitted_version_id)
        self.uncommitted_version = new_uncommitted_version_id
        self.version = committed_version_id
        self.filelist = self.get_filelist()
        return committed_version_id

    # def get_trigger(self):
    #     return ApiTrigger.from_json_string(self.metadata.get("trigger"))

    # def set_trigger(self, trigger: ApiTrigger):
    #     self.metadata["trigger"].string_value = str(trigger)
    #     self.trigger = trigger
    #     return update_artifact(ArtifactType.DATASET, self.datasetname, None, None, None, self.metadata["trigger"].string_value)

    def trigger_retrain(self, models=None):
        from mlmd.gservice_dao import get_secret
        config = get_secret("RETRAIN_CONFIG")        
        if config["retrain_url"] is None:
            print("retrain_url configuration not found in secret RETRAIN_CONFIG")
            return
        import google.auth
        cred, project = google.auth.default()
        data = {
            "dataset":self.datasetname,
            "version":self.version,
            "refresh_token": cred.refresh_token,
            "token_uri": cred.token_uri,
            "client_id": cred.client_id,
            "client_secret": cred.client_secret,
            "scopes": cred.scopes
        }
        if models is not None and isinstance(models, list):
            data["models"] = models
        t = ApiTrigger("POST", config["retrain_url"], data)
        return t.execute()

    def get_tags(self):
        return self.metadata["tags"].string_value

    def add_tag(self, tag):
        tag_str = self.metadata["tags"].string_value
        if tag_str is None or tag_str == '':
            tag_arr = [tag]
        else:
            tag_arr = tag_str.split(",")
            if tag not in tag_arr:
                tag_arr.append(tag)
            else:
                print("Tag existed")
                return False
        tag_str = ",".join(tag_arr)
        self.metadata["tags"].string_value = tag_str
        return update_artifact(ArtifactType.DATASET, self.datasetname, None, None, None, None, tag_str)

    def set_tags(self, tags: Array):
        tags_str = ",".join(tags)
        self.metadata["tags"].string_value = tags_str
        return update_artifact(ArtifactType.DATASET, self.datasetname, None, None, None, None, tags_str)

    def get_connected_models(self):
        return get_model_info_by_dataset(self.datasetname)

    def __collect_changelist(self, version, global_changelist, global_annotations, metadata_filter=None):
        ctx = get_context(ContextType.COMMIT_DATASET_VERSION, version)
        if ctx is None:
            raise Exception("Version {} not exists in this dataset".format(self.version))

        image_log_arr = get_image_executions_by_version(version, metadata_filter)
        for item in image_log_arr:
            global_annotations.add(item.get("annotation"))
            if global_changelist.get(item.get("image_name")) is None:
                global_changelist[item.get("image_name")] = {"changes":[item.get("execution_id")], "annotation": item.get("annotation"), "metadata": item.get("metadata")}
            else:
                global_changelist[item.get("image_name")]["changes"].append(item.get("execution_id"))

        prev_version = ctx.properties["prev_ref"].string_value
        if prev_version is not None and prev_version != '':
            return self.__collect_changelist(prev_version, global_changelist, global_annotations, metadata_filter)
        return global_changelist, global_annotations

    def get_filelist(self, metadata_filter=None, get_annotation=False, file_path=None, get_metadata=False):
        if self.version is None or self.version == "":
            return None
        addtype = get_execution_type_by_name(ExecutionType.ADD_FILES_TO_DATASET)
        if self.global_changelist is None or self.global_annotations is None or metadata_filter is not None:
            self.global_changelist, self.global_annotations = self.__collect_changelist(self.version, {}, set(),metadata_filter)        

        if file_path == "cloud":
            gcs_path = self.get_gcs_path()
        elif file_path is not None:
            if not os.path.isdir(file_path):
                raise Exception("Local download dir {} not found".format(file_path))
            gcs_path = file_path        

        # annotation_dict = dict(map(lambda t: (t[1], t[0]), enumerate(sorted(self.global_annotations))))

        for key,value in self.global_changelist.items():            
            ret_key = "{}/{}".format(gcs_path, key) if file_path is not None else key            
            if value["changes"][0] == addtype.id:
                if get_annotation or get_metadata:
                    if get_metadata:
                        yield ret_key, value["annotation"], value["metadata"]
                    else:
                        yield ret_key, value["annotation"]
                else:
                    yield ret_key
        

    def get_current_version(self):
        return self.version

    def checkout(self, version, metadata_filter=None):
        if version == "latest":
            version = self.metadata["latest_version"].string_value
        if version not in self.list_versions(short=True):
            raise Exception("Version is not valid")
        self.version = version
        self.global_changelist, self.global_annotations = self.__collect_changelist(self.version, {}, set(),metadata_filter)

    def download_to_dir(self, _dir, overriding=False, verbose=0):
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if self.filelist is None:
            self.filelist = self.get_filelist()

        existing_files = os.listdir(_dir)
        arglist = []
        total_file_count = 0
        skip_count = 0
        for _f in self.filelist:
            if not overriding and _f in existing_files:
                skip_count += 1
                if verbose == 1:
                    print("Skipping existing file {}".format(_f))
            else:
                arglist.append((_f, self.datasetname, _dir))
            total_file_count += 1
        
        print("Skipped {} file".format(skip_count))
        if len(arglist) < 1:
            print("Nothing to download")
            return False
        proc_count = cpu_count()
        if len(arglist) < cpu_count():
            proc_count = len(arglist)
        print("Downloading {} files by {} processes...".format(total_file_count, proc_count))
        p = Pool(proc_count)
        r = p.map(_download_blob, arglist)
        p.close()
        p.join()
        success_list = []
        for i,_ in enumerate(r):
            if r[i] == False:
                print("Failed to download {}".format(self.changelist[i][0]))
            else:
                success_list.append(r[i])
        print("{}/{} files downloaded".format(len(success_list), total_file_count))

    def get_annotation_stats(self):
        """
        Return all annotations of the images of the current version

        """
        return get_annotation_stats(self.id)

    def get_training_history(self):
        return get_training_history(self.datasetname)
