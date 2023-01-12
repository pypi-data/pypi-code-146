import os
import sys
import threading
import time
import copy
from multiprocessing.pool import ThreadPool

from layerx.datalake.constants import MediaType, FILE_UPLOAD_THREADS, SUB_FILE_LENGTH
from layerx.datalake.s3_upload import S3Upload

imageExtensionList = ['jpg', 'jpeg', 'png']
videoExtensionList = ['mp4', 'mkv']


class FileUpload:
    def __init__(self, client: "DatalakeClient"):
        self._client = client
        self.folder_upload = True
        self.path = ""
        self.upload_type = ""
        self.payload = ''
        self.objectKeyList = []
        self.file_list = []
        self.uploadId = ""
        self.collectionName = ''
        self.collectionId = ""
        self.key_name_array = []
        self.fail_upload_array = []
        self.folder_path = ""
        self.total_keys = 0
        self.progress = 0
        self.count = 0
        self.failed_upload_count = 0
        self.count_lock = threading.Lock()

    '''
    Split object key list
    '''

    def split_object_key_list(self, input_list, sub_size):
        sub_list = [input_list[i:i + sub_size] for i in range(0, len(self.key_name_array), sub_size)]
        return sub_list

    ''''
    Check media type
    '''

    def check_media_type(self, extension):
        if self.upload_type == MediaType.IMAGE.value and extension in imageExtensionList:
            return True
        elif self.upload_type == MediaType.VIDEO.value and extension in videoExtensionList:
            return True
        else:
            return False

    ''''
    Get media file list
    '''

    def get_media_files_list(self):
        dir_list = []

        if self.folder_upload:
            dir_list = os.listdir(self.path)
            self.folder_path = self.path
        else:
            path_array = self.path.split("/")
            dir_list.append(path_array[-1])
            path_array.pop()

            index = 0
            for path_component in path_array:
                if index != 0:
                    self.folder_path += "/"

                self.folder_path += path_component

                index += 1

        # Filter according to upload type
        for file_name in dir_list:
            extension = file_name.split(".")[-1]

            if self.check_media_type(extension):
                self.objectKeyList.append(file_name)
                self.file_list.append(file_name)
                self.key_name_array.append({
                    "key": file_name,
                    "path": self.folder_path + "/" + file_name
                })

        self.total_keys = len(self.key_name_array)

    '''
    Write progress
    '''

    def write_progress(self, count=True):
        if count:
            self.count_lock.acquire()
            try:
                self.count += 1
                self.progress = 100 * (self.count / self.total_keys)
                sys.stdout.write(
                    "\r" + "upload files: " + str(self.count) + f"/{self.total_keys}" + "     " + "progress: " +
                    str(round(self.progress, 2)) + " %")
                sys.stdout.flush()
            finally:
                self.count_lock.release()
        else:
            sys.stdout.write(
                "\r" + "upload files: " + str(self.count) + "     " + "progress: " +
                str(round(self.progress, 2)) + " %")
            sys.stdout.flush()

    ''''
    Add upload failed files into an array
    '''

    def add_fail_files(self, object_key):
        self.count_lock.acquire()
        try:
            file_name = object_key.split("/")[-1]
            #self.fail_upload_array.append(file_name)
            self.fail_upload_array.append({
                "key": file_name,
                "path": self.folder_path + "/" + file_name
            })
            self.failed_upload_count += 1
        finally:
            self.count_lock.release()

    ''''
    Parallel upload
    '''

    def parallel_upload(self, sublist):
        _upload = S3Upload(self._client, self.collectionName, self.uploadId, self.write_progress, self.add_fail_files)
        _upload.multi_part_upload(sublist)

    ''''
    File upload initiate     
    '''

    def file_upload_initiate(self, path, collection_type, collection_name, meta_data_object, override):
       
        self.write_progress(False)

        self.path = path
        self.payload = {
            "collectionType": collection_type,
            "collectionName": collection_name,
            "metaDataObject": meta_data_object
        }
        self.upload_type = collection_type
        self.collectionName = collection_name

        if not os.path.exists(self.path):
            raise Exception("Path does not exists")
        elif os.path.isdir(path):
            self.folder_upload = True
        elif os.path.isfile(path):
            self.folder_upload = False

        """ Get media file list"""
        self.get_media_files_list()
        self.payload["objectKeyList"] = self.objectKeyList

        """Upload metadata in collection"""
        upload_metadata_response = self._client.datalake_interface.upload_metadata_collection(self.payload)

        if not upload_metadata_response["isSuccess"]:
            raise Exception("Can not upload meta data")

        self.uploadId = upload_metadata_response["uploadId"]
        self.collectionId = upload_metadata_response["collectionId"]

        sub_list = self.split_object_key_list(self.key_name_array, SUB_FILE_LENGTH)

        process = ThreadPool(FILE_UPLOAD_THREADS)
        process.map(self.parallel_upload, sub_list)
        process.close()
        process.join()

        print(f"\n\nUpload failed count/total : {self.failed_upload_count}/{self.total_keys}")  
        if self.failed_upload_count > 0:
            print(f'Retrying {self.failed_upload_count} failed uploads.....')
            time.sleep(30)
            #Retry with half no of threads
            #Copy failed array to temp and reset original
            temp_failed_arr = copy.deepcopy(self.fail_upload_array)
            self.fail_upload_array = []
            self.parallel_upload(temp_failed_arr)
            #sub_list_retry = self.split_object_key_list(temp_failed_arr, SUB_FILE_LENGTH)
            #process_retry = ThreadPool(FILE_UPLOAD_THREADS/2)
            #process_retry.map(self.parallel_upload, sub_list_retry)
            #process_retry.close()
            #process_retry.join()
            print('Finished processing failed uploads')
        
        time.sleep(1)
        #if self.progress != 0:
        complete_res = self._client.datalake_interface.complete_collection_upload(self.uploadId)
        if complete_res["isSuccess"]:
            print("\nComplete upload")
        else:
            print("\nError In complete upload")

        if len(self.fail_upload_array) != 0:
            print(f"\n\nupload failed files: {self.failed_upload_count}/{self.total_keys}")
            for failed_obj in self.fail_upload_array:
                file_name = failed_obj["key"]
                print(f'{file_name}')

    def get_upload_status(self, collection_name):
        if(collection_name == None):
            print('Invalid collection name')
        else:
            progress_response = self._client.datalake_interface.get_upload_status(collection_name)
            return progress_response