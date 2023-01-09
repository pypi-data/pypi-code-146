import ast
import csv
import datetime
import enum
import logging
import os.path
from typing import List

from PySide6 import QtCore

NO_VALUE_SET_INT = -1
NO_VALUE_SET_STR = ""
DATABASE_FILE_NAME_STR = "remembrances.csv"


class ContentType(enum.Enum):
    not_set = -1
    text = 0
    image = 1
    web_page = 2
    custom = 3
    breathing = 4


class RememberItem:
    def __init__(self):
        self.id_int = NO_VALUE_SET_INT

        self.permanent_bool = False

        self.last_activated_ts_int = NO_VALUE_SET_INT  # -default: never activated

        self.next_notif_ts_int = NO_VALUE_SET_INT

        self.notif_spec_secs_list = []  # -please note that these are stored in secs (unix timestamp)
        self.notif_freq_secs_int = NO_VALUE_SET_INT  # -both of these are possible, though this may result in overlap

        self.notif_active_bool = True
        self.notif_fired_bool = False

        self.title_str = NO_VALUE_SET_STR

        self.content_type_enum = ContentType.not_set
        self.content_str = NO_VALUE_SET_STR  # -can be a text, a webpage link, a file image name, or a custom command

    def export_names(self):
        # -used for the fieldnames
        export_dict = self.__dict__
        key_list = export_dict.keys()
        return key_list

    def export(self):
        export_dict = self.__dict__
        return export_dict

    def get_next_notification_time(self) -> int:
        if self.notif_active_bool == False:
            return NO_VALUE_SET_INT
        if self.permanent_bool:
            return NO_VALUE_SET_INT

        # today_qdt = QtCore.QDateTime(QtCore.QDate.currentDate())
        today_qdt = QtCore.QDateTime()
        today_qdt.setDate(QtCore.QDate.currentDate())
        today_ts_secs = today_qdt.toSecsSinceEpoch()
        now_ts_secs_int = QtCore.QDateTime.currentSecsSinceEpoch()

        # Closest of the specified times
        spec_closest_time_int = NO_VALUE_SET_INT  # -if the list is empty
        if len(self.notif_spec_secs_list) > 0:
            for time_during_day_secs_int in sorted(self.notif_spec_secs_list):
                if now_ts_secs_int < today_ts_secs + time_during_day_secs_int:
                    spec_closest_time_int = today_ts_secs + time_during_day_secs_int  # -the closest future time
                    break
            if spec_closest_time_int == NO_VALUE_SET_INT:
                # Going to the next day
                tomorrow_qdt = today_qdt.addDays(1)
                tomorrow_ts_secs = tomorrow_qdt.toSecsSinceEpoch()
                spec_closest_time_int = sorted(self.notif_spec_secs_list)[0] + tomorrow_ts_secs

        # Closest of the frequency times
        freq_closest_time_int = NO_VALUE_SET_INT
        if self.notif_freq_secs_int != NO_VALUE_SET_INT:
            freq_closest_time_int = now_ts_secs_int + self.notif_freq_secs_int

        # Lowest of specified and frequency
        if freq_closest_time_int == NO_VALUE_SET_INT and spec_closest_time_int == NO_VALUE_SET_INT:
            return NO_VALUE_SET_INT
        elif freq_closest_time_int == NO_VALUE_SET_INT:
            return spec_closest_time_int
        elif spec_closest_time_int == NO_VALUE_SET_INT:
            return freq_closest_time_int
        elif freq_closest_time_int < spec_closest_time_int:
            return freq_closest_time_int
        return spec_closest_time_int

    @staticmethod
    def get_item(i_id: int):
        if i_id == NO_VALUE_SET_INT:
            return None
        for remember_item in Remembrances.get_all():
            if remember_item.id_int == i_id:
                return remember_item
        return None

    @staticmethod
    def del_item(i_id: int):
        index = 0
        for remember_item in Remembrances.get_all():
            if remember_item.id_int == i_id:
                Remembrances.get_all().pop(index)
                break
            index += 1
        Remembrances.store()

    @staticmethod
    def get_nr_of_fired_notifications() -> int:
        count = 0
        for remembrance_item in Remembrances.get_all():
            if remembrance_item.notif_fired_bool:
                count += 1
        return count

    @staticmethod
    def get_sorted_ids_of_fired_notifications(i_type_list: List[ContentType]) -> List[int]:
        type_and_rb_list = []
        for remembrance_item in Remembrances.get_all():
            if remembrance_item.notif_fired_bool and (remembrance_item.content_type_enum in i_type_list):
                type_and_rb_list.append((remembrance_item.content_type_enum.value, remembrance_item))

        ret_intlist = []
        for _, remembrance_item in sorted(type_and_rb_list, key=lambda x: x[0]):
            # -this makes sure that ids for texts come first, then images, websites, and last custom
            ret_intlist.append(remembrance_item.id_int)

        return ret_intlist

    """
    @staticmethod
    def get_all() -> List[RememberItem]:
        items = Remembrances.get()
        # ordered_dict = collections.OrderedDict(sorted(items, key=lambda t: int(t[0])))
        # return ordered_dict.items()
        # -returns key and value    
    @staticmethod
    def close():
        if Remembrances.remember_list is not None:
            Remembrances.get().close()
    """

    @staticmethod
    def add_item(i_title: str, i_content_type: ContentType, i_content: str, i_frequency: int = NO_VALUE_SET_INT):
        remembrances_list = Remembrances.get_all()
        new_index_int = 0
        if remembrances_list:
            new_index_int = RememberItem.get_max_id() + 1

        remember_item = RememberItem()
        remember_item.id_int = new_index_int
        remember_item.title_str = i_title
        remember_item.content_type_enum = i_content_type
        remember_item.content_str = i_content
        remember_item.notif_freq_secs_int = i_frequency

        Remembrances.get_all().append(remember_item)
        Remembrances.store()

        return new_index_int

    @staticmethod
    def get_max_id() -> int:
        highest_id_int = -1
        for remembrance_item in Remembrances.get_all():
            if remembrance_item.id_int > highest_id_int:
                highest_id_int = remembrance_item.id_int
        return highest_id_int


