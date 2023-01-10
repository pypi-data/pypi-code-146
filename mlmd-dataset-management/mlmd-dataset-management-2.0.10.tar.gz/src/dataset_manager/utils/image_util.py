from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ServiceRequestError, ResourceNotFoundError, HttpResponseError
import os
import numpy as np
import urllib.request
import glob

ORIENTATION_TAG = b"\x01\x12"
ORIENTATION_FORMAT = b"\x00\x03"
IMAGE_COLOR_FLAG = -1
EXIF_END_TAG = b"\xFF\xDB\x00\x43\x00"
APP1_VALUE = b"\xff\xe1"
EXIF_HEADER_VALUE = b"\x45\x78\x69\x66\x00\x00"
COMPRESSION_QUALITY = 95

def inner_download_blob(doc_id, authentication, output_path):
    doc_id = doc_id[0].rstrip()
    filename, extension = os.path.splitext(os.path.basename(doc_id))
    outfile_path = os.path.join(output_path, "{}.JPG".format(filename))
    if os.path.exists(outfile_path):
        print("Skipping {} due to existed".format(doc_id))
        return False
    
    if set(authentication.keys()) != set(["fields", "type"]):
        print("Not correct parameters {}".format(authentication.keys()))
        return False    
    if authentication["type"]=="key":
        buff = connect_and_download_key(doc_id, authentication)
    elif authentication["type"]=="sas":
        buff = connect_and_download_sas(doc_id, authentication)
    else:
        print("Type {} not exists".format(authentication["type"]))
        return False
    
    if buff:
        remove_exif_and_save(doc_id, buff, outfile_path)
    else:
        print("Empty buff {}".format(doc_id))
        return False
    
    return True

def remove_exif_and_save(doc_id, buff, outfile_path):
    import cv2
    # get tag values
    indexes = get_indexes(buff)
    orientation_value = get_orientation(buff[:indexes["APP1_header_index"] + 2 + indexes["Exif_length"]], indexes["Align"])
    
    # rotate and save
    exif_end_index = buff.rfind(EXIF_END_TAG)  
    if orientation_value != 1 or exif_end_index == -1:      
        image = cv2.imdecode(np.frombuffer(buff, np.uint8), IMAGE_COLOR_FLAG)
        # Check output image empty
        if image.size:
            cv2.imwrite(outfile_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), COMPRESSION_QUALITY])     
        else:
            print("Empty output image {}".format(doc_id))
            return False
    if orientation_value == 1 and exif_end_index != -1:
        with open(outfile_path, "wb") as f:        
            f.write(buff[:2] + buff[exif_end_index:]) 
    
    return True

def check_authentication(authentication):
    authentication_dict = {"key":["connection_string", "container_name", "input_path"], "sas":["account_url","credential","container_name","input_path"]}
    if not isinstance(authentication, dict):
        print("Wrong type authentication")
        return False
    if authentication["type"] == "key" and set(authentication["fields"].keys()) == set(authentication_dict["key"]):
        return True
    if authentication["type"] == "sas" and set(authentication["fields"].keys()) == set(authentication_dict["sas"]):
        return True
    print("Invalid authentication")
    return False 

def connect_and_download_key(doc_id, authentication):
    authentication_field_check = check_authentication(authentication)
    if not authentication_field_check:
        print("Did not pass function {}".format(check_authentication.__name__))
        return None 
    
    print("Downloading {}...".format(doc_id))
    try: 
        blob_service_client = BlobServiceClient.from_connection_string(authentication["fields"]["connection_string"])
        container = blob_service_client.get_container_client(authentication["fields"]["container_name"])  
        container.get_container_properties()
    except ServiceRequestError as e:
        print("Invalid connection string {}".format(authentication["fields"]["connection_string"]))
        return None
    except (ResourceNotFoundError, HttpResponseError) as e:
        print("Invalid container_name {}".format(authentication["fields"]["container_name"]))
        return None
    except Exception as e:
        print("Error code {}".format(type(e).__name__))
        return None
    
    doc_id = os.path.join(authentication["fields"]["input_path"],doc_id)
    blob_client = container.get_blob_client(doc_id)    
    
    if not blob_client.exists():
        print("doc {} not exists".format(doc_id))
        return None
    buff = blob_client.download_blob().readall()
    blob_client.close()
    
    return buff

def connect_and_download_sas(doc_id, authentication):
    authentication_fields_check = check_authentication(authentication)
    if not authentication_fields_check:
        print("Did not pass function {}".format(check_authentication.__name__))
        return None 
    
    print("Downloading {}...".format(doc_id))
    authentication = authentication["fields"]
    url_with_sas = authentication["account_url"] + "/" + authentication["container_name"] + "/" + authentication["input_path"] + "/" + doc_id + "?" + authentication["credential"]

    try:
        req = urllib.request.urlopen(url_with_sas)
        buff = bytearray(req.read())
    except:
        print("doc {} not exists".format(doc_id))
        return None
    
    return buff

