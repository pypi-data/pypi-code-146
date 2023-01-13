"""This module provides the CLI."""
# cli-module/cli.py
import json
from typing import List, Optional
import typer
from polygon import rest_connect
app = typer.Typer()


@app.command()
def list():
    typer.echo(f"list")
    #call the endpoint to get list of datasets in account
    #rest-connect with the json
    datasetList=rest_connect.dataset_list()
    print(json.dumps(datasetList, indent=3))

@app.command()
def create(name:str = typer.Option("None","--name","--n"),
    classname: str = typer.Option("","--classname",),
    clodustoragename: str = typer.Option("None","--clodustoragename","--n"),
) -> None:
    classes=[]
    classnames = classname.strip()
    classnames_list = classnames.split(",")
    if (len(classnames_list) > 0):
        for i in range(len(classnames_list)):
            classes.append(classnames_list[i])
    else:
        classes.append(classname)
    #print(classnames_list)
    createDataset = rest_connect.createDataset(name, classnames_list, clodustoragename)
    print(createDataset)

#list_datasetname_or_id
@app.command()
def merge(name:str = typer.Option("None","--name","--n"),
    datasetid: str = typer.Option("","--datasetid",),
    datasetname: str = typer.Option("","--datasetname",),
) -> None:
    typer.secho(
        f"""polygon: dataset merge """
        f"""pass in a list of datasetnames or dataset ids""",
        fg=typer.colors.GREEN,
    )
    dataset_id_list=[]
    dataset_name_list=[]
    print(datasetid)
    dataset_id = datasetid.strip()
    dataset_idlist = dataset_id.split(",")
    if (len(dataset_idlist) > 0):
        for i in range(len(dataset_idlist)):
            dataset_id_list.append(dataset_idlist[i])
    else:
        dataset_id_list.append(datasetid)

    dataset_name = datasetname.strip()
    dataset_namelist = dataset_name.split(",")
    if (len(dataset_namelist) > 0):
        for i in range(len(dataset_namelist)):
            dataset_name_list.append(dataset_namelist[i])
    else:
        dataset_name_list.append(datasetname)

    datasetDetails = rest_connect.dataset_merge(dataset_id_list,dataset_name_list, name)
    print(datasetDetails)
    #get the list - the options can be -ids or -names
    # if -ids the list has datasetids -names then the list has datasetnames
    # based on the options get the list and use them to merge the dataset
    #create proper json and call the endpoint to merge dataset


@app.command()
def download(name:str = typer.Option("None","--name","--n"),
    filters: str = typer.Option("","--filters",),
    format: str = typer.Option("","--format",),
    datasetid: str = typer.Option("","--datasetid",),
    datasetname: str = typer.Option("","--datasetname",),
) -> None:
    typer.secho(
        f"""polygon: dataset download """
        f"""pass in a list of datasetnames or dataset ids""",
        fg=typer.colors.GREEN,
    )

    #print(filters)
    filters_list = []
    filters1=filters.strip()
    filter=filters1.split(",")
    if(len(filter)>0):
        for i in range(len(filter)):
            filters_list.append(filter[i])
    else:
        filters_list.append(filters)

    #print(filters_list)

    for id in filters:
        filters_list.append(id)

    if(datasetid =="" and datasetname==""):
        print("Please pass dataset Id or dataset name to download")
    else:
        datasetDownload = rest_connect.dataset_download(datasetid,datasetname, filters_list,format)


@app.command()
def delete(name: str = typer.Option("None","--name"),id: str = typer.Option("None","--id",),)-> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon: dataset delete """
        f"""pass datasetname or dataset id""",
        fg=typer.colors.GREEN,
    )
    deletestatus = rest_connect.dataset_delete(name, id)
    print(deletestatus)
    # the options can be -id or -name
    # based on the options take the input and
    #create proper json and call the endpoint to merge dataset

@app.command()
def details(name: str = typer.Option("None","--name"),id: str = typer.Option("None","--id",),)-> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon: dataset details """
        f"""pass datasetname or dataset id""",
        fg=typer.colors.GREEN,
    )
    datasetDetails=rest_connect.dataset_details(name,id)
    print(json.dumps(datasetDetails, indent=3))

    # the options can be -id or -name
    # based on the options take the input and
    #create proper json and call the endpoint to merge dataset


@app.command()
def version(name:str = typer.Option("None","--name","--n"),
    filters: str =  typer.Option("","--filters",),
    datasetid: str = typer.Option("","--datasetid",),
    datasetname: str = typer.Option("","--datasetname",),
) -> None:
    typer.secho(
        f"""polygon: dataset version """
        f"""pass datasetname or dataset id and list of filters to apply""",
        fg=typer.colors.GREEN,
    )

    filters_list = []
    if(filters!=""):
        #filters1=filters.strip()
        filter=filters.split(",")
        if(len(filter)>0):
            for i in range(len(filter)):
                filters_list.append(filter[i])

    if(len(filters_list)==0):
        print("Please pass the filters to apply")
    elif(datasetid=="" and datasetname==""):
        print("Please pass dataset name or dataset id to create version")
    elif (name == ""):
        print("Please pass version name to create")
    else:
        response=rest_connect.dataset_version(datasetid,datasetname,filters_list,name)
        print(response)


if __name__ == "__main__":
    app()



# list_datasetname_or_id: List[str] = typer.Argument(...),
# priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
