import time

import pandas as pd
import numpy as np
import sys

import pytz
import datetime

class LastEntry:
    distanceTicks: int = 0
    value: any = None


class DataTable():
    def __init__(self, df=None):
        self._df = None
        self._np = np.zeros((0,0), dtype=object)
        self.columns = []
        self.col_chart = {}
        self._np_by_chart = {}
        self._index_by_chart = {}
        self._index_reference_by_chart = {}
        self.index_as_timestamp = []
        self.col = {}
        self.index = []
        if df is not None:
            self.convertDataFrame(df)
        return None

    def to_df(self):
        return pd.DataFrame(self._rows)

    def getDf(self):
        return self._df

    def from_df(self, df: pd.DataFrame):
        self._df = df
        self.convertDataFrame(df)

    def get_cleared_np_from_df(self, chart):

        targetColumn = self._np[self.col[chart+".main:close"],:]
        indexes = pd.isna(targetColumn)

        new_numpy_transposed = None
        for d in self.col_chart[chart]:
            index = self.col_chart[chart][d]
            new_data = np.delete(self._np[self.col[d]], indexes)
            if new_numpy_transposed is None:
                new_numpy_transposed = np.empty([len(self.col_chart[chart]), len(new_data)], dtype=object)
            new_numpy_transposed[index,:] = new_data
        index = np.delete(self.index, indexes)

        i = 0
        index_reference = np.zeros(len(self.index))
        intern_index = -1
        for d in indexes:
            index_reference[i] = intern_index
            if d == False:
                intern_index = intern_index + 1
            i = i + 1


        return {
            "data": new_numpy_transposed,
            "index": index,
            "index_reference": index_reference
        }

    def convertDataFrame(self, df):
        try:
            self._df = df
            self._np = df.to_numpy().transpose()
            self.columns = self._df.columns.to_list()
            index = 0
            for c in self.columns:
                self.col[c] = index
                if c.startswith("chart"):
                    chart = c.split(".")[0]
                    if chart not in self.col_chart:
                        self.col_chart[chart] = {"datetime": 0}
                    self.col_chart[chart][c] = len(self.col_chart[chart])
                index = index + 1

            self.index = self._df.index.tolist()
            self.index_as_timestamp = []
            for e in self.index:
                if type(e) == pd.Timestamp:
                    self.index_as_timestamp.append(int(time.mktime(e.timetuple()) / 60) * 60)
                else:
                    self.index_as_timestamp.append(e)

            for chart in self.col_chart:
                try:
                    data = self.get_cleared_np_from_df(chart)
                    self._np_by_chart[chart] = data["data"]
                    self._index_by_chart[chart] = data["index"]
                    self._index_reference_by_chart[chart] = data["index_reference"]
                except Exception as e:
                    print("error in generating the speedup datatbles")

        except Exception as e:
            print("Error while converting dataframe ", e)

    def rows(self):
        return self._np.transpose()

    def asArray(self):
        return self._np.transpose()[:,0]

    def subTable(self, index=0, length=None, columns=None):
        sub = DataTable()
        sub._df = self._df
        sub.columns = self.columns
        sub.col = self.col
        if length is None:
            length = len(self.index)
        sub.index = self.index[index:index + length]

        if columns is not None:
            sub.columns = columns
            list = []
            index = 0
            cols = {}
            for c in columns:
                list.append(self._np[self.col[c], index:index + length])
                cols[c] = index
                index = index + 1
            sub._np = np.array(list)
            sub.col = cols
        else:
            sub._np = self._np[:, index:index + length]
            sub.col_chart = self.col_chart
            for chart in self.col_chart:
                convertedIndex = int(self._index_reference_by_chart[chart][index + length])
                sub._index_by_chart = self._index_reference_by_chart
                sub._np_by_chart[chart] = self._np_by_chart[chart][:, (convertedIndex-length if convertedIndex-length > 0 else 0):convertedIndex]

        return sub

    def setColumn(self, name, data, index=None, pad=True, type=float):
        ## padding needed maybe

        length = len(self.index)
        if length <= 0 and len(data) > 0:
            if isinstance(data, pd.Series):
                self.index = data.index
            else:
                self.index = range(len(data))

        if name not in self.col:
            columnIndex = len(self.col.keys())
            self.col[name] = columnIndex
            length = len(self.index)
            a = np.zeros(length, dtype=object)
            a[:] = np.nan
            newlist = []
            for i in range(len(self.col)-1):
                newlist.append(self._np[i])
            newlist.append(a)
            self._np = np.array(newlist)
            self.columns.append(name)


        length = len(self.index)
        if isinstance(data, (int, float)):
            narr = np.zeros(self.length())
            narr[:] = np.array(data)
            data = narr
        if len(data) < length:
            data = np.pad(np.array(data, dtype=type), (length-len(data),0), 'constant', constant_values=np.nan)

        try:
            self._np[self.col[name]] = data
        except Exception as e:
            pass


    def length(self):
        return len(self.index)

    def hasIndex(self, date):
        target_date_in_min = int(time.mktime(date.timetuple()) / 60) * 60
        if target_date_in_min in self.index_as_timestamp:
            return True
        return False

    def addRow(self, row):
        date = row["datetime"]

        for col in row:
            if col not in self.col:
                self.col[col] = len(self.col.keys())

        correct_object = []
        for col in row:
            ele = row[col]
            if col == "datetime":
                ele = row[col].replace(tzinfo=pytz.utc)
            correct_object.append(ele)

        if self.length() <= 0:
            self._np = np.array([correct_object])
        else:
            self._np = np.concatenate((self._np, [correct_object]), axis=1)

        self.index.append(date)
        self.index_as_timestamp.append(int(time.mktime(date.timetuple()) / 60) * 60)


    def getColumns(self, names):
        return self._np[[self.col[name] for name in names]]

    def getLastEntry(self, name, maxLength=100) -> LastEntry:
        row = self.getColumn(name)
        length = 0
        if row is not None:
            for i, e in enumerate(reversed(row)):
                length = length + 1
                if length > maxLength:
                    return None
                if e is not None:
                    if "Timestamp" in str(type(e)):
                        le = LastEntry()
                        le.value = e.to_pydatetime()
                        le.distanceTicks = length
                        return le
                    if not np.isnan(e):
                        le = LastEntry()
                        le.value = e
                        le.distanceTicks = length
                        return le
            return None
        return None

    def getLast(self, name, maxLength=100):
        row = self.getColumn(name)
        if row is False:
            return False
        length = 0
        if row is not None:
            for i, e in enumerate(reversed(row)):
                length = length + 1
                if length > maxLength:
                    return None
                if e is not None:
                    if "Timestamp" in str(type(e)):
                        return e.to_pydatetime()
                    if not np.isnan(e):
                        return e
            return None
        return None

    def getColumn(self, name, index=None, limit=None, with_dates=False,
                  clear_nan=True, to_date=None, from_date=None):
        data = None
        datetimes = None
        if name not in self.col:
            return False

        chart = name.split(".")[0]
        if chart in self.col_chart and name in self.col_chart[chart]:
            targetColumn = self._np_by_chart[chart][self.col_chart[chart][name]]
        else:
            targetColumn = self._np[self.col[name]]
        indexColumn = self.index

        if to_date:
            indexColumn = [date for date in indexColumn if date < to_date]
            targetColumn = targetColumn[0:len(indexColumn)]


        if clear_nan and data is not None:
            #i = np.argwhere(pd.isna(data))
            idx = 0
            for e in data:
                if not np.isnan(e):
                    break
                idx = idx + 1
            data = data[idx:]
            datetimes = datetimes[idx:]
            #datetimes = np.delete(datetimes, i)

        if index is not None:
            data = targetColumn[index]
            datetimes = indexColumn[index]

        if limit is not None and data is None:
            data = targetColumn[-limit:]
            datetimes = indexColumn[-limit:]


        if data is None:
            data = targetColumn
            datetimes = indexColumn


        if with_dates:
            return {"data": data, "datetime": datetimes}

        return data

    def getColumnNames(self):
        return self.col.keys()

    def column(self, name, index=None, limit=None, with_dates=False, clear_nan=False, to_date=None, from_date=None):
        return self.getColumn(name, index, limit=limit, with_dates=with_dates,
                              clear_nan=clear_nan, to_date=to_date, from_date=from_date)

    def lastElement(self, column):
        return self.row(-1)[self.col[column]]

    def lastRow(self, column=None):
        if column is not None:
            return self.lastElement(column)
        r = self.row(-1)
        d = {}
        i = 0
        for s in self.columns:
            d[s] = r[i]
            i = i +1
        return d

    def row(self, row):
        return self._np[:, row]
