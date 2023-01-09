import boto3
import json
import uuid

from api import Response
from dynamodb import Table


def handler(event, context):
    """Runs a image"""

    method = event["httpMethod"]
    resource = event["resource"]

    key = (event.get("pathParameters") or {}).get("id", None)
    body = event.get("body", {})

    functions = {
        "GET": {
            "/execution/{id}": detail,
            "/execution": list,
        },
        "POST": {
            "/execution": create,
        },
        "DELETE": {
            "/execution/{id}": delete,
        },
        "PATCH": {
            "/execution/{id}": update,
        },
    }

    handler = functions.get(method, {}).get(resource)

    return handler(key=key, body=body)


def detail(key, *args, **kwargs):
    """Describes a entry"""

    table = Table("REGISTRY_TABLE_NAME")

    response = Response(200, table.get(key))

    return response.parse()


def list(*args, **kwargs):
    """Lists all entries"""
    pass


def delete(key, *args, **kwargs):
    """Deletes a entry"""
    pass


def update(key, body, *args, **kwargs):
    """Updates (patches) a entry"""
    pass


def create(body, *args, **kwargs):
    """Creates a entry"""

    table = Table("JOBS_TABLE_NAME")
    registry = Table("REGISTRY_TABLE_NAME")
    client = boto3.client("ecs")

    # Parses the body
    body = json.loads(body)

    # Generates a uuid and updates the table
    id = uuid.uuid4().hex
    table.update(id, {"status": "RECEIVED"})

    # Gets the task definition from the registry
    image = registry.get(body["image"])

    # Image not built yet
    if image is None:

        return Response(404, "Image does not exists.").parse()

    elif image["status"] != "SUCCEEDED":

        return Response(409, "Image is not built yet.").parse()

    # Default parameters
    parameters = {
        "cpu": body.get("cpu", image["definition"]["cpu"]),
        "memory": body.get("memory", image["definition"]["memory"]),
        "count": body.get("count", 1),
        "role": body.get("role", image["definition"]["roles"]["task"]),
        "environment": body.get("environment", []),
    }

    response = client.run_task(
        cluster="harbour",
        count=parameters["count"],
        launchType="FARGATE",
        group=id,
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": [
                    "subnet-00f960fed27512fc7",
                    "subnet-029e4362fc65caf73",
                    "subnet-01b6fb88abc34f050",
                ],
                "securityGroups": [
                    "sg-0fec3abb27c2d3dec",
                ],
                "assignPublicIp": "DISABLED",
            }
        },
        overrides={
            "containerOverrides": [
                {
                    "name": "task",
                    "environment": [
                        {
                            "name": name,
                            "value": value,
                        }
                        for name, value in parameters["environment"].items()
                    ],
                    "cpu": int(parameters["cpu"]),
                    "memory": int(parameters["memory"]),
                    "memoryReservation": int(parameters["memory"]) - 50,
                },
            ],
            "cpu": parameters["cpu"],
            "memory": parameters["memory"],
            "taskRoleArn": parameters["role"],
        },
        startedBy="harbour:api",
        tags=[
            {"key": "database", "value": parameters["environment"]["DATABASE"]},
            {"key": "table", "value": parameters["environment"]["TABLE"]},
            {"key": "Name", "value":  "Dump." + parameters["environment"]["DATABASE"] + "." + parameters["environment"]["TABLE"]},
        ],
        taskDefinition=image["definition"]["arn"],
    )

    event = {
        "tasks": [
            {
                "id": None,
                "az": task["availabilityZone"],
                "placement": {
                    "availability_zone": task["availabilityZone"],
                },
                "attachments": task["attachments"],
                "cluster": {
                    "arn": task["clusterArn"],
                },
                "containers": [
                    {
                        "name": container["name"],
                        "arn": container["containerArn"],
                        "task": {
                            "arn": container["taskArn"],
                        },
                        "image": container["image"],
                        "cpu": int(container["cpu"]),
                        "memory_reservation": int(container["memoryReservation"]),
                    }
                    for container in task["containers"]
                ],
                "created_at": task["createdAt"],
                "group": task["group"],
                "launch_type": task["launchType"],
                "memory": int(task["memory"]),
                "cpu": int(task["cpu"]),
                "overrides": task["overrides"],
                "platform_version": task["platformVersion"],
                "started_by": task["startedBy"],
                "tags": task["tags"],
                "arn": task["taskArn"],
                "definition": task["taskDefinitionArn"],
            }
            for task in response["tasks"]
        ]
    }

    event["failures"] = response["failures"]

    table.update(id, event)

    response = Response(200, event)

    return response.parse()
