"""CSV Generator"""
from typing import Optional
import csv
import faker
from datasets_genie.utils import generate_file_name, get_file_location
from datasets_genie.faker_utils import callable_methods, random_faker_method

fake = faker.Faker()


def generate_data(rows: int, columns: int) -> list[list[str]]:
    """Generates data for the CSV file"""
    keys = []
    for _ in range(columns):
        keys.append(random_faker_method())
    data = [keys]
    for _ in range(rows):
        data.append(callable_methods(keys))
    return data


def generate_csv(rows: int,
                 columns: int,
                 *,
                 file_location: Optional[str] = None,
                 file_name: Optional[str] = None,
                 preview: bool = False,
                 stream: bool = False,
                 ):
    """returns a csv file"""
    data = generate_data(rows, columns)

    # safe check on file location
    file_location = get_file_location(location=file_location)

    # safe check on file name
    file_name = generate_file_name(file_name=file_name, file_type='csv')

    if preview:
        counter = 0
        for row in data:
            print(row)
            counter += 1
            if counter == 5:
                break
    elif stream:
        # handle data stream
        pass
    else:
        full_file_name = f'{file_location}/{file_name}'
        try:
            with open(full_file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
        except FileNotFoundError as file_not_found_error:
            raise ValueError(f'Error: {full_file_name} does not exist') \
                from file_not_found_error
        except PermissionError as permission_error:
            raise ValueError(f'Error: Insufficient permission to write to'
                             f' {full_file_name}') from permission_error
        except IOError as io_error:
            raise ValueError(f'Error: I/O error occurred when writing to'
                             f' {full_file_name}') from io_error


def data_stream(data):
    """generator function that yields one row at a time"""
    for row in data:
        yield row
