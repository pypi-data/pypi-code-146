import boto3, botocore, json, os, tqdm, threading, datetime

try:
    s3_client = boto3.client('s3', region_name="ap-southeast-2") # Connect to the AWS S3 bucket
except Exception as error:
    print("""\033[91mFor first-timers, be sure to generate a credentials file as ~/.aws/credentials with the following information:
    [default]
    aws_access_key_id = ********
    aws_secret_access_key = ***********\n    
    If that does not fix this, then please investigate the following error\033[0m""")
    raise error


def upload_file_to_S3(project_name: str, local_filepath: str, filename: str, version=datetime.date.today().strftime("%Y_%m_%d")):
    """
    Update a file to the project folder in the S3 urbanintelligencedevdata bucket.
    """
    s3_client.upload_file(local_filepath, "urbanintelligencedevdata", f"data/{project_name}/{version}/{filename}", Callback=ProgressPercentage(local_filepath))


def update_S3_versions(project_name, dev_version=None, test_version=None, prod_version=None):
    """
    Edits the versions.json file on the S3 urbanintelligencedevdata bucket to the new versions provided for each domain (dev/test/prod) on a given project_name.
    """

    # Download the current versions.json file
    try:
        s3_client.download_file("urbanintelligencedevdata", "data/versions.json", "versions.json")
    except botocore.exceptions.ClientError as error:
        print("A error occured downloading versions.json from the S3 bucket.")
        raise error

    # Read the file and make the necessary changes as requested
    with open("versions.json") as file:
        versions = json.load(file)

    if dev_version:
        versions[project_name]["dev"] = dev_version
    if test_version:
        versions[project_name]["test"] = test_version
    if prod_version:
        versions[project_name]["production"] = prod_version

    with open("versions.json", "w") as file:
        json.dump(versions, file)

    # Upload the modified versions.json to the bucket
    try:
        s3_client.upload_file("versions.json", "urbanintelligencedevdata", "data/versions.json", Callback=ProgressPercentage("versions.json"))
    except botocore.exceptions.ClientError as error:
        print("A error occured uploading the modified versions.json to the S3 bucket.")
        raise error
    
    os.remove("versions.json") # Cleanup


def remove_previous_versions(project_name, current_version):
    """
    Delete ALL files and folders (except the current_version) for a given project_name from the S3 urbanintelligencedevdata bucket
    """

    # Get all the subfolders and objects within this project folder
    result = s3_client.list_objects(Bucket="urbanintelligencedevdata", Prefix=f"data/{project_name}/", Delimiter='/')
    version_folders = [version_folder.get('Prefix') for version_folder in result.get('CommonPrefixes')]
    
    # Obviosuly, we should not delete the folder with the new data in it!
    version_folders.remove(f"data/{project_name}/{current_version}/")

    # The client can tag objections for deletion, but can't go ahead with it. Hence, use the Bucket Resource.
    bucket = boto3.resource('s3').Bucket('urbanintelligencedevdata')
    for version_folder in version_folders:
        bucket.objects.filter(Prefix=version_folder).delete()


class ProgressPercentage(object):
    """
    Display the progress of an uploading file to S3 using tqdm.
    """
    def __init__(self, filename):
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        self.pbar = tqdm.tqdm(desc=f"Uploading {filename}", total=100, leave=False, dynamic_ncols=True)

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            self.pbar.n = round((self._seen_so_far / self._size) * 100, 2)
            self.pbar.refresh()