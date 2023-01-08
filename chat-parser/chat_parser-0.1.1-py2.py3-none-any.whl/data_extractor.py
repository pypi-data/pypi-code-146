from datetime import datetime
from .fileparser import FileParser
from .utils import WordTools
import pandas as pd
import re


class OwnerOperator(FileParser):
    """Operating with owner columns table"""
    def __init__(self):
        super().__init__()

    def is_owner_exist(self, name):
        return name in self.frame["owner"].unique()

    def count_owner_words(self, name):
        """Count the words of owner by name"""
        try:
            owner_text = self.frame.groupby("owner").agg(lambda x : list(x)).loc[name]["text"]
        except KeyError:
            return {"message": f"name \"{name}\" not in file" }
        owner_text = [WordTools.text_cleaner(t) for t in owner_text]
        return WordTools.count_word(" ".join(owner_text).split(" "))

    def count_owner_emojis(self,name):
        """Count the emojis of owner by name"""
        owner_text = self.frame.groupby("owner").agg(lambda x : list(x)).loc[name]["text"]
        owner_text = [WordTools.text_cleaner(t) for t in owner_text]
        return WordTools.extract_emojis(" ".join(owner_text))

    def __owner_activities(self, name):
        """return the activities of owner"""
        owner_times = self.frame.groupby("owner").agg(lambda x : list(x)).loc[name]["date"]
        return owner_times

    def owner_activities(self, name):
        """return the dictionary of owner ativities"""
        # print(self.__owner_activities(name))
        return {"activities": [ t.strftime("%Y-%m-%d %H:%M") for t in self.__owner_activities(name)]}

    def count_owner_hours(self,name):
        """Count the owner hourly activities"""
        return WordTools.count_hour(self.__owner_activities(name))

    def count_owner_days(self,name):
        """Count the owner daily activities"""
        return WordTools.count_day(self.__owner_activities(name))


class DateOperator(FileParser):
    """Operating with date columns table"""
    def __init__(self):
        super().__init__()

    def expand_datetime(self):
        """Expands datetime"""
        pass

    def __get_time_by(self, time):
        if len(time) == 4 and time.startswith("20"):
            return "year", int(time)
        elif time.capitalize() in WordTools.months_list():
            return "month", time.capitalize()
        elif time.capitalize() in WordTools.days_list():
            return "day_name", time.capitalize()
        elif time.isdecimal() :
            if int(time) in range(0,32):
                return "day", int(time)
        elif re.match(r"\d{4}-\d{2}-\d{2}", time):
            try:
                time = datetime.strptime(time.split()[0], "%Y-%m-%d")
                time = time.year, WordTools.month_name(time.month), time.day
                return (["year", "month", "day"], time)
            except ValueError:
                pass
        raise ValueError(f"invalid time format for \"{time}\"")

    def __group_frameby(self, time):
        get_by = self.__get_time_by(time)
        by, time = get_by
        # print(get_by)
        try:
            frame = self.frame.groupby(by).agg(lambda x : list(x)).loc[time]
        except KeyError:
            raise KeyError(f"time of {time} doesn\'t exist in chat frame")
        return frame

    def is_time_format_errors(self, time):
        """Error handling if format not available"""
        if not self.__get_time_by(time):
            raise KeyError(f"\"{time}\" is not in available formats: {self._time_format}")

    def is_time_exist(self, time):
        try:
            self.__group_frameby(time)
        except KeyError:
            return False
        return True

    def count_time_owners(self, time):
        """Count owner occurences by specfied time"""
        owners_list = self.__group_frameby(time)["owner"]
        return WordTools.count_word(owners_list)

    def count_time_words(self, time):
        """Count words occurence by specified time"""
        text_by_time = self.__group_frameby(time)["text"]
        text_by_time = [WordTools.text_cleaner(t) for t in text_by_time]
        text_by_time = " ".join(text_by_time).split(" ")
        return WordTools.count_word(text_by_time)

    def count_time_emojis(self,time):
        """Count emojis occurences by specified time"""
        text_by_time = self.__group_frameby(time)["text"]
        text_by_time = " ".join(text_by_time)
        return WordTools.extract_emojis(text_by_time)

    def get_conversations_at(self,time):
        """Get the conversations at specified time"""
        r = self.__group_frameby(time)
        r = r.loc[r.index.isin(self.data_columns)]
        date, owner, text = r.loc["date"], r.loc["owner"], r.loc["text"]
        date = [d.strftime("%Y-%m-%d %H:%m") for d in date]
        data = []
        for i in range(len(date)):
            d = {
                "date": date[i],
                "owner": owner[i],
                "text": text[i]
            }
            data.append(d)
        return {"conversation": data}

