import statsu
import pandas as pd
import argparse



def get_sample_data(id: int):
    data = None
    if id == 1:
        data = pd.DataFrame([
            [1, 3, 5, 7, 9],
            [62, 32, 57, 16, 3],
            [21, 29, 10, 43, 57],
        ])

    elif id == 2:
        data = pd.DataFrame([
            [1, 3, '52', 7, -91],
            [62, 'Agent', 57, 16, 3],
            ['21a', 29, 10, 3.212, 57],
            [26.921, 102, 19, 3.212, -232],
        ])

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Statsu Pandas Editor')
    parser.add_argument(
        '--demo', 
        type=int,
        help='Open with sample data (Number: Sample Data ID)'
    )

    args = parser.parse_args()
    sample_data = get_sample_data(args.demo)

    statsu.show(sample_data)
