from dataset_management.blob import get_bucket_name
from mlmd.dataset_manager_dao import create_artifact, create_context, get_artifact_by_type_and_name, get_artifacts_by_type, create_association_attribution
from mlmd.dataset_manager_scheme import ContextType, ArtifactType
from dataset_management.dataset import Dataset
from dataset_management.utils import generate_version_id
from google.cloud import storage
from multiprocessing import cpu_count, Pool
from dataset_manager.utils.image_util import inner_download_blob, check_authentication, get_endpoint_folder, create_folder, create_key_doc_id_gen, create_sas_doc_id_gen, create_dir_gen, inner_remove_exif_file
from itertools import repeat
import datetime
import csv
import os

def _is_tag_hit(requested_tags, tags):
    if requested_tags is None or requested_tags == '':
        return True
    if tags is None or tags == '':
        return False
    for tag in requested_tags:
        if tag in tags:
            return True
    return False

def list_datasets(tags=None):
    return [{
        "name": dataset.name,
        "created_at": datetime.datetime.fromtimestamp(dataset.create_time_since_epoch//1000.0).strftime("%Y-%m-%d %H:%M:%S"),
        "created_by": dataset.properties["created_by"].string_value,
        "latest_version": dataset.properties["latest_version"].string_value,
        "tags": dataset.properties["tags"].string_value,
        } for dataset in get_artifacts_by_type(ArtifactType.DATASET) if _is_tag_hit(tags, dataset.properties["tags"].string_value.split(","))]

def get_dataset(name, version="latest"):
    ds = Dataset(name, version)
    return ds

def create_dataset(name, get_if_exists=False):
    #login verifying
    from mlmd.gservice_dao import get_user_info
    username = get_user_info()["email"]

    #create artifact
    dataset = get_artifact_by_type_and_name(ArtifactType.DATASET, name)
    if dataset is not None:
        if get_if_exists:
            return get_dataset(name)
        else:
            raise Exception("Dataset {} existed".format(name))    

    # bucket link
    storage_client = storage.Client()
    bucket = storage_client.bucket(get_bucket_name(name))
    if bucket.exists():
        print("WARNING: Bucket {} existed".format(name))
    else:
        bucket.storage_class = "STANDARD"
        storage_client.create_bucket(bucket, location="eu")

    # mlmd
    uncommitted_version_id = generate_version_id()
    context_id = create_context(ContextType.COMMIT_DATASET_VERSION, uncommitted_version_id, None, None)
    artifact_id = create_artifact(ArtifactType.DATASET, {"name": name, "created_by": username, "uncommitted_version": uncommitted_version_id})
    create_association_attribution(context_id, None, artifact_id)

    return Dataset(name)

def delete_dataset(name):
    print("Not yet implemeted")
    pass

def download_blob(doc_id_file=None, doc_id_gen=None, authentication=None,  output_path="./"):
    """
    Note: if filename has extension, must include
    Args:
        doc_id_file (string): [description]. Defaults to None. sample.csv: doc_id_1, doc_id_2
        doc_id_gen (generator of filename). Defaults to None. sample_gen = (["doc_id_1"], ["doc_id_n"])
        authentication (dict). authentication = {"fields": key_authentication or sas_authenticaiton, "type":"key" or "sas"}
        key_authentication = {"connection_string":None, "container_name":None}.
        sas_authentication = {"account_url":None,"credential":None,"container_name":None,"input_path":None}
        output_path (str, optional). Defaults to "./".

    Returns:
        Int: The numbers of doc_id being downloaded
    """
    close_flag = False
    if not doc_id_file and not doc_id_gen:
        print("Empty doc_id_file and doc_id_gen")
        return 0
    if not authentication:
        print("Empty authentication")
        return 0
    if doc_id_file and not doc_id_gen:
        close_flag = True
        if os.path.exists(doc_id_file):
            docfile = open(doc_id_file,"r")
            doc_id_gen = csv.reader(docfile)
        else:
            print("Invalid doc_id_file {}".format(doc_id_file))
            return 0

    cc = cpu_count()
    print("Init {} processes".format(cc))
    p = Pool(cc)
    result = p.starmap(inner_download_blob, zip(doc_id_gen, repeat(authentication), repeat(output_path)))
    p.close()
    p.join()
    
    if close_flag:
        docfile.close()
    
    return sum(result)


def download_folder(folder_file=None, folder_gen=None, authentication=None,  output_path="./"):
    """

    Args:
        folder_file ([type], optional): sample.csv: path/to/folder_1, path/to/folder_2
        folder_gen ([type], optional): sample_gen=(["path/to/folder_1"], ["path/to/folder_2"])
        authentication (dict). authentication = {"fields": key_authentication or sas_authenticaiton, "type":"key" or "sas"}
        key_authentication = {"connection_string":None, "container_name":None}.
        sas_authentication = {"account_url":None,"credential":None,"container_name":None,"input_path":None}
        output_path (str, optional): Defaults to "./".

    Returns:
        Int: The numbers of doc_id being downloaded
    """ 
    close_flag = False
    result = []
    if not folder_file and not folder_gen:
        print("Empty folder_file and folder_gen")
        return 0
    if not authentication:
        print("Empty authentication")
        return 0
    if folder_file and not folder_gen:
        close_flag = True        
        if os.path.exists(folder_file):
            folderfile = open(folder_file,"r")
            folder_gen = csv.reader(folderfile)
        else:
            print("Invalid folder_file {}".format(folder_file))
            return 0
        
    authentication_field_check = check_authentication(authentication)
    if not authentication_field_check:
        print("Did not pass function {}".format(check_authentication.__name__))
        return 0 
    
    for folder_path in folder_gen:
        folder_path = folder_path[0]
        folder_name = get_endpoint_folder(folder_path=folder_path)
        create_folder(folder_path=folder_path, output_path=output_path)
        new_folder_path = os.path.join(output_path,folder_name)
        authentication["fields"]["input_path"] = folder_path
        if authentication["type"] == "key":
            doc_id_gen = create_key_doc_id_gen(authentication)
        else:
            doc_id_gen = create_sas_doc_id_gen(authentication)
        
        _result = download_blob(doc_id_gen=doc_id_gen,authentication=authentication,output_path=new_folder_path)
        result.append(_result)
    
    if close_flag:
        folderfile.close()
        
    return sum(result)

def remove_exif_generator(image_dir_gen, output_path="./"):
    """Remove exif and rotate image

    Args:
        image_dir_gen (generator, optional): ex: (["path/to/image.jpg"]). Defaults to None.
        output_path (str, optional): Defaults to "./".

    Returns:
        int: number of images being processed
    """ 
    cc = cpu_count()
    print("Init {} processes".format(cc))
    p = Pool(cc)
    result = p.starmap(inner_remove_exif_file, zip(image_dir_gen, repeat(output_path)))
    p.close()
    p.join()
    
    return sum(result)

def remove_exif_folder(folder_path, output_path="./"):
    """Remove exif and rotate image

    Args:
        folder_path: "path/to/folder"
        output_path (str, optional): Defaults to "./".

    Returns:
        int: number of images being processed
    """
    folder_name = get_endpoint_folder(folder_path=folder_path)
    create_folder(folder_path=folder_path, output_path=output_path)
    new_folder_path = os.path.join(output_path,folder_name)
    image_dir_gen = create_dir_gen(folder_path)
    image_count = remove_exif_generator(image_dir_gen=image_dir_gen,output_path=new_folder_path)
    
    return image_count