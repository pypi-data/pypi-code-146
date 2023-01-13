from convoc import csv2dir

# csv file to be read
read_filepath = 'csv/sample.csv'

# Convert directory from csv
csv_contents = csv2dir(csvfile=read_filepath, level=2, target_path="target", is_header=True)

# loaded csv file (type: list)
print(csv_contents)