import azureml.core
from azureml.core import Workspace, Datastore, Environment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration


def load_workspace(config_aml_path):
    # Load the workspace from the saved config file
    workspace = Workspace.from_config(config_aml_path)
    print(
        "Ready to use Azure ML {} to work with {}".format(
            azureml.core.VERSION, workspace.name
        )
    )
    return workspace


def get_datastore(workspace, name=""):
    if name == "":
        # Get the default datastore
        datastore = workspace.get_default_datastore()
        print("Default datastore - {} - loaded.".format(datastore.name))
    else:
        datastore = Datastore.get(workspace, name)
        print("Datastore - {} - loaded.".format(datastore.name))
    return datastore


def create_cluster(
    workspace,
    cluster_name="cluster-cpu",
    vm_size="STANDARD_DS3_V2",
    max_nodes=4,
    vnet_resourcegroup_name="",
    vnet_name="",
    subnet_name=""
):
    cluster = None
    try:
        # Check for existing compute target
        cluster = ComputeTarget(workspace=workspace, name=cluster_name)
        print("Found existing cluster, use it.")
        print("cluster_name: {}, vm_size: {}".format(cluster.name, cluster.vm_size))
    except ComputeTargetException:
        # If it doesn't already exist, create it
        try:
            print(
                "Creating cluster: {}, vm_size: {}, max_nodes: {}".format(
                    cluster_name, vm_size, max_nodes
                )
            )
            compute_config = AmlCompute.provisioning_configuration(
                vm_size=vm_size,
                max_nodes=max_nodes,
                vnet_resourcegroup_name=vnet_resourcegroup_name,
                vnet_name=vnet_name,
                subnet_name=subnet_name
            )
            cluster = ComputeTarget.create(workspace, cluster_name, compute_config)
            cluster.wait_for_completion(
                show_output=True
            )
            print("Compute cluster created !")
        except Exception as ex:
            print(ex)
    return cluster


def create_environment(
    workspace,
    environment_name,
    version=None,
    conda_dependencies_file="./aml/conda_dependencies.yml",
    register=True,
    dockerfile=None,
):

    conda_dependencies_file_path = conda_dependencies_file

    # Create a Python environment for the experiment
    environment = Environment(environment_name)

    # Create a set of package dependencies
    aml_packages = CondaDependencies(conda_dependencies_file_path)

    # Add the dependencies to the environment
    environment.python.conda_dependencies = aml_packages

    if dockerfile:
        environment.docker.base_image = None
        DOCKER_PATH = dockerfile
        with open(DOCKER_PATH, "r") as f:
            dockerfile = f.read()
        environment.docker.base_dockerfile = dockerfile
        environment.docker.enabled = True

    if register:
        # Register the environment
        environment.register(workspace=workspace)
        environment = Environment.get(workspace, environment_name, version=version)

    return environment


def create_run_config(cluster, registered_environment):

    # create a new run configuration
    run_config = RunConfiguration()

    # Use the compute you created above.
    run_config.target = cluster

    # Assign the environment to the run configuration
    run_config.environment = registered_environment

    print("Run configuration created.")

    return run_config
