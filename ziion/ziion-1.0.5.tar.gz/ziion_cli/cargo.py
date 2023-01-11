
from packaging import version
import subprocess
import platform
import ziion_cli.dispatcher
import ziion_cli.utils
from ziion_cli.constants import (
    CARGO_ARTIFACTS_DIR,
    CARGO_DIR
)

def installed_versions():
    output = subprocess.check_output(["cargo","install","--list"])
    return ziion_cli.utils.parse_str_to_dict(output.decode("utf-8"))


def list_packages_to_be_updated(s3_packages_list, local_packages_list):
    packages_to_update=[]
    print ("\n{:<30} {:<15} {:<15}".format('Package','Installed','Latest'))
    print ("-"*55)
    for package in s3_packages_list:
        if package not in local_packages_list:
            print ("{:<30} {:<15} {:<15}".format(package," No ", s3_packages_list[package]))
            packages_to_update.append(package)
        elif package in local_packages_list:
            print ("{:<30} {:<15} {:<15}".format(package,local_packages_list[package], s3_packages_list[package]))
        elif version.parse(s3_packages_list[package]) > version.parse(local_packages_list[package]):
            print ("{:<30} {:<15} {:<15}".format(package,local_packages_list[package], s3_packages_list[package]))
            packages_to_update.append(package)
    print("\n")
    return packages_to_update

def update_necessary_packages(s3_packages_list, local_packages_list):
    print("\nPackages to be updated:")
    packages = list_packages_to_be_updated(s3_packages_list, local_packages_list)
    if platform.machine() == 'x86_64':
        s3_folder = "rust-amd-binaries/"
    elif platform.machine() == 'aarch64':
        s3_folder = "rust-arm-binaries/"
    for package in packages:
        download = subprocess.run(["wget", "-O", CARGO_ARTIFACTS_DIR.joinpath(package), "https://ziion-binaries.s3.amazonaws.com/"+ s3_folder + package], 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
        subprocess.run(["chmod", "755", CARGO_ARTIFACTS_DIR.joinpath(package)], 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
        if download.returncode == 0:
            print(package + " updated succesfully.")
        else:
            print(package + " could not be updated correctly.")
    if packages: 
        subprocess.run(["wget", "-O", str(CARGO_DIR) + "/.crates.toml", "https://ziion-binaries.s3.amazonaws.com/"+ s3_folder + ".crates.toml"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
    print("\n")