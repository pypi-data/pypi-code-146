####
##
#
#

import os
import sys
import csv
import deta
import fire
import src.cli as this

DETA_PROJECT_KEY = os.getenv("DETA_PROJECT_KEY", None)


class DetaCsv:
    def __init__(self):
        scriptname = os.path.basename(sys.argv[0]).rsplit(".", 1)[0]
        print(scriptname, "version", this.__version__)
        if len(sys.argv) == 1:
            print(f"type `{scriptname} --help` for more info")
            sys.exit()
        pass

    def upload(
        self,
        filename: str,
        dbname: str = None,
        project: str = DETA_PROJECT_KEY,
        key: str = "key",
        encoding: str = "UTF-8",
        asynct: bool = False,
        verbose: bool = False,
    ):
        """
        Read csv file and upload data to your deta project database

        PATH_TO_CSV_FILE : str
        DETA_DB_NAME : str
        DETA_PROJECT_KEY : str
        CSV_FILE_ENCODING : str
        ASYNCHRONOUS_TRANSFER_FLAG : any

        :param str filename: The path (absolute or relative) to the source CSV data file
        :param str dbname: The name of your Deta Base, default filename(PATH_TO_CSV_FILE)
        :param str project: The `project key` of your Deta Base instance, default DETA_PROJECT_KEY environment variable
        :param str key: - unused yet - The name for `key` field (like ID field in RDB) to store the data under
        :param str encoding: CSV file encoding, default UTF-8
        :param str asynct: unused
        :return: None
        """

        dbname = dbname or os.path.basename(filename).rsplit(".", 1)[0]

        print(f"* Open detabase `{dbname}`")
        db = (deta.Deta(project)).Base(dbname)

        print(f"* Reading CSV from `{filename}`")
        with open(filename, mode="rt", encoding=encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            count = 0

            while True:
                items = []
                c = 0
                for csv_row in csv_reader:
                    items.append(csv_row)
                    c += 1
                    if 25 == c:
                        break
                if not items:
                    break
                res = db.put_many(items)
                count += c
                not verbose or print(f"* Uploaded {c} rows, total {count}")

            print(f"Succesfully uploaded {count} rows to `{dbname}` Deta Base")

        return

    def download(
        self,
        dbname: str,
        filename: str = None,
        project: str = DETA_PROJECT_KEY,
        key: str = "key",
        encoding: str = "UTF-8",
        asynct: bool = False,
        verbose: bool = False,
    ):
        """
        Read your Deta Base and save content to CSV file

        DETA_DB_NAME : str
        PATH_TO_CSV_FILE : str
        DETA_PROJECT_KEY : str
        CSV_FILE_ENCODING : str
        ASYNCHRONOUS_TRANSFER_FLAG : any

        :param str dbname: The name of your Deta Base
        :param str filename: The path to the target CSV file, default `DETA_DB_NAME.csv`
        :param str project: The `project key` of your Deta Base instance, default DETA_PROJECT_KEY environment variable
        :param str key: - unused yet - The name for `key` field (like ID field in RDB) to store the data under
        :param str encoding: CSV file encoding, default UTF-8
        :param str asynct: unused
        :return: None
        """

        dbname = str(dbname)
        filename = (
            os.path.abspath(filename)
            if filename
            else os.path.abspath(os.curdir) + os.sep + dbname + '.csv'
        )

        print(f"* Open detabase `{dbname}`")
        db = (deta.Deta(project)).Base(dbname)
        res = db.fetch(query=None, limit=1, last=None)
        fieldnames = list(res.items[0].keys())

        print(f"* Writing CSV to `{filename}`")
        with open(filename, mode="xt", encoding=encoding) as csv_file:
            count = 0
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            res = db.fetch(query=None, limit=1000, last=None)
            while True:
                items = res.items
                csv_writer.writerows(items)

                # for item in items:
                #    csv_writer.writerow(list(item))

                count += len(items)
                not verbose or print(f"* Last uploaded key `{res.last}`")
                if res.last:
                    res = db.fetch(query=None, limit=1000, last=res.last)
                else:
                    break

            print(f"Succesfully saved {count} rows to `{filename}`")

        return
