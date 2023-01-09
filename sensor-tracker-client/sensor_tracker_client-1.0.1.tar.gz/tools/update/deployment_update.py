import csv

from sensor_tracker_client import sensor_tracker_client as stc

accept_variables = ["start_time", "end_time", "wmo_id", "deployment_number", "title", "comment", "acknowledgement",
                    "contributor_name", "contributor_role", "creator_email", "creator_name", "creator_url",
                    "data_repository_link", "publisher_email", "publisher_name", "publisher_url", "metadata_link",
                    "references", "sea_name", "deployment_latitude", "deployment_longitude", "recovery_latitude",
                    "recovery_longitude", "deployment_cruise", "recovery_cruise", "deployment_personnel",
                    "recovery_personnel", "depth", "contributors_email", "agencies", "agencies_role", "site", "program",
                    "transmission_system", "positioning_system", "publisher_country"]


def read_csv_file(file_name):
    """
    First element is the header then it is the datas
    :param file_name:
    :return:
    """
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def data_filter(headers):
    for header in headers:
        if header not in accept_variables:
            print(header)
            raise ValueError


def get_deployments(deployment_list):
    deployment_dicts = []
    for num in deployment_list:
        deployment_dicts.extend(stc.deployment.get({"deployment_number": num}).dict)
    return deployment_dicts


def generate_update_list(csv_data_list):
    header = csv_data_list[0]
    data_filter(header)
    new_csv_data_list = []
    for d in csv_data_list[1:]:
        data_dict = dict()
        for pos, h in enumerate(header):
            data_dict[h] = d[pos]
        new_csv_data_list.append(data_dict)
    return new_csv_data_list


def update_sensor_tracker(csv_data_dicts, deployment_dicts):
    for pos, data in enumerate(csv_data_dicts):
        deployment_id = deployment_dicts[pos]["id"]
        data.pop("deployment_number")
        stc.deployment.patch(deployment_id, data)


def update_deployment_page(csv_file_path, token, debug=True):
    stc.basic.DEBUG = debug
    stc.authentication.token = token
    deployment_num_list = []
    csv_data = read_csv_file(csv_file_path)
    csv_data_dicts = generate_update_list(csv_data)
    for deployment in csv_data_dicts:
        deployment_num_list.append(deployment["deployment_number"])
    deployments_data_list = get_deployments(deployment_num_list)
    update_sensor_tracker(csv_data_dicts, deployments_data_list)