def get_indexes(buff):
    # app1_header, length, align
    result = {}
    reverse_flag = None
    # find header and length of exif 
    app1_header = buff.find(APP1_VALUE)
    exif_length = int.from_bytes(buff[app1_header+2:app1_header+4], byteorder = "big")
    result["APP1_header_index"], result["Exif_length"] = app1_header, exif_length 

    # find align marker
    exif_header = buff.find(EXIF_HEADER_VALUE)
    result["Exif_header"] = exif_header
    align_marker = buff[exif_header+len(EXIF_HEADER_VALUE):exif_header+len(EXIF_HEADER_VALUE)+2]

    if align_marker == b"II":
        reverse_flag = True
    elif align_marker == b"MM":
        reverse_flag = False
    result["Align"] = reverse_flag
    
    return result

def get_orientation(exif_buff, reverse_flag):
    if reverse_flag:
        orientation_tag = ORIENTATION_TAG[::-1]
        orientation_format = ORIENTATION_FORMAT[::-1]
    else: 
        orientation_tag = ORIENTATION_TAG
        orientation_format = ORIENTATION_FORMAT

    index = 0
    format_bytes = b""
    
    # check tag and format
    while index != -1 and format_bytes != orientation_format:
        index = exif_buff.find(orientation_tag, index + 1)
        format_bytes = exif_buff[index + len(orientation_tag): index + len(orientation_tag) + 2]
    
    # check orientation
    if index != -1:
        offset = len(orientation_tag) + len(orientation_format) + 4
        # orientation is always 2 bytes, read in alignment order
        orientation_bytes = exif_buff[index + offset: index + offset + 4][:2]
    
        if reverse_flag:
            orientation_value = int.from_bytes(orientation_bytes, byteorder = "little")
        else:
            orientation_value = int.from_bytes(orientation_bytes, byteorder = "big")
    else:
        # no orientation tag found
        orientation_value = 1
    
    return orientation_value

def create_sas_doc_id_gen(authentication):
    authentication_fields_check = check_authentication(authentication)
    if not authentication_fields_check:
        print("Did not pass function {}".format(check_authentication.__name__))
        return None 
    
    authentication = authentication["fields"]
    blob_service_client = BlobServiceClient(account_url=authentication["account_url"], credential= authentication["credential"])
    container = blob_service_client.get_container_client(authentication["container_name"])
    blob_list_iter = container.list_blobs(results_per_page=2, name_starts_with= authentication["input_path"]).by_page()
    stop = False
    while not stop:
        try: 
            blob_list = next(blob_list_iter)
            for blob in blob_list:
                filename, extension = os.path.splitext(os.path.basename(blob.name))
                if extension in [".jpg",".JPG",".jpeg",".JPEG",""]:
                    yield [filename + extension]
        except StopIteration:
            stop = True
     
def create_key_doc_id_gen(authentication):
    # Need advide on this authentication checking, should build a separate checking function? 
    # Can not return container object => merge authentication checking in connecting function
    authentication_field_check = check_authentication(authentication)
    if not authentication_field_check:
        print("Did not pass function {}".format(check_authentication.__name__))
        return None 
    
    try: 
        blob_service_client = BlobServiceClient.from_connection_string(authentication["fields"]["connection_string"])
        container = blob_service_client.get_container_client(authentication["fields"]["container_name"])  
        container.get_container_properties()
    except ServiceRequestError as e:
        print("Invalid connection string {}".format(authentication["fields"]["connection_string"]))
        return None
    except (ResourceNotFoundError, HttpResponseError) as e:
        print("Invalid container_name {}".format(authentication["fields"]["container_name"]))
        return None
    except Exception as e:
        print("Error code {}".format(type(e).__name__))
        return None
      
    blob_list_iter = container.list_blobs(results_per_page=2, name_starts_with=authentication["fields"]["input_path"]).by_page()
    stop = False
    while not stop:
        try:
            blob_list = next(blob_list_iter)
            for blob in blob_list:
                filename = os.path.basename(blob.name)
                yield [filename]
        except StopIteration:
            stop = True

def create_folder(folder_path, output_path="./"):
    folder_name = get_endpoint_folder(folder_path=folder_path)
    if not os.path.exists(os.path.join(output_path,folder_name)):
        os.mkdir(os.path.join(output_path, folder_name))
    else:
        pass
    
def get_endpoint_folder(folder_path):
    without_extra_slash = os.path.normpath(folder_path)
    folder_name = os.path.basename(without_extra_slash)
    
    return folder_name

def create_dir_gen(folder_dir):
    image_dirs = []
    if os.path.exists(folder_dir):
        image_dirs = glob.glob(folder_dir + "/*")
    for image_dir in image_dirs:
        yield([image_dir])

def read_image_dir(image_dir):
    with open(image_dir, "rb") as image:
        image_file = image.read()
        buff = bytearray(image_file)
    return buff

def inner_remove_exif_file(image_dir, output_path):
    image_dir = image_dir[0].rstrip()
    filename, extension = os.path.splitext(os.path.basename(image_dir))
    outfile_path = os.path.join(output_path, "{}.JPG".format(filename))
    if os.path.exists(outfile_path):
        print("Skipping {} due to existed".format(filename))
        return False
    buff = read_image_dir(image_dir)    
    
    if buff:
        remove_exif_and_save(filename, buff, outfile_path)
    else:
        print("Empty buff {}".format(filename))
        return False
    
    return True
