import tarfile

from qbeast import predefs


def is_curator_valid_directory(project_dir):
    check_passed = False
    from pathlib import Path
    if not Path(project_dir).exists():
        return check_passed, f"Path {project_dir} does not exist"
    if not Path(project_dir + '/' + predefs.qbeast_dbt_config_filename).exists():
        return check_passed, f"{predefs.qbeast_dbt_config_filename} not present in the folder"
    if not Path(project_dir + '/ingestion/').exists():
        return check_passed, f"ingestion folder not present in the directory"
    if not Path(project_dir + '/transformation/' + predefs.dbt_config_filename).exists():
        return check_passed, f"{predefs.dbt_config_filename} not present in the folder"
    
    check_passed = True
    return check_passed, "Ok"

def compress_dir(directory, output_name, jar_location):
    file_location = predefs.output_dir + '/' + output_name
    with tarfile.open(file_location, "w:gz") as tar:
        tar.add(jar_location, arcname="/ingestion/qbeast-ingestion.jar")
        tar.add(directory + "/transformation/", arcname="/transformation/")
        tar.add(directory + "/qbeast.yaml", arcname="/qbeast.yaml")
        tar.add("/tmp/profiles.yml", arcname="/profiles.yml")

    return True, file_location


def find_file(pattern, path):
    import os, fnmatch
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def compile_ingestion_app(path, output_name):
    import yaml
    ingestion_command = ""
    with open(path + '/' + "qbeast.yaml", "r") as f:
        try:
            config = yaml.safe_load(f)
            for step in config["steps"]:
                if "ingestion" in step.keys():
                    ingestion_command = step["run"]
        except yaml.YAMLError as exc:
            return False, "Failed to parse the config, please check it has a correct format"

    from subprocess import call

    # 1. Compile ingestion JAR
    rc_compile = call(f"(cd {path+'/ingestion/'}; {' '.join(ingestion_command.split(' '))} )", timeout=predefs.sync_timeout, shell=True)
    if rc_compile != 0:
        return False, "Sync Failed. Failed to compile ingestion JAR"
    # 2. Find JAR in target directory
    jar_path = find_file("*.jar", path+'/ingestion/target/')[0] # There should be only one result

    # 3. Rename JAR to output_name
    file_location = predefs.output_dir + '/' + output_name
    import shutil
    shutil.move(jar_path, file_location)

    return True, file_location