class TextOperator(FileParser):
    """Operating with text columns table"""
    def __init__(self):
        pass

    def __filter_frame_by_text(self, text):
        """filter frame by the occurences of specified text"""
        temp_frame = self.frame[self.frame["text"].str.contains(rf"\b{text}\b", case=False)]
        return temp_frame

    def get_text_conversations(self, text):
        """Get conversation with the specified text"""
        return self.row_dict_list(self.__filter_frame_by_text(text))

    def count_text_owners(self, text):
        """Count the owners who had specified text"""
        return self.__filter_frame_by_text(text)["owner"].value_counts().to_dict()

    def __get_text_activities(self, text):
        """Get the date of the specified text"""
        return self.__filter_frame_by_text(text)["date"]

    def get_text_activities(self,text):
        """Get the date of the specified text as dict"""
        return {"activities": [ d.strftime("%Y-%m-%d %H:%M") for d in self.__filter_frame_by_text(text)["date"].to_dict().values()]}

    def count_text_dayname(self, text):
        """Count the dayname of the specified text"""
        return WordTools.count_day(self.__get_text_activities(text))


class GeneralOperator(FileParser):
    def __init__(self):
        pass

    def count_owner(self):
        return self.frame["owner"].value_counts().to_dict()

    def count_hour(self):
        datetimelist = self.frame["date"]
        return WordTools.count_hour(datetimelist)

    def count_day(self):
        return self.frame["day_name"].value_counts().reindex(WordTools.days_list()).dropna().to_dict()

    def count_month(self):
        return self.frame["month"].value_counts().reindex(WordTools.months_list()).fillna(0).to_dict()

    def count_emojis(self):
        text_list = self.frame["text"]
        return WordTools.extract_emojis(" ".join(text_list))

    def count_year(self):
        return self.frame["year"].value_counts().to_dict()

    def count_word(self):
        text_list = self.frame["text"]
        text_list =  [WordTools.text_cleaner(w) for w in text_list]
        cw =  WordTools.count_word(" ".join(text_list).split())
        tDf = pd.DataFrame([cw.keys(),cw.values()]).T
        # qt99 = tDf[1].quantile(.99)
        # # print(tDf)
        # # print("qq", qt99)
        # tDf = tDf[tDf[1] <= qt99]
        # print(tDf)
        d = {}
        for i in range(tDf.index.size):
            k,v  = tDf.iloc[i]
            d[k] = v
        # print(d)
        return d

    def get_conversations(self):
        # date, owner, text = self.frame["date"], self.frame["owner"], self.frame["text"]
        # date = [d.strftime("%Y-%m-%d %H:%m") for d in date]
        # data = []
        # for i in range(len(date)):
        #     d = {
        #         "id": i + 1,
        #         "date": date[i],
        #         "owner": owner.iloc[i],
        #         "text": text.iloc[i]
        #     }
        #     data.append(d)
        # return {"conversations": data}
        conversations = list(self.frame[["date","owner", "text"]].T.to_dict().values())
        return conversations

    def get_activities(self):
        data = {}
        labels = self.frame["date"].value_counts().sort_index().index
        values = self.frame["date"].value_counts().sort_index().values
        labels = [d.strftime("%Y-%m-%d %H:%M") for d in labels]
        values = [int(i) for i in values]
        for i in range(len(labels)):
            # data.append({"date": labels[i], "value":values[i]})
            data[labels[i]] = values[i]
        return data


class HierarchyOperator(FileParser):
        def __init__(self):
            pass

        def __filter_year(self, year):
            return self.frame[self.frame.year == year]

        def __filter_month(self, year, month):
            frame = self.__filter_year(year)
            return frame[frame.month == month]

        def __filter_hour(self, year, month, day):
            frame = self.__filter_month(year, month)
            return frame[frame.day == day]

        def __pack_hour(self,frame):
            packets = []
            for key,value in frame["hour"].value_counts().to_dict().items():
                packets.append({"name": str(key) + ":00", "value":value})
            return packets

        def make_time_root(self):
            years = self.frame.year.unique()
            parent = []
            for y in years:
                months = self.__filter_year(y).month.unique()
                children = []
                for m in months:
                    days = self.__filter_month(y,m).day.unique()
                    grand_children = []
                    for d in days:
                        ends_frame = self.__filter_hour(y,m,d)
                        packets = self.__pack_hour(ends_frame)
                        grand_children.append({"name": m[:3] + "/" + str(d), "children": packets})
                    children.append({"name": m, "children": grand_children})
                parent.append({"name": str(y), "children": children})
            return {"name": "root", "children": parent}



class Operator(OwnerOperator, DateOperator, TextOperator, GeneralOperator, HierarchyOperator):
    def __init__(self):
        super(OwnerOperator, self).__init__()
        super(DateOperator, self).__init__()
        super(TextOperator, self).__init__()
        super(GeneralOperator, self).__init__()
        super(HierarchyOperator, self).__init__()
