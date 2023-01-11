import csv
from pathlib import Path


class CSVLogger:

    def __init__(self, csvLogFilePath: str):
        self.csvLogFilePath = csvLogFilePath

    def cleanCsv(self):
        if Path(self.csvLogFilePath).exists():
            Path(self.csvLogFilePath).unlink()

    def addCsvRow(self, row: dict):
        parent = Path(self.csvLogFilePath).parent
        if not parent.exists():
            Path(parent).mkdir(parents=True, exist_ok=True)

        if not Path(self.csvLogFilePath).exists():
            csvFileHanlder = open(self.csvLogFilePath, "w+", newline="")
            writer = csv.writer(csvFileHanlder)
            writer.writerow(row.keys())
        else:
            csvFileHanlder = open(self.csvLogFilePath, "a+", newline="")
            writer = csv.writer(csvFileHanlder)

        writer.writerow(row.values())
        csvFileHanlder.close()

    def getRowsReader(self, reader, removeHeader=True):
        try:
            with open(self.csvLogFilePath, "r", newline="") as csv_file:
                rows = list(reader(csv_file))
                # remove header
                if removeHeader and len(rows) > 0:
                    rows.pop(0)
        except FileNotFoundError:
            rows = []
        return rows

    def getRowsAsDict(self):
        return self.getRowsReader(csv.DictReader, removeHeader=False)

    def getRowsAsList(self):
        return self.getRowsReader(csv.reader)

    def getLastRow(self):
        rows = self.getRows()
        return rows[-1]
