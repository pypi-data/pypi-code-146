"""
Script to download images and text files to local machine and generate path file
"""
import requests
import json
import os
from multiprocessing.pool import ThreadPool
from zipfile import ZipFile


# # IP+port or url of the server # (eg: https://qa.deepzea.com)
# serverUrl = 'http://localhost:8080' # default

class DatasetSync:
    def __init__(self, encoded_key_secret: str, server_url: str):
        self.failed_downloads_present = False
        self.encoded_key_secret = encoded_key_secret
        self.server_url = server_url


    """
    method to get item URL list from layerX (per page)
    @params - callUrl=(Url to get itemlist of given group and version from layerx), payload=(pageNo,pageSize)
    @returns - response=(response from layerX containing URL list)"""
    def get_data_from_server(self, call_url, payload):

        hed = {'Authorization': 'Basic ' + self.encoded_key_secret}

        print(hed)
        print(call_url)
        try:
            call_response = requests.get(call_url, params=payload, headers=hed, timeout=10)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.Timeout) as e :
            print(f'Error connecting to layerx')
            print(e.errno)
            print("We are facing a problem with the network, please retry to download missing items")
            quit()
        print(call_response, flush=True)
        response = call_response.json()
        return response

    """
    Method to download files
    @params: fileData=(data including url of file), downloadLocation=(file path to save downloaded file) """
    def download_file(self, file_data, download_location):
        # download files from newly added paths
        # print('Downloading file '+fileData["fileName"])
        r = requests.get(file_data["fileUrl"], timeout=25)
        download_path = download_location
        # print(downloadLocation)
        with open(download_path, 'wb') as f:
            f.write(r.content)

    """
     handle download for a single dataset item (image and textfile)
     @params: arg_list=[fileData=(data of file), identifier=(unique identifier name for the dataset version)]
     @returns: {False<when download failed>, arg_list<from params>}
           or  {
                   True<when download success>,
                   {textFileImagePathData={imagePath=(file path of downloaded item), pathFileName=("training path file" name - stores paths of downloaded images used for training)}}
               } """
    def handle_one_download(self, arg_list):
        file_data = arg_list[0]
        # //print(fileData)
        # identifier = arg_list[1]
        # ---------------------

        formatted_write_key = file_data['fileName']
        file_path = f'{file_data["fileDownloadFolderLocation"]}/' + file_data['fileName']

        # if item have to be extracted (a zip file)    
        if "isUnzipRequired" in file_data:
            folder_path_absolute = os.path.abspath(f'./{self.data_directory_name}/' + file_path)
            file_path = f'{file_path}.zip'

        file_path_absoulute = os.path.abspath(f'./{self.data_directory_name}/' + file_path)

        if "writingPathFileName" in file_data:
            # write to a annotation file path list
            path_file_name = file_data["writingPathFileName"]
            text_file_image_path_data = (file_path_absoulute, path_file_name)
        else:
            text_file_image_path_data = None

        if "rawAnnotations" in file_data:
            # append raw annotations to json
            self.raw_data_arr.append(file_data["rawAnnotations"])

        if(not os.path.exists(file_path_absoulute)):
            # download files
            try:
                if "fileUrl" in file_data:
                    self.download_file(file_data, file_path_absoulute)  # download image
            except Exception as e:
                print(f'Failed downloading - {formatted_write_key}')
                print(e)
                return (False, arg_list)

            # if item have to be extracted (a zip file)    
            if "isUnzipRequired" in file_data:
                with ZipFile(file_path_absoulute, 'r') as zObject:
                    zObject.extractall(path=folder_path_absolute)

            # If item is not available in the syncdatafile (file hasn't downloaded before)
            print('Downloded item - ' + formatted_write_key)

            # return fileName and textFileName to update the textfile
            return (True,  text_file_image_path_data)

        else:
            print('Item already exists, OK ', file_data['fileName'])
            return (True, text_file_image_path_data)

    """
    main method to download items and update datafiles
    @params: dataList=(response from layerX containing URL list) """
    def download_page(self, data_list):
        arg_list = []
        for val in data_list['resourceArray']:
            arg_list.append([val, data_list['identifier']])

        # Download items in parallel
        print("starting page download")
        with ThreadPool(10) as p:
            for res in p.imap(self.handle_one_download, arg_list):
                is_downloded = res[0]
                download_data = res[1]
                if not is_downloded:
                    # try again to download the failed download
                    print(f"Retrying Download - {download_data[0]['fileName']}")
                    res = self.handle_one_download(download_data)
                    is_downloded = res[0]
                    download_data = res[1]

                if is_downloded:
                    #if file is downloaded, write it to master csv
                    text_file_image_path_data = download_data

                    if text_file_image_path_data is not None:
                        # write image file path to train text file
                        image_path = text_file_image_path_data[0]
                        path_file_name = text_file_image_path_data[1]
                        text_path_file_location = os.path.join(self.data_directory_name, path_file_name)
                        with open(text_path_file_location, 'a+', newline='') as train_txt_file:
                            train_txt_file.write(image_path + "\n")
                        p.close()
                else:
                    print(f"Retrying Failed! - {download_data[0]['fileName']}")
                    self.failed_downloads_present = True
                    p.close()

        print("page download done")

    """
    Method to create required directories for file download """
    def initiate_download(self, response, page_no):
        print("data format: ", response['format'])

        # global self.dataDirectoryName  # folder to download image and text files
        # create a folder with dataset groupname
        self.data_directory_name = response['groupUniqueName']
        data_directory_path = f'./{self.data_directory_name}'

        if page_no == 1:
            print('1st page')
            # create required files and directories
            if not os.path.exists(data_directory_path):
                os.makedirs(data_directory_path)
                print(f"Created {self.data_directory_name} folder")
            
            # get raw json file name (if applicable)
            if "rawFileName" in response:
                self.json_file_name = response["rawFileName"]

        # create required directories
        for directory in response["creatableDirectories"]:
            dir_path = os.path.join(data_directory_path, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"Created folder - {dir_path}")

        # updateVersionData(response)
        self.download_page(response)

    """
    method to get url list from server and execute the main script for all pages
    @params - callUrl (Url to get itemlist of given group and version from layerx), pageNo """
    def get_all_pages(self, call_url, page_no):
        payload = {'pageNo': page_no, 'pageSize': 250}
        response = self.get_data_from_server(call_url, payload)
        print('Downloading page no: ' + str(page_no))
        if "identifier" in response:

            # Direct the response to download files
            self.initiate_download(response, page_no)

            # recursively call this again to get next page
            if(response['nextPage'] == True):
                next_page_no = int(page_no)+1
                self.get_all_pages(call_url, next_page_no)
            print("Download Complete")
            if self.failed_downloads_present:
                print(
                    "Unfortunately we failed to download everything, please retry to download missing items")

        else:
            print("No data recieved from remote for given group and/or version")

    # main script starter
    """
    Download dataset
    From dataset manager
    @param version_id - id of dataset version 
    @param export_type - dataset export format """
    def download_dataset(self, version_id: str, export_type: str):
        # get dataset url data from server
        _base_url = f'{self.server_url}/dataset/api/dataset/getVersionData/'
        _call_url = f'{_base_url}{version_id}/{export_type}/'
        # start operation
        self.get_all_pages(_call_url, 1)
        # quit()

    # main script starter
    """
    Download collection annotations
    From datalake - Both ground trugh
    @param collection_id - id of dataset version  
    @param model_id - Optional: id of the model (same operation_id given in upload annotations) 
    if we need annotations for that specific model """
    def download_collection(self, collection_id: str, model_id: str):
        # get collection url data from server
        _base_url = f'{self.server_url}/datalake/api/client/getAnnotations/'
        #Pass the model_id only if specified
        if model_id is None:
            _call_url = f'{_base_url}{collection_id}/collection/'
        else:
            _call_url = f'{_base_url}{collection_id}/collection?operationId={model_id}'

        # define annotation json object 
        self.raw_data_arr = []
        self.json_file_name = 'default_json_filename.json'
        
        # start operation
        self.get_all_pages(_call_url, 1)

        # save json (anno list) to a file
        _raw_annotations = {
            "images": self.raw_data_arr
        }
        json_raw_annotations = json.dumps(_raw_annotations, indent=2)
        _file_path = os.path.join(self.data_directory_name, self.json_file_name)
        with open(_file_path, "w") as outfile:
            outfile.write(json_raw_annotations)
        print("Created RAW annotation file")
        # quit()

    # # main script below
    # def main():
    #     # start operation
    #     getAllPages(callUrl, 1)

    # # run main method
    # main()
    # # ---------------


# sample run command:
# python3 sync.py <url> <version ID> <format type> <access token>
