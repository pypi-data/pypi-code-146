from datetime import datetime
import re
import argparse


def build_report(start_log_file, end_log_file, sort=None):
    """
    Build a report based on data from start and end log files.

    :param start_log_file: (str) the path to the start log file.
    :param end_log_file: (str) the path to the end log file.
    :param sort: (str, optional) the order in which the report should be sorted.
                 Accepted values 'desc'.  The default value is 'asc'
    :return: A dictionary containing the race results.
        In the format {driver_abbreviation: race_time}.
    """
    start_log = {}
    end_log = {}
    race_result = {}
    with open(start_log_file, 'r') as f:
        for line in f.readlines():
            key, value = re.findall(r"(.+?\D)(\d.+)", line.strip())[0]
            start_log[key] = value
    with open(end_log_file, 'r') as f:
        for line in f.readlines():
            key, value = re.findall(r"(.+?\D)(\d.+)", line.strip())[0]
            end_log[key] = value
    for key in start_log:
        start_time = datetime.strptime(start_log[key], '%Y-%m-%d_%H:%M:%S.%f')
        end_time = datetime.strptime(end_log[key], '%Y-%m-%d_%H:%M:%S.%f')
        result_time = abs(end_time - start_time)
        seconds_time = result_time.total_seconds()
        result_str = datetime.utcfromtimestamp(seconds_time).strftime('%M:%S.%f')
        race_result[key] = result_str.strip('0')
        if sort == 'desc':
            race_result = dict(sorted(race_result.items(), key=lambda item: item[1], reverse=True))
        else:
            race_result = dict(sorted(race_result.items(), key=lambda item: item[1]))

    return race_result


def print_report(abbreviations_file, build_result, driver_name=None):
    """
    Print report of a race or specific driver.

    :param abbreviations_file: (srt) the path to the file with the driver abbreviation data.
    :param build_result: (dict) dictionary with data on race results, with driver abbreviations
                        as key and race time as value.
    :param driver_name: (srt, optional) parameter to specify a specific driver for print race data.
    :return: - None
    """
    abbreviations = {}
    dict_result = {}
    with open(abbreviations_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            key, value = line.strip().split('_', 1)
            abbreviations[key] = value
    for key in build_result:
        result = build_result[key]
        driver_team = abbreviations[key]
        driver, team = driver_team.split('_')
        if driver_name is None or driver_name == driver:
            dict_result[driver] = (team, result)
    if driver_name is None:
        driver_place = 0
        for driver, data in dict_result.items():
            driver_place += 1
            team, result = data
            if driver_place == 16:
                print('-' * 60)
            print(f"{driver:<20} | {team:<25} | {result}")
    else:
        team, result = dict_result[driver_name]
        print(f"{driver_name:<20} | {team:<25} | {result}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', required=True, help='folder containing the data files')
    parser.add_argument('--driver', type=str, help='name of the driver')
    parser.add_argument('--asc', action='store_true', help='sort results in ascending order')
    parser.add_argument('--desc', action='store_true', help='sort results in descending order')
    args = parser.parse_args()

    folder_path = args.files
    driver_name = args.driver
    start_log_file = f'{folder_path}/start.log'
    end_log_file = f'{folder_path}/end.log'
    abbreviations_file = f'{folder_path}/abbreviations.txt'
    sorted_asc = build_report(start_log_file, end_log_file)
    if args.driver:
        print_report(abbreviations_file, sorted_asc, driver_name)
    elif args.desc:
        sorted_desc = build_report(start_log_file, end_log_file, sort='desc')
        print_report(abbreviations_file, sorted_desc)
    else:
        print_report(abbreviations_file, sorted_asc)


if __name__ == '__main__':
    main()