class Remembrances:
    first_pass_bool: bool = True
    __remember_list: List[RememberItem] = []

    # TODO: only reference this in the get_all function

    @staticmethod
    def get_all() -> List[RememberItem]:
        if Remembrances.first_pass_bool:
            Remembrances.first_pass_bool = False
            if not os.path.isfile(DATABASE_FILE_NAME_STR):
                # -first time application is started
                with open(DATABASE_FILE_NAME_STR, "w+") as new_file:
                    new_file.close()
                setup_test_data()
            else:
                Remembrances.update_remembrances_from_csv_file()

        # logging.info("Remembrances.remember_list = " + str(Remembrances.__remember_list))
        return Remembrances.__remember_list

    @staticmethod
    def update_remembrances_from_csv_file() -> None:
        read_file = open(DATABASE_FILE_NAME_STR, newline='')
        csv_reader = csv.DictReader(read_file)
        # Remembrances.remember_list = list(csv_reader)

        # csv_reader_list = list(csv_reader)
        for row_od in csv_reader:
            # -new in Python 3.6: Rows are OrderedDicts
            generated_item = RememberItem()
            for attribute in row_od:
                raw_value_str = row_od[attribute]
                if not raw_value_str:
                    continue  # -this means that we didn't find a value and will therefore use the default
                value = None
                if not hasattr(generated_item, attribute):
                    logging.warn(str(type(
                        generated_item)) + " is missing attribute " + attribute + " (the default value will be used)")
                if attribute.endswith("_str"):
                    value = str(raw_value_str)
                elif attribute.endswith("_int"):
                    value = int(raw_value_str)
                elif attribute.endswith("_bool"):
                    my_bool = ast.literal_eval(raw_value_str)
                    assert (isinstance(my_bool, bool))
                    value = ast.literal_eval(raw_value_str)
                elif attribute.endswith("_list"):
                    my_list = ast.literal_eval(raw_value_str)
                    assert (isinstance(my_list, list))
                    value = [int(i) for i in my_list]
                elif attribute == "content_type_enum":
                    # enum_int = int(row_od[attribute])
                    # logging.debug("enum_int = " + str(enum_int))
                    # value = ContentType(int(row_od[attribute]))
                    enum_str = raw_value_str.split(".")[1]
                    value = ContentType[enum_str]
                else:
                    raise Exception("Unrecognized type during import")
                # ast.literal_eval(row_od[attribute])
                # logging.warning("attribute = " + str(attribute))
                # logging.warning("row_od[attribute] = " + str(row_od[attribute]))
                setattr(generated_item, attribute, value)

            if generated_item.id_int == NO_VALUE_SET_INT:
                logging.debug("No id found: Auto generating a new ID")
                new_index_int = RememberItem.get_max_id() + 1
                generated_item.id_int = new_index_int
            if generated_item.content_type_enum == ContentType.not_set:
                logging.warning('No content type found: Setting to "text"')
                generated_item.content_type_enum = ContentType.text

            Remembrances.__remember_list.append(generated_item)
            # print("io default buffer size = " + str(io.DEFAULT_BUFFER_SIZE))
            # read_file.close()

    @staticmethod
    def store():
        with open(DATABASE_FILE_NAME_STR, "w", buffering=32768) as write_file:
            rem_item_for_fieldnames = RememberItem()

            field_name_list = rem_item_for_fieldnames.export_names()
            # rem_item_one.export_names()
            # print("field_name_list = " + str(field_name_list))
            # getattr, setattr
            csv_dict_writer = csv.DictWriter(write_file, fieldnames=field_name_list)
            csv_dict_writer.writeheader()

            for remembrance_item in Remembrances.get_all():
                csv_dict_writer.writerow(remembrance_item.export())

    @staticmethod
    def update_item(i_remembrance_item: RememberItem, i_store: bool = True):
        # i_store can be set to False for example when updating many values at once
        if i_remembrance_item.id_int == NO_VALUE_SET_INT:
            return
        index = 0
        for remembrance_item in Remembrances.get_all():
            if remembrance_item.id_int == i_remembrance_item.id_int:
                Remembrances.__remember_list[index] = i_remembrance_item
                break
            index += 1
        if i_store:
            Remembrances.store()

    @staticmethod
    def update_permanent(id_int: int, i_permanent: bool):
        remember_item = RememberItem.get_item(id_int)
        remember_item.permanent_bool = i_permanent
        Remembrances.update_item(remember_item)

    @staticmethod
    def update_spec_times(id_int: int, i_notif_spec_secs_list: List[int]):
        remember_item = RememberItem.get_item(id_int)
        remember_item.notif_spec_secs_list = i_notif_spec_secs_list
        Remembrances.update_item(remember_item)

        """
        if id_int == NO_VALUE_SET_INT:
            return
        index = 0
        for remembrance_item in Remembrances.get_all():
            if remembrance_item.id_int == id_int:
                Remembrances.__remember_list[index].notif_spec_secs_list = i_notif_spec_secs_list
                break
            index += 1
        Remembrances.store()
        """

    @staticmethod
    def update_notif_active(id_int: int, i_notif_active: bool):
        remember_item = RememberItem.get_item(id_int)
        remember_item.notif_active_bool = i_notif_active
        Remembrances.update_item(remember_item)

    @staticmethod
    def update_content_type(id_int: int, i_content_type: ContentType):
        remember_item = RememberItem.get_item(id_int)
        remember_item.content_type_enum = i_content_type
        Remembrances.update_item(remember_item)

    @staticmethod
    def update_notif_fired(id_int: int, i_notif_fired: bool, i_store: bool = True):
        remember_item = RememberItem.get_item(id_int)
        remember_item.notif_fired_bool = i_notif_fired
        Remembrances.update_item(remember_item, i_store)

    @staticmethod
    def update_next_notif(id_int: int, i_next_notif: int):
        remember_item = RememberItem.get_item(id_int)
        remember_item.next_notif_ts_int = i_next_notif
        Remembrances.update_item(remember_item)

    @staticmethod
    def update_title(id_int: int, i_title: str, i_store: bool = True):
        remember_item = RememberItem.get_item(id_int)
        remember_item.title_str = i_title
        Remembrances.update_item(remember_item, i_store)

    @staticmethod
    def update_notif_freq(id_int: int, i_notif_freq: int):
        remember_item = RememberItem.get_item(id_int)
        remember_item.notif_freq_secs_int = i_notif_freq
        Remembrances.update_item(remember_item)

    @staticmethod
    def update_last_activated_ts(id_int: int, i_last_activated_ts: int):
        remember_item = RememberItem.get_item(id_int)
        remember_item.last_activated_ts_int = i_last_activated_ts
        Remembrances.update_item(remember_item)

    @staticmethod
    def update_content(id_int: int, i_content: str, i_store: bool = True):
        remember_item = RememberItem.get_item(id_int)
        remember_item.content_str = i_content
        Remembrances.update_item(remember_item, i_store)


