import csv

import modbus_connect.utils as utils


# Get variable names and memory addresses from csv file, and save them in a list of dictionaries
def load_tags_from_list(
    directory: str,
    filename: str,
    name_row: int,
    address_row: int,
    memory_row: int,
    datatype_row: int,
) -> list[utils.ModbusRegister]:
    tags = []
    try:
        with open(directory + filename, "r") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader, None)  # Skip header
            for row in reader:
                tags.append(
                    {
                        "name": row[name_row],
                        "address": int(row[address_row]),
                        "memory": row[memory_row],
                        "datatype": row[datatype_row],
                    }
                )
        return tags
    except Exception as e:
        raise ("Some problem has occurred while reading the file: " + str(e))
