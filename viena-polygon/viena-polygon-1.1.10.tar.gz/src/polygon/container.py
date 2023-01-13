"""This module provides the CLI."""
# cli-module/cli.py
import json
from typing import List, Optional
from polygon import rest_connect

import typer

app = typer.Typer()


@app.command()
def list():
    typer.echo(f"list")
    #call the endpoint to get list of clod containers
    #rest-connect with the json
    containerList=rest_connect.containerList()
    print(json.dumps(containerList, indent=3))


@app.command()
def add(cloudstoragename:str = typer.Option("None","--cloudstoragename","--n"),
    cloudtype: str = typer.Option("None","--cloudtype",),
    authentication: str = typer.Option("None","--authentication",),
    containername: str = typer.Option("None","--containername",),
    bucketname: str = typer.Option("None","--bucketname",),
    accontname: str = typer.Option("None","--accontname",),
    accesskey: str = typer.Option("None","--accesskey",),
    secretid: str = typer.Option("None","--secretid",),
    sastoken: str = typer.Option("None","--sastoken",),
    manifestjson: str = typer.Option("None","--manifestjson",),
    region: str = typer.Option("None","--region",),
) -> None:

    if (cloudtype == "aws_s3" and authentication == "account_authentication"):
        if (bucketname == "None" or accesskey == "None" or secretid == "None" or region == "None"):
            print("Please provide proper cloud details'")
        else:
            dataseDetails=rest_connect.createContainer(cloudstoragename,cloudtype,authentication,containername,bucketname,
                                                   accontname,accesskey,secretid,sastoken,manifestjson,region)
            print(dataseDetails)
    if (cloudtype == "aws_s3" and authentication == "annonymous_access"):
        if (bucketname == "None" or manifestjson == "None" or region == "None"):
            print("Please provide proper cloud details'")
        else:
            dataseDetails = rest_connect.createContainer(cloudstoragename, cloudtype, authentication, containername,
                                                       bucketname,
                                                       accontname, accesskey, secretid, sastoken, manifestjson, region)
            print(dataseDetails)
    if (cloudtype == "azure_container" and authentication == "account_authentication"):
        if (containername == "None" or accontname == "None" or sastoken == "None"):
            print("Please provide proper cloud details'")
        else:
            dataseDetails = rest_connect.createContainer(cloudstoragename, cloudtype, authentication, containername,
                                                       bucketname,
                                                       accontname, accesskey, secretid, sastoken, manifestjson, region)
            print(dataseDetails)
    if (cloudtype == "azure_container" and authentication == "annonymous_access"):
        if (containername == "None" or accontname == "None"):
            print("Please provide proper cloud details'")
        else:
            dataseDetails = rest_connect.createContainer(cloudstoragename, cloudtype, authentication, containername,
                                                       bucketname,
                                                       accontname, accesskey, secretid, sastoken, manifestjson, region)
            print(dataseDetails)

@app.command()
def details(cloudstoragename:str = typer.Option("None","--cloudstoragename","--n"),
    cloudstorageid: str = typer.Option("None","--cloudstorageid",),
) -> None:
    datasetDetails = rest_connect.container_details(cloudstoragename, cloudstorageid)
    print(datasetDetails)


@app.command()
def delete(name:str = typer.Option("None","--name","--n"),
    id: str = typer.Option("None","--id",),
) -> None:
    datasetDetails = rest_connect.delete_container(name, id)
    print(datasetDetails)


if __name__ == "__main__":
    app()