def setup_test_data():
    quote_str = """Quote here lorem ipsum, continuing on multiple lines when more text, and if even more we will get a vertical scrollbar"""
    RememberItem.add_item(
        "Quote [example]",
        ContentType.text,
        quote_str,
        NO_VALUE_SET_INT
    )

    insight_str = """<h2>html Title</h2><p>Insight text here</p>"""
    RememberItem.add_item(
        "Insight (10min) [example]",
        ContentType.text,
        insight_str,
        10 * 60
    )

    RememberItem.add_item(
        "Image (3min) [example]",
        ContentType.image,
        "DSC_1033.JPG",
        3 * 60
    )

    RememberItem.add_item(
        "Web site [example]",
        ContentType.web_page,
        "https://self-compassion.org/",
        NO_VALUE_SET_INT
    )

    """
    qtime_12 = QtCore.QTime(12, 0)
    qtime_18 = QtCore.QTime(18, 0)
    quote_1_rememberance = Remembrances.get_item(quote_1_id_int)
    times_list = quote_1_rememberance.times_during_day_secs_list
    times_list.append(qtime_12.msecsSinceStartOfDay() // 1000)
    times_list.append(qtime_18.msecsSinceStartOfDay() // 1000)
    Remembrances.update_spec_times_list(quote_1_id_int, times_list)
    in_half_a_minute_int = QtCore.QDateTime.currentDateTime().toSecsSinceEpoch() + 30
    Remembrances.update_planned_notification(quote_1_id_int, in_half_a_minute_int)

    RememberItem.add_item(
        "Application (1min)",
        ContentType.custom,
        "/home/sunyata/PycharmProjects/mindfulness/mindfulness.py",
        1 * 60
    )

    a_minute_ago_int = QtCore.QDateTime.currentDateTime().toSecsSinceEpoch() - 60
    Remembrances.update_planned_notification(image_1_id_int, a_minute_ago_int)
    """


