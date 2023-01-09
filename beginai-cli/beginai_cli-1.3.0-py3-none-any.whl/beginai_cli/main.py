import typer
import beginai as bg
from uuid import UUID
from rich import print

app = typer.Typer()

CREATED_AT_HELP_TEXT = "Name of the column which represents the 'created at' timestamp of the object. Defaults to batch process timestamp when not provided."


@app.command(name="process_user_data")
def process_user_data(app_id: UUID = typer.Option(...),
                      license_key: str = typer.Option(...),
                      csv_file_location: str = typer.Option(...),
                      column_representing_user_id: str = typer.Option(...),
                      column_representing_label: str = None,
                      column_representing_created_at: str = typer.Option(
                          None, CREATED_AT_HELP_TEXT),
                      file_separator: str = ',',
                      host: str = None):

    try:
        embeddings_applier = bg.AlgorithmsApplier(
            str(app_id), license_key, host)
        embeddings_applier.load_user_data(filename=csv_file_location,
                                          unique_identifier_column=column_representing_user_id,
                                          label_column=column_representing_label,
                                          created_at_column=column_representing_created_at,
                                          file_separator=file_separator)
        embeddings_applier.learn_from_data()
    except Exception as e:
        print("An error ocurred while processing the information", e)


@app.command(name="process_object_data")
def process_object_data(app_id: UUID = typer.Option(...),
                        license_key: str = typer.Option(...),
                        csv_file_location: str = typer.Option(...),
                        object_name: str = typer.Option(...),
                        column_representing_object_id: str = typer.Option(...),
                        column_representing_label: str = None,
                        column_representing_created_at: str = typer.Option(
                            None, help=CREATED_AT_HELP_TEXT),
                        file_separator: str = ',',
                        host: str = None):

    try:
        embeddings_applier = bg.AlgorithmsApplier(
            str(app_id), license_key, host)
        embeddings_applier.load_object_data(filename=csv_file_location,
                                            object_name=object_name,
                                            unique_identifier_column=column_representing_object_id,
                                            label_column=column_representing_label,
                                            created_at_column=column_representing_created_at,
                                            file_separator=file_separator)
        embeddings_applier.learn_from_data()
    except Exception as e:
        print("An error ocurred while processing the information", e)


@app.command(name="process_interactions")
def process_interactions(app_id: UUID = typer.Option(...),
                         license_key: str = typer.Option(...),
                         csv_file_location: str = typer.Option(...),
                         column_representing_user_id: str = typer.Option(...),
                         object_name: str = typer.Option(...),
                         column_representing_object_id: str = typer.Option(
                             ...),
                         column_representing_action: str = typer.Option(...),
                         column_representing_created_at: str = typer.Option(
                             None, help=CREATED_AT_HELP_TEXT),
                         file_separator: str = ',',
                         host: str = None):

    try:
        embeddings_applier = bg.AlgorithmsApplier(
            str(app_id), license_key, host)
        embeddings_applier.load_interactions(filename=csv_file_location,
                                             unique_identifier_column=column_representing_user_id,
                                             target_object_name=object_name,
                                             target_unique_identifier_column=column_representing_object_id,
                                             interaction_column_name=column_representing_action,
                                             created_at_column=column_representing_created_at,
                                             file_separator=file_separator)
        embeddings_applier.learn_from_data()
    except Exception as e:
        print("An error ocurred while processing the information", e)


if __name__ == "__main__":
    app()
