"""This module provides the CLI."""
# cli-module/cli.py
import json
from pathlib import Path
from typing import List, Optional
import sqlparse
import typer
from polygon import __app_name__, __version__, dataset, container,search
from polygon import rest_connect
from polygon import cmdprompt
# import dataset
# import container
from polygon import rest_connect
app = typer.Typer()
app.add_typer(dataset.app, name="dataset")
app.add_typer(container.app, name="container")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()

def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def list(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon-cli: list """
        f"""with priority: {priority}""",
        fg=typer.colors.GREEN,
    )

@app.command()
def query()-> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon: search  results """
        f"""pass phrase to search""",
        fg=typer.colors.GREEN,

    )
    cmdprompt.PolygonShell().cmdloop()
@app.command()
def search(phrase: str = typer.Option("None","--phrase",),
           sql: str = typer.Option("None","--sql",),)-> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon: search  results """
        f"""pass phrase to search""",
        fg=typer.colors.GREEN,
    )
    if(phrase !="None"):
        searchResult=rest_connect.search_details(phrase)
        print(searchResult)
    else:
        parsedSql=pharsesql(sql)
        searchResult = rest_connect.search_details(phrase,parsedSql)
        print(json.dumps(searchResult, indent=3))

@app.command()
def adduser(name: str = typer.Option("None","--name"),
            email: str = typer.Option("None","--email",),
            password: str = typer.Option("None","--password",),
            role: str = typer.Option("None","--role",),)-> None:
    """Example :\n
        --add user : polygon adduser  --name="<name of the user>" --email="<email of the user>" --password="<set the password to login>" --role="<assign role admin  or dataset to user>"\n
            """
    typer.secho(
        f"""polygon: adduser """
        f"""pass name,email,password,role  to add the user""",
        fg=typer.colors.GREEN,
    )
    addserdetails = rest_connect.add_user(name, email,password,role)
    print(addserdetails)

@app.command()
def edituser(email: str = typer.Option("None","--email",),
            role: str = typer.Option("None","--role",),)-> None:
    """Example :\n
        --edit user: polygon edituser --email="<email of the user>" --role="<assign role admin  or dataset to user>"\n
            """
    typer.secho(
        f"""polygon: edituser """
        f"""pass email,role  to edit the user""",
        fg=typer.colors.GREEN,
    )
    edituserdetails = rest_connect.edit_user(email,role)
    print(edituserdetails)

@app.command()
def getusers()-> None:
    """Example :\n
        --get users : polygon getsers
            """
    typer.secho(
        f"""polygon: getsers """
        f"""Get users in the account""",
        fg=typer.colors.GREEN,
    )
    getserdetails = rest_connect.get_users()
    print(getserdetails)

@app.command()
def deleteuser(email: str = typer.Option("","--email",),)-> None:
    """Example :\n
        --add user : polygon deleteuser  --email "<name of the user>" --email="<List of email id to delete>"  \n
            """
    typer.secho(
        f"""polygon: deleteuser """
        f"""pass list of email  to delete the user""",
        fg=typer.colors.GREEN,
    )
    users = []
    emails = email.strip()
    emailslist = emails.split(",")
    if (len(emailslist) > 0):
        for i in range(len(emailslist)):
            users.append(emailslist[i])
    else:
        users.append(emails)

    deleteusers = rest_connect.delete_user(users)
    print(deleteusers)

@app.command()
def assigndataset( email: str = typer.Option("None","--email",),
            datasetid:  str= typer.Option("","--datasetid",),)-> None:
    """Example :\n
        -- assigndataset : polygon assigndataset --email="<email of the user>" --datasetid "<List of dataset id to assign>"  \n
    """
    typer.secho(
        f"""polygon: assigndataset """
        f"""pass email, list of datasetid  to assign """,
        fg=typer.colors.GREEN,
    )
    datasets = []
    dataset_id = datasetid.strip()
    dataset_idlist = dataset_id.split(",")
    if (len(dataset_idlist) > 0):
        for i in range(len(dataset_idlist)):
            datasets.append(dataset_idlist[i])
    else:
        datasets.append(datasetid)

    assigndatasetdetails = rest_connect.assign_dataset(email, datasets)
    print(assigndatasetdetails)

def pharsesql(sql):
    statements = sqlparse.split(sql)
    #print(statements)
    # statements
    # ['select * from foo;', 'select * from bar;']

    # Format the first statement and print it out:
    first = statements[0]
    #print(sqlparse.format(first, reindent=True, keyword_case='upper'))
    # SELECT *
    # FROM foo;

    # Parsing a SQL statement:
    parsed = sqlparse.parse(first)[0]
    #print(parsed.tokens)
    counter = 0
    for tok in parsed.tokens:
        counter = counter + 1
        #print("counter=" + str(counter))
        # print("token="+str(tok))
        IN_WHERE = False
        input_dict = {}
        if tok.is_group:
            for sub_tok in tok.tokens:
                # print("sub_token=" + str(sub_tok))
                if sub_tok.normalized == 'WHERE':
                    IN_WHERE = True
                if IN_WHERE and sub_tok.is_group:
                    # handle where clause
                    #print("sub_token||" + str(sub_tok))
                    #print("sub_token||" + str(sub_tok.value.replace('=', ':')))
                    # strip quotes out
                    input_dict[sub_tok.left.value] = sub_tok.right.value
                    for sub_sub_tok in sub_tok.tokens:
                        k=0
                        #print("sub_sub_tok=" + str(sub_sub_tok))
                        # pass

    input_json_data = json.dumps(input_dict)
    return input_json_data
# @app.command()
# def dataset(
#     description: List[str] = typer.Argument(...),
#     priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
# ) -> None:
#     """Add a new to-do with a DESCRIPTION."""
#     typer.secho(
#         f"""polygon-cli: list """
#         f"""with priority: {priority}""",
#         fg=typer.colors.GREEN,
#     )



# @app.command()
# def container(
#     description: List[str] = typer.Argument(...),
#     priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
# ) -> None:
#     """Add a new to-do with a DESCRIPTION."""
#     typer.secho(
#         f"""polygon-cli: list """
#         f"""with priority: {priority}""",
#         fg=typer.colors.GREEN,
#     )

