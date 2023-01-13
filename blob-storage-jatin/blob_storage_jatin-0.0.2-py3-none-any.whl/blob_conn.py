from azure.storage.blob import BlobServiceClient
import traceback
import blob_storage_jatin.config as config

blobConnStr = config.BLOB_CONN_STR
containerName = config.CONTAINER_NAME
blob_name = config.BLOB_NAME
logs_blob_name = config.LOGS_BLOB_NAME


class BlobStorageAPI:

    def write_to_blob(self, blob_name, content):
        global blobConnStr
        global containerName
        try:
            blob_service_client = BlobServiceClient.from_connection_string(conn_str=blobConnStr)
            container_client = blob_service_client.get_container_client(containerName)
            block_blob_client = container_client.get_blob_client(blob_name)
            upload_blob_response = block_blob_client.upload_blob(content, length=len(content), blob_type="BlockBlob")
            print("created.--------- \n", upload_blob_response, "\n")
            return "created." + str(upload_blob_response)
        except:
            return str(traceback.format_exc())

    def get_data_from_default_blob(self):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(conn_str=blobConnStr)
            container_client = blob_service_client.get_container_client(containerName)
            block_blob_client = container_client.get_blob_client(blob_name)
            upload_blob_response = block_blob_client.download_blob()
            data = upload_blob_response.readall()
            print("default output === ", data)
            return data
        except:
            return str(traceback.format_exc())

    def get_data_from_blob(self, blob_name):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(conn_str=blobConnStr)
            container_client = blob_service_client.get_container_client(containerName)
            block_blob_client = container_client.get_blob_client(blob_name)
            upload_blob_response = block_blob_client.download_blob()
            data = upload_blob_response.readall()
            print("output === ", data)
            return data
        except:
            return str(traceback.format_exc())

    def write_logs(self, message):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(conn_str=blobConnStr)
            container_client = blob_service_client.get_container_client(containerName)
            block_blob_client = container_client.get_blob_client(logs_blob_name)
            upload_blob_response = block_blob_client.append_block(message, length=len(message))
            return upload_blob_response
            # return True
        except:
            return str(traceback.format_exc())

    def create_logs_blob(self):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(conn_str=blobConnStr)
            container_client = blob_service_client.get_container_client(containerName)
            block_blob_client = container_client.get_blob_client(logs_blob_name)
            if not block_blob_client.exists():
                upload_blob_response = block_blob_client.create_append_blob()
            return True
        except:
            return str(traceback.format_exc())


if __name__ == "__main__":
    blob_conn = BlobStorageAPI()
    print(blob_conn.get_data_from_blob("temp_req.txt"))
    # print(blob_conn.write_to_blob(blob_name, "Hi this is the new blob configured on friday 6th Jan"))
    # output = blob_conn.write_to_blob("new_3.txt", "Hi creating a new blob")
    # print("++++++", output)
    # blob_conn.create_blob()
    # print(blob_conn.write_logs("Finished ====== "))
    # print(blob_conn.write_logs("ENDED FINALLY "))
    # print(writeToBlob(containerClient, "temp_data.txt", "temp data"))