def export_all():
    # If we want to automate this: https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
    csv_writer = csv.writer(open("exported.csv", "w"))
    for (key_str, remembrance_item) in Remembrances.get_all_keys_plus_items():
        csv_writer.writerow(
            (remembrance_item.title_str, remembrance_item.content_type_enum.name,
             remembrance_item.content_link_or_text_str)
        )


def get_base_dir() -> str:
    first_str = os.path.abspath(__file__)
    # -__file__ is the file that started the application, in other words mindfulness-at-the-computer.py
    second_str = os.path.dirname(first_str)
    base_dir_str = os.path.dirname(second_str)
    return base_dir_str


BACKUP_DIR_STR = "backups"


def get_user_backup_path(i_file_name: str = "") -> str:
    file_or_dir_path_str = os.path.join(get_base_dir(), BACKUP_DIR_STR)
    os.makedirs(file_or_dir_path_str, exist_ok=True)
    if i_file_name:
        file_or_dir_path_str = os.path.join(file_or_dir_path_str, i_file_name)
    return file_or_dir_path_str
    # user_dir_path_str = QtCore.QDir.currentPath() + "/user_files/images/"
    # return QtCore.QDir.toNativeSeparators(user_dir_path_str)


def removing_oldest_files(directory_path: str, i_suffix: str, i_nr_of_files_to_keep: int):
    # Removing the oldest files
    filtered_files_list = [
        fn for fn in os.listdir(directory_path) if fn.endswith(i_suffix)
    ]
    sorted_and_filtered_files_list = sorted(filtered_files_list)
    logging.debug("sorted_and_filtered_files_list = " + str(sorted_and_filtered_files_list))
    for file_name_str in sorted_and_filtered_files_list[:-i_nr_of_files_to_keep]:
        file_path_str = os.path.join(directory_path, file_name_str)
        os.remove(file_path_str)
        logging.debug("File " + file_name_str + " was removed")


PY_DATETIME_FILENAME_FORMAT_STR = "%Y-%m-%dT%H-%M-%S"
BACKUP_USING_COPY_FILENAME_SUFFIX_STR = "_db_backup_using_copy.csv"
import shutil


def backup_db_file() -> int:
    date_sg = datetime.datetime.now().strftime(PY_DATETIME_FILENAME_FORMAT_STR)

    backup_dir_str = get_user_backup_path()  # -alt: os.path.abspath(new_file_name_sg)
    removing_oldest_files(backup_dir_str, BACKUP_USING_COPY_FILENAME_SUFFIX_STR, 3)

    new_file_name_sg = get_user_backup_path(date_sg + BACKUP_USING_COPY_FILENAME_SUFFIX_STR)
    new_file_path_str = get_user_backup_path(new_file_name_sg)

    shutil.copyfile(DATABASE_FILE_NAME_STR, new_file_path_str)
    # TODO: Catching exception if there's not enough diskspace available

    file_size_in_bytes_int = os.path.getsize(new_file_path_str)
    return file_size_in_bytes_int
