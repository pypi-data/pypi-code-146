"""
Connecting to Linux servers (e.g. Piwakawaka) to execute terminal commands, as well as uploading files and/or whole directories to the server
"""

__all__ = ["Server"]

import paramiko, os, tqdm, warnings, zipfile, tempfile
from uintel import config

class Server(object):
    """
    A SSH and SFTP client that can execute commands on any Linux server and send files.
    """
    def __init__(self) -> None:
        """
        Create a SSH and SFTP client with a server. The client searches for any local RSA key files (if indictaed in the UI configuration file) otherwise it uses the given password.
        """
        client = paramiko.SSHClient()
        credentials = config["SSH"].copy()
        try:
            if credentials["ssh_key"]:
                # Set it to automatically add the host to known hosts
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=credentials["host"], username=credentials["username"])
            else:
                client.connect(hostname=credentials["host"], username=credentials["username"], password=credentials["password"])
        except paramiko.SSHException as error:
            warnings.warn(f"Unfortunately, your credentials could not be verified. Connection to {credentials['host']} failed.\n{error}")
            return

        self.client = client
        self.sftp_client = client.open_sftp()
    
    def close(self) -> None:
        """
        Close the SSH connection with the server
        """
        self.client.close()
        self.sftp_client.close()

    def execute_command(self, command: str, show_output=True) -> None:
        """
        Execute a command on the sever
        """
        # Execute the command
        _, ssh_stdout, ssh_stderr = self.client.exec_command(command)
        # Display the output
        output = ''
        for line in ssh_stdout.readlines():
            output += line
        if output and show_output:
            print(output)

        error = ''
        for line in ssh_stderr.readlines():
            error += line
        if error:
            warnings.warn(f"The command: {command} could not be executed due to: \n{error}")
    
    def transfer_file(self, local_path: str, remote_path: str, show_progress=True, perm=775, group="www-data") -> None:
        """
        Upload a local file to the given remote filepath on the server
        """
        def print_progress(transferred, toBeTransferred):
            transferred = transferred/1e6 # in MB now
            toBeTransferred = toBeTransferred/1e6 # in MB now
            print(f"Progress: {100*transferred/toBeTransferred:.2f}%\t Transferred: {transferred:.2f} / {toBeTransferred:.2f} MB", end="\n" if transferred/toBeTransferred == 1 else "\r")
        
        self.execute_command(f"rm {remote_path}", show_output=True)
        _ = self.sftp_client.put(local_path, remote_path, callback=print_progress if show_progress else None, confirm=True)
        
        self.execute_command(f'chmod {perm} {remote_path} 2> /dev/null')
        self.execute_command(f'chgrp {group} {remote_path}')

    def transfer_directory(self, local_directory: str, remote_directory: str, show_progress=True, zip_compression=zipfile.ZIP_DEFLATED, perm=775, group="www-data") -> None:
        """
        Zip a whole diretory and then send it to the remote filepath on the server and uncompress
        """    
        # Check the directory specified exists
        if not os.path.exists(local_directory):
            warnings.warn(f"The local directory {local_directory} does not exists.")
            return
        
        # Complete the walk through the top 3 nested subdirectories to add files
        all_files = []
        for root, subdirs, files in os.walk(local_directory):
            for file in files:
                all_files.append((os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(local_directory, '..'))))

            for subdir in subdirs:
                for root, subdirs, files in os.walk(subdir):
                    for file in files:
                        all_files.append((os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(local_directory, '..'))))

                    for subdir in subdirs:
                        for root, subdirs, files in os.walk(subdir):
                            for file in files:
                                all_files.append((os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(local_directory, '..'))))
        
        if len(all_files) == 0:
            warnings.warn(f"No files were found in the top 3 subdirectories of {local_directory}. Please extend this, otherwise the zip file has been skipped.")
            return
        
        # Make the zip file
        temp_dir = tempfile.TemporaryDirectory()
        local_path = os.path.join(temp_dir.name, "zipped_dir.zip")
        with zipfile.ZipFile(local_path, "w", compression=zip_compression) as zip:
            for filepath, filename in tqdm.tqdm(all_files, "Creating ZIP file", total=len(all_files), leave=False, dynamic_ncols=True):
                zip.write(filepath, arcname=filename)

        # Upload the zip file
        remote_path = "{}zipped_dir.zip".format(remote_directory if remote_directory.endswith("/") else remote_directory + "/")
        self.transfer_file(local_path, remote_path, show_progress)
        # Unzip and overwrite on the server
        self.execute_command(f"unzip -o {remote_path} -d {remote_directory}..")
        # Delete the zip files on the server and local path
        self.execute_command(f"rm {remote_path}")
        temp_dir.cleanup()
        
        self.execute_command(f'chmod -R {perm} {remote_directory} 2> /dev/null')
        self.execute_command(f'chgrp -R {group} {remote_directory}')
