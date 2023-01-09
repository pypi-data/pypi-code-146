import csv


def load_csv_into_dict(filename):
    """Load a CSV file into a dictionary on first columns are the keys and the second the values,
    all values ar integers"""
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        return {int(row[0]): int(row[1]) for row in reader}


if __name__ == '__main__':
    print(load_csv_into_dict('../data/hi_res_ramp_codes.csv'))
