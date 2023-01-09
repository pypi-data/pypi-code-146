from __future__ import annotations

import abc
import csv
import datetime
import enum
import hashlib
import logging
import math
import os
from typing import List, Tuple

#################
#
# Model
#
# This module contains everything related to the model for the application:
# * The db schema TODO: Update description since we have moved things into the db.py file
# * The db connection
# * Data structure classes (each of which contains functions for reading and writing to the db)
# * Database creation and setup
# * Various functions (for backing up the db etc)
#
# Notes:
# * When inserting vales, it's best to use "VALUES (?, ?)" because then the sqlite3 module will take care of
#   escaping strings for us
#
#################


ALL_ENTRIES_NO_PAGINATION_INT = -1
LAST_PAGE_INT = -2


class ListM(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_all():
        """Returns all items for the list"""

    @staticmethod
    @abc.abstractmethod
    def get(i_id: int):
        """Returns a single item for the list"""

    @staticmethod
    @abc.abstractmethod
    def remove(i_id: int):
        """Removes an entry"""


class ListWithOrderM(ListM):
    @staticmethod
    @abc.abstractmethod
    def update_sort_order(i_id: int, i_sort_order: int) -> None:
        """Changes the sort order for a single item"""


class FilterPresetM():
    def __init__(
            self,
            i_id: int = -1,
            i_order: int = -1,
            i_title: str = "",
            i_tag_active: bool = False,
            i_tag_id: int = wbd.wbd_global.NO_ACTIVE_TAG_INT,
            i_search_active: bool = False,
            i_search_term: str = "",
            i_rating_active: bool = False,
            i_rating: int = 0,
            i_datetime_active: bool = False,
            i_start_datetime_string: str = wbd.wbd_global.DATETIME_NOT_SET_STR,
            i_end_datetime_string: str = wbd.wbd_global.DATETIME_NOT_SET_STR
    ):
        # -TODO: Removing default values? These aren't used anyway?

        self.id_int = i_id
        self.sort_order_int = i_order
        self.title_str = i_title

        self.tag_active_bool = i_tag_active  # False
        self.tag_id_int = i_tag_id  # wbd.wbd_global.NO_ACTIVE_TAG_INT
        # TODO: Can we trust that -1 is never used as a primary key?

        self.search_active_bool = i_search_active  # False
        self.search_term_str = i_search_term  # ""

        self.rating_active_bool = i_rating_active  # False
        self.rating_int = i_rating

        self.datetime_active_bool = i_datetime_active  # False
        self.start_datetime_string = i_start_datetime_string  # OLD[None]
        self.end_datetime_string = i_end_datetime_string  # OLD[QtCore.QDate.currentDate()]

    # get_filter_preset_by_title
    @staticmethod
    def get_by_title(i_title: str) -> FilterPresetM:
        # This works since the title is "unique" in our SQLite db
        db_cursor_result = wbd.db.db_exec(
            "SELECT * FROM " + wbd.db.DbSchemaM.FilterPresetTable.name
            + " WHERE " + wbd.db.DbSchemaM.FilterPresetTable.Cols.title + "= ?",
            (i_title,)
        )
        filter_preset_db_te = db_cursor_result.fetchone()
        ret_filter_preset = FilterPresetM(*filter_preset_db_te)
        return ret_filter_preset

    # get_all_filter_presets
    @staticmethod
    def get_all() -> List[FilterPresetM]:
        db_connection = wbd.db.DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + wbd.db.DbSchemaM.FilterPresetTable.name
        )
        filter_preset_db_te_list = db_cursor_result.fetchall()
        db_connection.commit()

        ret_filter_preset_list = [
            FilterPresetM(*filter_preset_db_te) for filter_preset_db_te in filter_preset_db_te_list
        ]
        return ret_filter_preset_list

    # add_filter_preset
    @staticmethod
    def add(
            i_title: str,
            i_tag_active_bool,
            i_tag_id_int,
            i_search_active_bool,
            i_search_term_str,
            i_rating_active_bool,
            i_rating_int,
            i_datetime_active_bool,
            i_start_datetime_string,
            i_end_datetime_string
    ) -> int:
        sort_order = len(FilterPresetM.get_all())
        print("sort_order = " + str(sort_order))
        db_cursor = wbd.db.db_exec(
            "INSERT INTO " + wbd.db.DbSchemaM.FilterPresetTable.name
            + "(" + wbd.db.DbSchemaM.FilterPresetTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.title
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.tag_active
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.tag_id_ref
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.search_active
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.search_term
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.rating_active
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.rating
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.datetime_active
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.start_date
            + ", " + wbd.db.DbSchemaM.FilterPresetTable.Cols.end_date
            + ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                sort_order,
                i_title,
                i_tag_active_bool,
                i_tag_id_int,
                i_search_active_bool,
                i_search_term_str,
                i_rating_active_bool,
                i_rating_int,
                i_datetime_active_bool,
                i_start_datetime_string,
                i_end_datetime_string
            )
        )
        # -sort_order is generated here, other values are taken from the filter preset sent to the function
        #  (probably the active preset stored in memory and in the wbd_global module)
        # -using the bools as ints above works since this is how python 2.6 and 3.x works with bools. More info here:
        #  https://stackoverflow.com/a/2764099/2525237
        filter_preset_id_int = db_cursor.lastrowid
        return filter_preset_id_int


class QuestionM(ListWithOrderM):
    def __init__(self, i_id: int, i_order: int, i_title: str, i_description: str) -> None:
        self.id_int = i_id
        self.sort_order_int = i_order
        self.title_str = i_title
        self.description_str = i_description

    @staticmethod
    def get(i_id_it) -> QuestionM:
        db_connection = wbd.db.DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + wbd.db.DbSchemaM.QuestionTable.name
            + " WHERE " + wbd.db.DbSchemaM.QuestionTable.Cols.id + "=" + str(i_id_it)
        )
        journal_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        ret_question = QuestionM(*journal_db_te)
        return ret_question

    @staticmethod
    def get_all() -> List[QuestionM]:
        db_connection = wbd.db.DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + wbd.db.DbSchemaM.QuestionTable.name
        )
        journal_db_te_list = db_cursor_result.fetchall()
        db_connection.commit()

        ret_question_list = [QuestionM(*journal_db_te) for journal_db_te in journal_db_te_list]
        return ret_question_list

    # <API function>
    @staticmethod
    def update_sort_order(i_id: int, i_sort_order: int) -> None:
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.QuestionTable.name
            + " SET " + wbd.db.DbSchemaM.QuestionTable.Cols.sort_order + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.QuestionTable.Cols.id + " = ?",
            (str(i_sort_order), str(i_id))
        )

    @staticmethod
    def update_title(i_id: int, i_new_text: str) -> None:
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.QuestionTable.name
            + " SET " + wbd.db.DbSchemaM.QuestionTable.Cols.title + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.QuestionTable.Cols.id + " = ?",
            (i_new_text, str(i_id))
        )

    @staticmethod
    def update_description(i_id: int, i_new_text: str) -> None:
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.QuestionTable.name
            + " SET " + wbd.db.DbSchemaM.QuestionTable.Cols.description + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.QuestionTable.Cols.id + " = ?",
            (i_new_text, str(i_id))
        )

    @staticmethod
    def remove(i_id: int) -> None:
        wbd.db.db_exec(
            "DELETE FROM " + wbd.db.DbSchemaM.QuestionTable.name
            + " WHERE " + wbd.db.DbSchemaM.QuestionTable.Cols.id + "= ?",
            (str(i_id),)
        )
        # TODO: Add code for removing tag associations as well

    @staticmethod
    def add(i_title: str, i_description: str) -> int:
        sort_order = len(QuestionM.get_all())
        print("sort_order = " + str(sort_order))
        db_cursor = wbd.db.db_exec(
            "INSERT INTO " + wbd.db.DbSchemaM.QuestionTable.name
            + "(" + wbd.db.DbSchemaM.QuestionTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.QuestionTable.Cols.title
            + ", " + wbd.db.DbSchemaM.QuestionTable.Cols.description
            + ") VALUES (?, ?, ?)",
            (sort_order, i_title, i_description)
        )
        question_id_int = db_cursor.lastrowid
        return question_id_int


class EntryM:
    def __init__(self, i_id, i_datetime_added: str, i_sort_order: int, i_rating: int, i_diary_text: str,
                 i_image_file: bytes):
        self.id = i_id
        self.datetime_added_str = i_datetime_added
        self.sort_order_int = i_sort_order
        self.rating_int = i_rating
        self.diary_text_str = i_diary_text
        self.image_file_bytes = i_image_file

    def is_all_day(self) -> bool:
        if self.datetime_added_str.find('T') == -1:
            return True
        return False

    @staticmethod
    def add(i_datetime_added: str, i_sort_order: int = 0, i_diary_text: str = "", i_rating: int = 1,
            i_image_file: bytes = None) -> int:
        db_cursor = wbd.db.db_exec(
            "INSERT INTO " + wbd.db.DbSchemaM.EntryTable.name
            + "(" + wbd.db.DbSchemaM.EntryTable.Cols.datetime_added
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.text
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.rating
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.image_file
            + ") VALUES (?, ?, ?, ?, ?)",
            (i_datetime_added, i_sort_order, i_diary_text, i_rating, i_image_file)
        )
        entry_id_int = db_cursor.lastrowid
        return entry_id_int

    @staticmethod
    def add_with_id(i_id: int, i_datetime_added: str, i_sort_order: int = 0, i_diary_text: str = "", i_rating: int = 1,
                    i_image_file: bytes = None) -> int:
        db_cursor = wbd.db.db_exec(
            "INSERT INTO " + wbd.db.DbSchemaM.EntryTable.name
            + "(" + wbd.db.DbSchemaM.EntryTable.Cols.id
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.datetime_added
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.text
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.rating
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.image_file
            + ") VALUES (?, ?, ?, ?, ?, ?)",
            (i_id, i_datetime_added, i_sort_order, i_diary_text, i_rating, i_image_file)
        )
        entry_id_int = db_cursor.lastrowid
        return entry_id_int

    @staticmethod
    def update_text(i_id: int, i_new_text: str) -> None:
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.EntryTable.name
            + " SET " + wbd.db.DbSchemaM.EntryTable.Cols.text + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.EntryTable.Cols.id + " = ?",
            (i_new_text, i_id)
        )

    @staticmethod
    def update_datetime(i_id: int, i_new_datetime: str) -> None:
        # TODO: Not sure if we need the lines below
        # since sqlite may sort Y-M-D before Y-M-DTH:M:S even if the date part is the same
        """
        if i_new_datetime.find('T') == -1:
            # -date without time
            sort_order_int = 255
        else:
            sort_order_int = 0
            # -used for now, may become more complex in the future.
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.EntryTable.name
            + " SET " + wbd.db.DbSchemaM.EntryTable.Cols.sort_order + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.EntryTable.Cols.id + " = ?",
            (sort_order_int, i_id)
        )
        """

        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.EntryTable.name
            + " SET " + wbd.db.DbSchemaM.EntryTable.Cols.datetime_added + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.EntryTable.Cols.id + " = ?",
            (i_new_datetime, i_id)
        )

    @staticmethod
    def update_rating(i_id: int, i_rating: int) -> None:
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.EntryTable.name
            + " SET " + wbd.db.DbSchemaM.EntryTable.Cols.rating + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.EntryTable.Cols.id + " = ?",
            (i_rating, i_id)
        )

    @staticmethod
    def get(i_id: int) -> EntryM:
        db_cursor_result = wbd.db.db_exec(
            "SELECT * FROM " + wbd.db.DbSchemaM.EntryTable.name
            + " WHERE " + wbd.db.DbSchemaM.EntryTable.Cols.id + "= ?",
            (i_id,)
        )
        diary_db_te = db_cursor_result.fetchone()
        return EntryM(*diary_db_te)

    @staticmethod
    def remove(i_id: int) -> None:
        # Removing relations to this entry
        wbd.db.db_exec(
            "DELETE FROM " + wbd.db.DbSchemaM.TagEntryRelationTable.name
            + " WHERE " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref + "= ?",
            (i_id,)
        )

        wbd.db.db_exec(
            "DELETE FROM " + wbd.db.DbSchemaM.EntryTable.name
            + " WHERE " + wbd.db.DbSchemaM.EntryTable.Cols.id + "= ?",
            (i_id,)
        )

    @staticmethod
    def update_image(i_id: int, i_image_file: bytes) -> None:
        """
        if i_image_file is None:
            entry = get_entry(i_id)
            wbd.wbd_global.delete_image_file(entry.image_file_name_str)
        """
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.EntryTable.name
            + " SET " + wbd.db.DbSchemaM.EntryTable.Cols.image_file + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.EntryTable.Cols.id + " = ?",
            (i_image_file, i_id)
        )

    @staticmethod
    def does_entry_exist(i_id: int) -> bool:
        db_cursor_result = wbd.db.db_exec(
            "SELECT * FROM " + wbd.db.DbSchemaM.EntryTable.name
            + " WHERE " + wbd.db.DbSchemaM.EntryTable.Cols.id + "= ?",
            (i_id,)
        )
        diary_db_te = db_cursor_result.fetchone()
        if diary_db_te is None:
            return False
        return True

    @staticmethod
    def get_entry_list_and_max_page_nr(
            i_tag_active_bool, i_tag_id_int,
            i_search_active_bool, i_search_term_str,
            i_rating_active_bool, i_rating_int,
            i_datetime_active_bool, i_start_datetime_string, i_end_datetime_string,
            i_page_number_int: int = ALL_ENTRIES_NO_PAGINATION_INT
    ) -> (List[EntryM], int):

        sqlite_vars_list = []

        sqlite_where_list = []

        sqlite_select_str = "*"
        sqlite_join_str = ""
        if i_tag_active_bool and i_tag_id_int != wbd.wbd_global.NO_ACTIVE_TAG_INT:
            sqlite_select_str = wbd.db.DbSchemaM.EntryTable.name + ".*"
            sqlite_join_str = (
                    " INNER JOIN " + wbd.db.DbSchemaM.TagEntryRelationTable.name
                    + " ON " + wbd.db.DbSchemaM.EntryTable.name + "." + wbd.db.DbSchemaM.EntryTable.Cols.id
                    + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref
            )
            sqlite_where_list.append(wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref + " = ?")
            sqlite_vars_list.append(i_tag_id_int)

        if i_search_active_bool:
            sqlite_search_term_str = wbd.db.DbSchemaM.EntryTable.Cols.text + " LIKE ?"
            sqlite_where_list.append(sqlite_search_term_str)
            sqlite_vars_list.append("%" + i_search_term_str + "%")

        if i_rating_active_bool:
            sqlite_rating_str = wbd.db.DbSchemaM.EntryTable.Cols.rating + ">= ?"
            sqlite_where_list.append(sqlite_rating_str)
            sqlite_vars_list.append(i_rating_int)

        if i_datetime_active_bool and i_start_datetime_string != wbd.wbd_global.DATETIME_NOT_SET_STR:
            sqlite_start_date_str = wbd.db.DbSchemaM.EntryTable.Cols.datetime_added + " >= ?"
            sqlite_where_list.append(sqlite_start_date_str)
            sqlite_vars_list.append(i_start_datetime_string)

        if i_datetime_active_bool and i_end_datetime_string != wbd.wbd_global.DATETIME_NOT_SET_STR:
            end_datetime_string = i_end_datetime_string + "T23:59:59"
            sqlite_end_date_str = wbd.db.DbSchemaM.EntryTable.Cols.datetime_added + " <= ?"
            sqlite_where_list.append(sqlite_end_date_str)
            sqlite_vars_list.append(end_datetime_string)

        sqlite_where_and_combined_string_str = ""
        count_int = 0
        for sqlite_where_item_str in sqlite_where_list:
            prefix_str = " AND "
            if count_int == 0:
                prefix_str = " WHERE "
            sqlite_where_and_combined_string_str += prefix_str + sqlite_where_item_str
            count_int += 1

        # Finding the number of entries (used for pagination)
        # -TODO: We may want to move this into a separate function,
        # to be called from the functions that rely on the max page

        sqlite_string_str = (
                "SELECT COUNT(*)"
                + " FROM " + wbd.db.DbSchemaM.EntryTable.name
                + sqlite_join_str
                + sqlite_where_and_combined_string_str
        )
        db_cursor_result = wbd.db.db_exec(sqlite_string_str, tuple(sqlite_vars_list))
        logging.debug("sqlite_string_str = " + sqlite_string_str)
        logging.debug("sqlite_vars_list = " + str(sqlite_vars_list))
        number_of_entries_int = db_cursor_result.fetchone()[0]
        logging.debug(" -------------- number_of_entries_int = " + str(number_of_entries_int))

        max_nr_of_pages_int = math.ceil(
            number_of_entries_int
            /
            wbd.wbd_global.DIARY_ENTRIES_PER_PAGE_INT
        )

        # Getting the entries..

        sqlite_limit_and_offset_string_str = ""  # ..for all pages
        if i_page_number_int != ALL_ENTRIES_NO_PAGINATION_INT:
            logging.debug("i_page_number_int = " + str(i_page_number_int))
            sqlite_limit_and_offset_string_str = " LIMIT ? OFFSET ?"
            sqlite_vars_list.append(wbd.wbd_global.DIARY_ENTRIES_PER_PAGE_INT)
            page_nr_starting_at_zero_int = i_page_number_int - 1
            # -transforming so the page nr starts at zero
            sqlite_vars_list.append(page_nr_starting_at_zero_int * wbd.wbd_global.DIARY_ENTRIES_PER_PAGE_INT)
            """
            reversed_page_int = max_nr_of_pages_int - i_page_number_int  # ..for the current page
            if i_page_number_int == LAST_PAGE_INT:
                reversed_page_int = 0  # ..for the last page
            """

        sqlite_string_str = (
                "SELECT " + sqlite_select_str
                + " FROM " + wbd.db.DbSchemaM.EntryTable.name
                + sqlite_join_str
                + sqlite_where_and_combined_string_str
                + " ORDER BY " + wbd.db.DbSchemaM.EntryTable.Cols.datetime_added + " DESC"
                + ", " + wbd.db.DbSchemaM.EntryTable.Cols.sort_order + " DESC"
                + ", " + wbd.db.DbSchemaM.EntryTable.Cols.id + " DESC"
                + sqlite_limit_and_offset_string_str
        )
        """
            + " ORDER BY " + "date(" + wbd.db.DbSchemaM.EntryTable.Cols.datetime_added + ") DESC"
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.sort_order + " DESC"
            + ", " + "time(" + wbd.db.DbSchemaM.EntryTable.Cols.datetime_added + ") DESC"
            + ", " + wbd.db.DbSchemaM.EntryTable.Cols.id + " DESC"
        """
        db_cursor_result = wbd.db.db_exec(sqlite_string_str, tuple(sqlite_vars_list))
        logging.debug("sqlite_string_with_limit_and_offset_str = " + sqlite_string_str)
        logging.debug("sqlite_vars_list = " + str(sqlite_vars_list))

        diary_db_te_list = db_cursor_result.fetchall()
        ret_diary_list = []
        for entry_db_te in reversed(diary_db_te_list):
            ret_diary_list.append(EntryM(*entry_db_te))

        return (ret_diary_list, max_nr_of_pages_int)


class TagM(ListWithOrderM):
    def __init__(self, i_id: int, i_order: int, i_title: str, i_description: str) -> None:
        self.id_int = i_id
        self.sort_order_int = i_order
        self.title_str = i_title  # -<API>
        self.description_str = i_description

    @staticmethod
    def add(i_title: str, i_description: str) -> int:
        sort_order = len(TagM.get_all())
        logging.debug("sort_order = " + str(sort_order))
        db_cursor = wbd.db.db_exec(
            "INSERT INTO " + wbd.db.DbSchemaM.TagTable.name + "("
            + wbd.db.DbSchemaM.TagTable.Cols.sort_order + ", "
            + wbd.db.DbSchemaM.TagTable.Cols.title + ", "
            + wbd.db.DbSchemaM.TagTable.Cols.description
            + ") VALUES (?, ?, ?)",
            (sort_order, i_title, i_description)
        )
        tag_id_int = db_cursor.lastrowid
        return tag_id_int

    @staticmethod
    def get(i_id: int) -> TagM:
        db_cursor_result = wbd.db.db_exec(
            "SELECT * FROM " + wbd.db.DbSchemaM.TagTable.name
            + " WHERE " + wbd.db.DbSchemaM.TagTable.Cols.id + "= ?",
            (i_id,)
        )
        tag_db_te = db_cursor_result.fetchone()
        ret_tag = TagM(*tag_db_te)
        return ret_tag

    @staticmethod
    def tag_with_title_exists(i_title: str) -> bool:
        db_cursor_result = wbd.db.db_exec(
            "SELECT * FROM " + wbd.db.DbSchemaM.TagTable.name
            + " WHERE " + wbd.db.DbSchemaM.TagTable.Cols.title + " LIKE ?",
            (i_title,)
        )
        # -please note that "like" is used here instead of "=", since this function is used when importing
        tag_db_te = db_cursor_result.fetchone()
        if tag_db_te is None:
            return False
        return True

    @staticmethod
    def get_by_title(i_title: str) -> TagM:
        # This works since the title is "unique" in our SQLite db
        db_cursor_result = wbd.db.db_exec(
            "SELECT * FROM " + wbd.db.DbSchemaM.TagTable.name
            + " WHERE " + wbd.db.DbSchemaM.TagTable.Cols.title + "= ?",
            (i_title,)
        )
        tag_db_te = db_cursor_result.fetchone()
        if tag_db_te is None:
            return None
        ret_tag = TagM(*tag_db_te)
        return ret_tag

    @staticmethod
    def get_all(i_sort_order: wbd.wbd_global.SortType = wbd.wbd_global.SortType.sort_by_custom_order) -> List[TagM]:
        ret_tags_list = []
        if i_sort_order == wbd.wbd_global.SortType.sort_by_custom_order:
            db_cursor_result = wbd.db.db_exec(
                "SELECT * FROM " + wbd.db.DbSchemaM.TagTable.name
                + " ORDER BY " + wbd.db.DbSchemaM.TagTable.Cols.sort_order,
                ()
            )
            tag_db_te_list = db_cursor_result.fetchall()
            ret_tags_list = [TagM(*tag_db_te) for tag_db_te in tag_db_te_list]

        elif i_sort_order == wbd.wbd_global.SortType.sort_by_name:
            db_cursor_result = wbd.db.db_exec(
                "SELECT * FROM " + wbd.db.DbSchemaM.TagTable.name
                + " ORDER BY " + wbd.db.DbSchemaM.TagTable.Cols.title,
                ()
            )
            tag_db_te_list = db_cursor_result.fetchall()
            ret_tags_list = [TagM(*tag_db_te) for tag_db_te in tag_db_te_list]

        elif i_sort_order == wbd.wbd_global.SortType.sort_by_frequency:
            tag_count_str = "tag_count"
            db_cursor_result = wbd.db.db_exec(
                "SELECT " + wbd.db.DbSchemaM.TagTable.name + ".*" + ", "
                + "COUNT(" + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref + ") AS " + tag_count_str
                + " FROM " + wbd.db.DbSchemaM.TagTable.name + " LEFT JOIN " + wbd.db.DbSchemaM.TagEntryRelationTable.name
                + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
                + " GROUP BY " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " ORDER BY " + tag_count_str + " DESC",
                ()
            )
            db_te_list = db_cursor_result.fetchall()
            ret_tags_list = [TagM(*db_te[:-1]) for db_te in db_te_list]
            # -please note that we remove the last part of each tuple, since this contains the count

        elif i_sort_order == wbd.wbd_global.SortType.sort_by_time:
            datetime_value_str = "datetime_value_count"
            db_cursor_result = wbd.db.db_exec(
                "SELECT " + wbd.db.DbSchemaM.TagTable.name + ".*" + ", " + wbd.db.DbSchemaM.EntryTable.name + "." + wbd.db.DbSchemaM.EntryTable.Cols.datetime_added
                + " AS " + datetime_value_str
                + " FROM " + wbd.db.DbSchemaM.TagTable.name
                + " LEFT JOIN " + wbd.db.DbSchemaM.TagEntryRelationTable.name
                + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
                + " LEFT JOIN " + wbd.db.DbSchemaM.EntryTable.name
                + " ON " + wbd.db.DbSchemaM.EntryTable.name + "." + wbd.db.DbSchemaM.EntryTable.Cols.id + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref
                + " GROUP BY " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id
                + " ORDER BY MAX(" + datetime_value_str + ") DESC",
                ()
            )

            """
            db_cursor_result = wbd.db.db_exec(
                "SELECT " + wbd.db.DbSchemaM.TagTable.name + ".*" + ", " + wbd.db.DbSchemaM.EntryTable.name + "." + wbd.db.DbSchemaM.EntryTable.Cols.datetime_added
                + " AS " + datetime_value_str
                + " FROM " + wbd.db.DbSchemaM.TagTable.name
                + " LEFT JOIN " + wbd.db.DbSchemaM.TagEntryRelationTable.name
                + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
                + " LEFT JOIN " + wbd.db.DbSchemaM.EntryTable.name
                + " ON " + wbd.db.DbSchemaM.EntryTable.name + "." + wbd.db.DbSchemaM.EntryTable.Cols.id + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref
                + " GROUP BY " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id
                + " HAVING MAX(" + wbd.db.DbSchemaM.EntryTable.Cols.datetime_added + ")"
                + " ORDER BY " + datetime_value_str + " DESC",
                ()
            )
            """

            db_te_list = db_cursor_result.fetchall()
            ret_tags_list = [TagM(*db_te[:-1]) for db_te in db_te_list]
            # -please note that we remove the last part of each tuple, since this contains the count
        else:
            logging.error("no such sorting")
        return ret_tags_list

    @staticmethod
    def update_title(i_id: int, i_new_text: str) -> None:
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.TagTable.name
            + " SET " + wbd.db.DbSchemaM.TagTable.Cols.title + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.TagTable.Cols.id + " = ?",
            (i_new_text, i_id)
        )

    @staticmethod
    def update_description(i_id: int, i_new_text: str) -> None:
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.TagTable.name
            + " SET " + wbd.db.DbSchemaM.TagTable.Cols.description + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.TagTable.Cols.id + " = ?",
            (i_new_text, i_id)
        )

    @staticmethod
    def update_sort_order(i_id: int, i_sort_order: int) -> None:
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.TagTable.name
            + " SET " + wbd.db.DbSchemaM.TagTable.Cols.sort_order + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.TagTable.Cols.id + " = ?",
            (i_sort_order, i_id)
        )

    @staticmethod
    def remove(i_id: int) -> None:
        wbd.db.db_exec(
            "DELETE FROM " + wbd.db.DbSchemaM.TagTable.name
            + " WHERE " + wbd.db.DbSchemaM.TagTable.Cols.id + "= ?",
            (i_id,)
        )
        # TODO: Add code for removing entry and question associations


class ViewM:
    def __init__(self, i_id: int, i_sort_order: int, i_title: str):
        self.id_int = i_id
        self.sort_order_int = i_sort_order
        self.title_str = i_title

    @staticmethod
    def get(i_id: int) -> ViewM:
        db_cursor_result = wbd.db.db_exec(
            "SELECT * FROM " + wbd.db.DbSchemaM.ViewTable.name
            + " WHERE " + wbd.db.DbSchemaM.ViewTable.Cols.id + "= ?",
            (i_id,)
        )
        view_db_te = db_cursor_result.fetchone()
        ret_view = ViewM(*view_db_te)
        return ret_view

    @staticmethod
    def get_all() -> List[ViewM]:
        db_connection = wbd.db.DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + wbd.db.DbSchemaM.ViewTable.name
        )
        db_te_list = db_cursor_result.fetchall()
        db_connection.commit()

        ret_view_list = [ViewM(*db_te) for db_te in db_te_list]
        return ret_view_list

    @staticmethod
    def add(i_title: str) -> int:
        sort_order = 1  # -TODO
        db_cursor = wbd.db.db_exec(
            "INSERT INTO " + wbd.db.DbSchemaM.ViewTable.name
            + "(" + wbd.db.DbSchemaM.ViewTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.ViewTable.Cols.title
            + ") VALUES (?, ?)",
            (sort_order, i_title)
        )
        view_id_int = db_cursor.lastrowid
        return view_id_int


# ===== Special =====

####get_all_tags_referenced_by_question
class TagsSuggestedForQuestionM(ListM):
    def __init__(self, i_tag_id: int, i_sort_order: int, i_tag_is_preselected: bool, i_tag_title: str):
        self._tag_id_int = i_tag_id
        self.sort_order_int = i_sort_order
        self.tag_is_preselected_bool = i_tag_is_preselected
        self._tag_title_str = i_tag_title
        ##########tag_is_preselected = "tag_is_preselected"

    # <API function>
    @property
    def id_int(self) -> int:
        return self._tag_id_int
        # -Please note that it's the tag ID that's returned here

    # <API function>
    @property
    def title_str(self) -> str:
        return self._tag_title_str
        # -Please note that it's the tag title that's returned here
        # -alternatively we can use the tag_id to look this up

    # <API function>
    @staticmethod
    def get_all() -> List[TagsSuggestedForQuestionM]:
        # selecting custom columns here, for matching the init function above
        db_cursor_result = wbd.db.db_exec(
            "SELECT " + wbd.db.DbSchemaM.TagQuestionRelationTable.name + "." + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_id_ref
            + ", " + wbd.db.DbSchemaM.TagQuestionRelationTable.name + "." + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.TagQuestionRelationTable.name + "." + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_is_preselected
            + ", " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.title
            + " FROM " + wbd.db.DbSchemaM.TagQuestionRelationTable.name
            + " LEFT JOIN " + wbd.db.DbSchemaM.TagTable.name
            + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
            + " WHERE " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.question_id_ref + " = ?"
            + " ORDER BY " + wbd.db.DbSchemaM.TagQuestionRelationTable.name + "." + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.sort_order,
            (wbd.wbd_global.active_state.question_id,)
        )
        # -Please note that wbd.wbd_global.active_state.view_id is used here!
        db_te_list = db_cursor_result.fetchall()

        ret_tags_suggested_for_entry_list: List[TagsSuggestedForQuestionM] = []
        for db_te in db_te_list:
            tag_selected_for_entry = TagsSuggestedForQuestionM(*db_te)
            ret_tags_suggested_for_entry_list.append(tag_selected_for_entry)

        logging.debug("ret_tags_suggested_for_entry_list = " + str(ret_tags_suggested_for_entry_list))
        return ret_tags_suggested_for_entry_list

    # <API function>
    @staticmethod
    def get(i_tag_id: int) -> TagsSuggestedForQuestionM:
        # selecting custom columns here, for matching the init function above
        db_cursor_result = wbd.db.db_exec(
            "SELECT " + wbd.db.DbSchemaM.TagQuestionRelationTable.name + "." + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_id_ref
            + ", " + wbd.db.DbSchemaM.TagQuestionRelationTable.name + "." + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.title
            + " FROM " + wbd.db.DbSchemaM.TagQuestionRelationTable.name
            + " LEFT JOIN " + wbd.db.DbSchemaM.TagTable.name
            + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
            + " WHERE " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.question_id_ref + " = ?"
            + " AND " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_id_ref + " = ?",
            (wbd.wbd_global.active_state.question_id, i_tag_id)
        )
        # -Please note that wbd.wbd_global.active_state.view_id is used here!
        db_te = db_cursor_result.fetchone()[0]

        ret_tag_suggested_for_entry = TagsSuggestedForQuestionM(db_te)

        logging.debug("ret_tag_suggested_for_entry = " + str(ret_tag_suggested_for_entry))
        return ret_tag_suggested_for_entry

    # <API function>
    @staticmethod
    def remove(i_id: int):
        TagM.remove(i_id)


class TagsSelectedForEntryM(ListM):
    def __init__(self, i_tag_id: int, i_sort_order: int, i_tag_title: str):
        self._tag_id_int = i_tag_id
        self.sort_order_int = i_sort_order
        self._tag_title_str = i_tag_title

    # <API function>
    @property
    def id_int(self) -> int:
        return self._tag_id_int
        # -Please note that it's the tag ID that's returned here

    # <API function>
    @property
    def title_str(self) -> str:
        return self._tag_title_str
        # -Please note that it's the tag title that's returned here
        # -alternatively we can use the tag_id to look this up

    # <API function>
    @staticmethod
    def get_all() -> List[TagsSelectedForEntryM]:
        # selecting custom columns here, for matching the init function above
        db_cursor_result = wbd.db.db_exec(
            "SELECT " + wbd.db.DbSchemaM.TagEntryRelationTable.name + "." + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
            + ", " + wbd.db.DbSchemaM.TagEntryRelationTable.name + "." + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.title
            + " FROM " + wbd.db.DbSchemaM.TagEntryRelationTable.name
            + " LEFT JOIN " + wbd.db.DbSchemaM.TagTable.name
            + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
            + " WHERE " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref + " = ?"
            + " ORDER BY " + wbd.db.DbSchemaM.TagEntryRelationTable.name + "." + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.sort_order,
            (wbd.wbd_global.active_state.last_entry(),)
        )
        # -Please note that wbd.wbd_global.active_state.view_id is used here!
        db_te_list = db_cursor_result.fetchall()

        ret_tags_selected_for_entry_list: List[TagsSelectedForEntryM] = []
        for db_te in db_te_list:
            tag_selected_for_entry = TagsSelectedForEntryM(*db_te)
            ret_tags_selected_for_entry_list.append(tag_selected_for_entry)

        logging.debug("ret_tags_selected_for_entry_list = " + str(ret_tags_selected_for_entry_list))
        return ret_tags_selected_for_entry_list

    # <API function>
    @staticmethod
    def get(i_tag_id: int) -> TagsSelectedForEntryM:
        # selecting custom columns here, for matching the init function above
        db_cursor_result = wbd.db.db_exec(
            "SELECT " + wbd.db.DbSchemaM.TagEntryRelationTable.name + "." + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
            + ", " + wbd.db.DbSchemaM.TagEntryRelationTable.name + "." + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.title
            + " FROM " + wbd.db.DbSchemaM.TagEntryRelationTable.name
            + " LEFT JOIN " + wbd.db.DbSchemaM.TagTable.name
            + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
            + " WHERE " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref + " = ?"
            + " AND " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref + " = ?",
            (wbd.wbd_global.active_state.last_entry(), i_tag_id)
        )
        # -Please note that wbd.wbd_global.active_state.view_id is used here!
        db_te = db_cursor_result.fetchone()[0]

        ret_tag_selected_for_entry: TagsSelectedForEntryM = TagInsideViewM(*db_te)

        logging.debug("ret_tag_selected_for_entry = " + str(ret_tag_selected_for_entry))
        return ret_tag_selected_for_entry

    # <API function>
    @staticmethod
    def remove(i_id: int):
        TagM.remove(i_id)


class TagInsideViewM:
    """
    Please note that there is a different between this class and the TagM, EntryM, QuestionM, etc classes:
    In this class there isn't a direct connection between the database and the class variables (for example see the
    get_all function below)
    """

    def __init__(self, i_tag_id: int, i_sort_order: int, i_tag_title: str):
        #######self._view_id_int = i_view_id
        ####i_view_id: int,
        self._tag_id_int = i_tag_id
        self.sort_order_int = i_sort_order
        self._tag_title_str = i_tag_title

    # <API function>
    @property
    def id_int(self) -> int:
        return self._tag_id_int
        # -Please note that it's the tag ID that's returned here

    # <API function>
    @property
    def title_str(self) -> str:
        return self._tag_title_str
        # -Please note that it's the tag title that's returned here
        # -alternatively we can use the tag_id to look this up

    # <API function>
    @staticmethod
    def get_all() -> List[TagInsideViewM]:
        # selecting custom columns here, for matching the init function above
        db_cursor_result = wbd.db.db_exec(
            "SELECT " + wbd.db.DbSchemaM.ViewTagRelationTable.name + "." + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref
            + ", " + wbd.db.DbSchemaM.ViewTagRelationTable.name + "." + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.title
            + " FROM " + wbd.db.DbSchemaM.ViewTagRelationTable.name
            + " LEFT JOIN " + wbd.db.DbSchemaM.TagTable.name
            + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " = " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref
            + " WHERE " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.view_id_ref + " = ?"
            + " ORDER BY " + wbd.db.DbSchemaM.ViewTagRelationTable.name + "." + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.sort_order,
            (wbd.wbd_global.active_state.view_id,)
        )
        # -Please note that wbd.wbd_global.active_state.view_id is used here!
        db_te_list = db_cursor_result.fetchall()

        ret_tag_inside_view_list: List[TagInsideViewM] = []
        for db_te in db_te_list:
            tag_inside_view = TagInsideViewM(*db_te)
            ret_tag_inside_view_list.append(tag_inside_view)

        logging.debug("ret_tag_inside_view_list = " + str(ret_tag_inside_view_list))
        return ret_tag_inside_view_list

    # <API function>
    @staticmethod
    def get(i_tag_id: int) -> TagInsideViewM:
        # selecting custom columns here, for matching the init function above
        db_cursor_result = wbd.db.db_exec(
            "SELECT " + wbd.db.DbSchemaM.ViewTagRelationTable.name + "." + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref
            + ", " + wbd.db.DbSchemaM.ViewTagRelationTable.name + "." + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.sort_order
            + ", " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.title
            + " FROM " + wbd.db.DbSchemaM.ViewTagRelationTable.name
            + " LEFT JOIN " + wbd.db.DbSchemaM.TagTable.name
            + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id + " = " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref
            + " WHERE " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.view_id_ref + " = ?"
            + " AND " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref + " = ?",
            (wbd.wbd_global.active_state.view_id, i_tag_id)
        )
        # -Please note that wbd.wbd_global.active_state.view_id is used here!
        db_te = db_cursor_result.fetchone()[0]

        ret_tag_inside_view: TagInsideViewM = TagInsideViewM(*db_te)

        logging.debug("ret_tag_inside_view = " + str(ret_tag_inside_view))
        return ret_tag_inside_view

    # <API function>
    @staticmethod
    def update_sort_order(i_id: int, i_sort_order: int) -> None:
        wbd.db.db_exec(
            "UPDATE " + wbd.db.DbSchemaM.ViewTagRelationTable.name
            + " SET " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.sort_order + " = ?"
            + " WHERE " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref + " = ?"
            + " AND " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.view_id_ref + " = ?",
            (i_sort_order, i_id, wbd.wbd_global.active_state.view_id)
        )


# ===== Relations =====


def get_all_tags_referenced_by_view(i_view_id: int) -> (ViewM, int):
    db_cursor_result = wbd.db.db_exec(
        "SELECT " + wbd.db.DbSchemaM.TagTable.name + ".*"
        + ", " + wbd.db.DbSchemaM.ViewTagRelationTable.name + "."
        + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.sort_order
        + " FROM " + wbd.db.DbSchemaM.TagTable.name
        + " INNER JOIN " + wbd.db.DbSchemaM.ViewTagRelationTable.name
        + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id
        + " = " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref
        + " WHERE " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.view_id_ref + " = ?",
        (i_view_id,)
    )
    db_te_list = db_cursor_result.fetchall()

    ret_tags_and_sort_order_list: List[Tuple[TagM, int]] = []
    for db_te in db_te_list:
        tag = TagM(*db_te[:-1])
        sort_order_int = db_te[-1]
        tags_and_sort_order_tuple = (tag, sort_order_int)
        ret_tags_and_sort_order_list.append(tags_and_sort_order_tuple)

    logging.debug("ret_tags_and_sort_order_list = " + str(ret_tags_and_sort_order_list))
    return ret_tags_and_sort_order_list


def add_view_tag_relation(i_view_id: int, i_tag_id: int):
    logging.debug("add_view_tag_relation i_view_id = " + str(i_view_id) + " i_tag_id = " + str(i_tag_id))
    # sort_order = len(get_all_filter_presets())
    # print("sort_order = " + str(sort_order))
    sort_order_int = 1  # -TODO
    wbd.db.db_exec(
        "INSERT OR IGNORE INTO " + wbd.db.DbSchemaM.ViewTagRelationTable.name
        + "(" + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.view_id_ref
        + ", " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref
        + ", " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.sort_order
        + ") VALUES (?, ?, ?)",
        (i_view_id, i_tag_id, sort_order_int)
    )
    # -please note that it's important to use _ref in the TagEntryRelationTable rather than using
    #  the id's referenced directly
    # -please note "or ignore" which has been added in case the value already exists
    # -question: do we want to use "or ignore" here or is it better to catch the problem in the GUI code?


def remove_view_tag_relation(i_view_id: int, i_tag_id: int):
    logging.debug("remove_view_tag_relation i_view_id = " + str(i_view_id) + " i_tag_id = " + str(i_tag_id))

    wbd.db.db_exec(
        "DELETE FROM " + wbd.db.DbSchemaM.ViewTagRelationTable.name
        + " WHERE " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.view_id_ref + " = ?"
        + " AND " + wbd.db.DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref + " = ?",
        (i_view_id, i_tag_id)
    )


def remove_tag_question_relation(i_tag_id: int, i_question_id: int):
    logging.debug("remove_tag_question_relation i_tag_id = " + str(i_tag_id) + " i_question_id = " + str(i_question_id))

    wbd.db.db_exec(
        "DELETE FROM " + wbd.db.DbSchemaM.TagQuestionRelationTable.name
        + " WHERE " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_id_ref + " = ?"
        + " AND " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.question_id_ref + " = ?",
        (i_tag_id, i_question_id)
    )


def add_tag_question_relation(i_tag_id: int, i_question_id: int, i_tag_is_preselected: bool) -> bool:
    logging.debug("add_tag_question_relation i_tag_id = " + str(i_tag_id) + " i_question_id = " + str(i_question_id))

    # Checking if there is already a relation between these two
    db_cursor_result = wbd.db.db_exec(
        "SELECT *"
        + " FROM " + wbd.db.DbSchemaM.TagQuestionRelationTable.name
        + " WHERE " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_id_ref + " = ?"
        + " AND " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.question_id_ref + " = ?",
        (i_tag_id, i_question_id)
    )
    db_te_list = db_cursor_result.fetchall()
    if len(db_te_list) > 0:
        logging.debug("add_tag_question_relation - Relation already exists, exiting")
        return False

    # Adding a new relation
    tag_is_preselected_as_int = wbd.db.SQLITE_FALSE
    if i_tag_is_preselected:
        tag_is_preselected_as_int = wbd.db.SQLITE_TRUE
    wbd.db.db_exec(
        "INSERT INTO " + wbd.db.DbSchemaM.TagQuestionRelationTable.name
        + "(" + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_id_ref
        + ", " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.question_id_ref
        + ", " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_is_preselected
        + ") VALUES (?, ?, ?)",
        (i_tag_id, i_question_id, tag_is_preselected_as_int)
    )
    # -please note that it's important to use _ref in the TagQuestionRelationTable rather than using
    #  the id's referenced directly
    return True


def add_tag_entry_relation(i_tag_id: int, i_entry_id: int):
    logging.debug("add_tag_entry_relation i_tag_id = " + str(i_tag_id) + " i_entry_id = " + str(i_entry_id))
    sort_order_int = 0
    wbd.db.db_exec(
        "INSERT OR IGNORE INTO " + wbd.db.DbSchemaM.TagEntryRelationTable.name
        + "(" + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
        + ", " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref
        + ", " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.sort_order
        + ") VALUES (?, ?, ?)",
        (i_tag_id, i_entry_id, sort_order_int)
    )
    # -please note that it's important to use _ref in the TagEntryRelationTable rather than using
    #  the id's referenced directly
    # TODO: Limit so that only one combination of tag and entry can be there


def remove_all_tag_relations_for_entry(i_entry_id: int):
    logging.debug("remove_all_tag_relations_for_entry " + " i_entry_id = " + str(i_entry_id))
    wbd.db.db_exec(
        "DELETE FROM " + wbd.db.DbSchemaM.TagEntryRelationTable.name
        + " WHERE " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref + "=?",
        (i_entry_id,)
    )


def remove_all_tag_relations_for_question(i_question_id: int) -> None:
    logging.debug("remove_all_tag_relations_for_question " + " i_question_id = " + str(i_question_id))
    wbd.db.db_exec(
        "DELETE FROM " + wbd.db.DbSchemaM.TagQuestionRelationTable.name
        + " WHERE " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.question_id_ref + "=?",
        (i_question_id,)
    )


def get_all_tags_referenced_by_question(i_question_id: int) -> (TagM, bool):
    db_cursor_result = wbd.db.db_exec(
        "SELECT " + wbd.db.DbSchemaM.TagTable.name + ".*"
        + ", " + wbd.db.DbSchemaM.TagQuestionRelationTable.name + "."
        + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_is_preselected
        + " FROM " + wbd.db.DbSchemaM.TagTable.name
        + " INNER JOIN " + wbd.db.DbSchemaM.TagQuestionRelationTable.name
        + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id
        + " = " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.tag_id_ref
        + " WHERE " + wbd.db.DbSchemaM.TagQuestionRelationTable.Cols.question_id_ref + " = ?",
        (i_question_id,)
    )
    db_te_list = db_cursor_result.fetchall()

    # [:-1] [-1]
    ret_tags_and_preselected_list: List[Tuple[TagM, bool]] = []
    for db_te in db_te_list:
        tag = TagM(*db_te[:-1])
        preselected_bool = False
        preselected_as_int = db_te[-1]
        if preselected_as_int == wbd.db.SQLITE_TRUE:
            preselected_bool = True
        tags_and_preselected_tuple = (tag, preselected_as_int)
        ret_tags_and_preselected_list.append(tags_and_preselected_tuple)

    # ret_tags_and_preselected_list = [(TagM(*db_te[:-1]), db_te[-1]) for db_te in db_te_list]
    logging.debug("ret_tags_and_preselected_list = " + str(ret_tags_and_preselected_list))
    return ret_tags_and_preselected_list


def get_all_tags_referenced_by_entry(i_entry_id: int) -> List[TagM]:
    db_cursor_result = wbd.db.db_exec(
        "SELECT " + wbd.db.DbSchemaM.TagTable.name + ".*"
        + " FROM " + wbd.db.DbSchemaM.TagTable.name
        + " INNER JOIN " + wbd.db.DbSchemaM.TagEntryRelationTable.name
        + " ON " + wbd.db.DbSchemaM.TagTable.name + "." + wbd.db.DbSchemaM.TagTable.Cols.id
        + " = " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref
        + " WHERE " + wbd.db.DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref + " = ?",
        (i_entry_id,)
    )
    tag_db_te_list = db_cursor_result.fetchall()
    ret_tags_list = [TagM(*tag_db_te) for tag_db_te in tag_db_te_list]
    # logging.debug("ret_tags_list = " + str(ret_tags_list))
    return ret_tags_list


class ExportTypeEnum(enum.Enum):
    active_filters = 0
    all = 1


TAG_IMPORT_EXPORT_SEPARATOR_STR = "; "
# TODO: Excluding this from possible/allowed tag titles


CSV_SUFFIX_STR = ".csv"
EXPORTED_ENTRIES_SUFFIX_STR = "_exported_entries.csv"
EXPORTED_QUESTIONS_SUFFIX_STR = "_exported_questions.csv"
EXPORTED_TAGS_SUFFIX_STR = "_exported_tags.csv"

ATTRIBUTE_IMAGE_FILE_NAME_STR = "image_file_name"

NO_IMAGE_FOR_ENTRY_STR = ""
JPEG_FILE_SUFFIX_STR = ".jpg"


def export_to_csv(i_type: ExportTypeEnum):
    # If we want to automate this:
    # https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python

    export_path_str = wbd.wbd_global.get_user_exported_path()

    entry_export_import_field_name_list = [
        wbd.db.DbSchemaM.EntryTable.Cols.datetime_added,
        wbd.db.DbSchemaM.EntryTable.Cols.rating,
        wbd.db.DbSchemaM.TagTable.Cols.title,
        ATTRIBUTE_IMAGE_FILE_NAME_STR,
        wbd.db.DbSchemaM.EntryTable.Cols.text
    ]

    now_time_datetime = datetime.datetime.now()
    now_date_str = now_time_datetime.strftime(wbd.wbd_global.PY_DATETIME_FILENAME_FORMAT_STR)

    # Entries

    file_name_str = now_date_str + EXPORTED_ENTRIES_SUFFIX_STR
    file_path_str = wbd.wbd_global.get_user_exported_path(file_name_str)
    with open(file_path_str, "w") as f:
        csv_dict_writer = csv.DictWriter(f, fieldnames=entry_export_import_field_name_list)
        csv_dict_writer.writeheader()

        diary_entry_list: List[EntryM] = []
        if i_type == ExportTypeEnum.active_filters:
            (diary_entry_list, _) = EntryM.get_entry_list_and_max_page_nr(
                wbd.wbd_global.active_state.filters.tag_active_bool,
                wbd.wbd_global.active_state.filters.tag_id_int,
                wbd.wbd_global.active_state.filters.search_active_bool,
                wbd.wbd_global.active_state.filters.search_term_str,
                wbd.wbd_global.active_state.filters.rating_active_bool,
                wbd.wbd_global.active_state.filters.rating_int,
                wbd.wbd_global.active_state.filters.datetime_active_bool,
                wbd.wbd_global.active_state.filters.start_datetime_string,
                wbd.wbd_global.active_state.filters.end_datetime_string,
                ALL_ENTRIES_NO_PAGINATION_INT
            )
        elif i_type == ExportTypeEnum.all:
            (diary_entry_list, _) = EntryM.get_entry_list_and_max_page_nr(
                False, wbd.wbd_global.NO_ACTIVE_TAG_INT,
                False, "",
                False, 0,
                False, wbd.wbd_global.DATETIME_NOT_SET_STR, wbd.wbd_global.DATETIME_NOT_SET_STR,
                ALL_ENTRIES_NO_PAGINATION_INT
            )

        for diary_entry in diary_entry_list:
            # time_datetime = datetime.date.fromtimestamp(diary_entry.date_added_it)
            # datetime_str = time_datetime.strftime(IMPORT_EXPORT_DATE_FORMAT_STR)
            datetime_str = diary_entry.datetime_added_str

            # Tags
            tag_list: List[TagM] = get_all_tags_referenced_by_entry(diary_entry.id)
            tag_titles_list = [tag.title_str for tag in tag_list]
            tags_string_str = TAG_IMPORT_EXPORT_SEPARATOR_STR.join(tag_titles_list)

            # Image exported to file
            image_name_str = NO_IMAGE_FOR_ENTRY_STR
            if diary_entry.image_file_bytes is not None:
                hash_str = hashlib.md5(diary_entry.image_file_bytes).hexdigest()
                if "T" in datetime_str:
                    date_str = datetime_str.split("T")[0]
                elif " " in datetime_str:
                    # Just in case
                    date_str = datetime_str.split(" ")[0]
                else:
                    # When there is only a date for the image
                    date_str = datetime_str
                image_name_str = date_str + "_" + hash_str + JPEG_FILE_SUFFIX_STR
                image_path_str = wbd.wbd_global.get_user_exported_images_path(image_name_str)
                with open(image_path_str, 'wb') as image_file:
                    # -the 'b' means that we are opening the file in binary mode
                    image_file.write(diary_entry.image_file_bytes)

            csv_dict_writer.writerow({
                wbd.db.DbSchemaM.EntryTable.Cols.datetime_added: datetime_str,
                wbd.db.DbSchemaM.EntryTable.Cols.rating: str(diary_entry.rating_int),
                wbd.db.DbSchemaM.TagTable.Cols.title: tags_string_str,
                ATTRIBUTE_IMAGE_FILE_NAME_STR: image_name_str,
                wbd.db.DbSchemaM.EntryTable.Cols.text: diary_entry.diary_text_str
            })

            """
            if diary_entry.image_file_bytes is not None:
                image_file_path_str = wbd.wbd_global.process_and_get_image_file_path_from_bytes(diary_entry.image_file_bytes)
                logging.debug("image_file_path_str = " + image_file_path_str)
            """
        wbd.wbd_global.removing_oldest_files(export_path_str, EXPORTED_ENTRIES_SUFFIX_STR, 3)
    file_size_in_bytes_int = os.path.getsize(file_path_str)
    if file_size_in_bytes_int < 1:
        wbd.exception_handling.warning(
            "Problem with backup",
            "Something probably went wrong, the file size is just " + str(file_size_in_bytes_int) + " bytes"
        )

    # Questions

    file_name_str = now_date_str + EXPORTED_QUESTIONS_SUFFIX_STR
    file_path_str = wbd.wbd_global.get_user_exported_path(file_name_str)
    with open(file_path_str, "w") as f:
        csv_writer = csv.writer(f)
        for question_item in QuestionM.get_all():
            csv_writer.writerow((question_item.title_str, question_item.description_str))
        wbd.wbd_global.removing_oldest_files(export_path_str, EXPORTED_QUESTIONS_SUFFIX_STR, 3)
    file_size_in_bytes_int = os.path.getsize(file_path_str)
    if file_size_in_bytes_int < 1:
        wbd.exception_handling.warning(
            "Problem with backup",
            "Something probably went wrong, the file size is just " + str(file_size_in_bytes_int) + " bytes"
        )

    # Tags

    file_name_str = now_date_str + EXPORTED_TAGS_SUFFIX_STR
    file_path_str = wbd.wbd_global.get_user_exported_path(file_name_str)
    with open(file_path_str, "w") as f:
        csv_writer = csv.writer(f)
        for tag_item in TagM.get_all():
            csv_writer.writerow((tag_item.title_str, tag_item.description_str))
        # file size cannot be trusted here, maybe because
    file_size_in_bytes_int = os.path.getsize(file_path_str)
    if file_size_in_bytes_int < 1:
        wbd.exception_handling.warning(
            "Problem with backup",
            "Something probably went wrong, the file size is just " + str(file_size_in_bytes_int) + " bytes"
        )
    wbd.wbd_global.removing_oldest_files(export_path_str, EXPORTED_TAGS_SUFFIX_STR, 3)

    wbd.wbd_global.open_directory(export_path_str)


DEFAULT_DATETIME_STR = "1900-01-01T00:00:00"


# "date not found"


def import_entries_from_csv(i_csv_file_path: str) -> None:
    read_file = open(i_csv_file_path, newline='')
    csv_reader = csv.DictReader(read_file)
    for csv_row_od in csv_reader:
        # -new in Python 3.6: Rows are OrderedDicts
        tag_id_list = []
        datetime_str = DEFAULT_DATETIME_STR
        rating_int = 1  # default
        text_str = ""  # default
        image_file_bytes = None

        image_dir_path_str = wbd.wbd_global.get_user_exported_images_path()
        image_files_list = os.listdir(image_dir_path_str)
        image_file_name_str = NO_IMAGE_FOR_ENTRY_STR

        ####image_available_bool = False
        for attribute_str in csv_row_od:
            raw_value_str = csv_row_od[attribute_str]
            if attribute_str == wbd.db.DbSchemaM.EntryTable.Cols.datetime_added:
                # entry_time_pydatetime = datetime.datetime.strptime(raw_value_str, IMPORT_EXPORT_DATE_FORMAT_STR)
                datetime_str = raw_value_str
            elif attribute_str == wbd.db.DbSchemaM.EntryTable.Cols.rating:
                rating_int = int(raw_value_str)
            elif attribute_str == wbd.db.DbSchemaM.TagTable.Cols.title:
                all_tag_titles_str: str = raw_value_str
                if all_tag_titles_str:
                    tag_title_list = all_tag_titles_str.split(TAG_IMPORT_EXPORT_SEPARATOR_STR)
                    for tag_title_str in tag_title_list:
                        if TagM.tag_with_title_exists(tag_title_str):
                            existing_tag = TagM.get_by_title(tag_title_str)
                            tag_id_list.append(existing_tag.id_int)
                        else:
                            new_tag_id = TagM.add(tag_title_str, "")
                            tag_id_list.append(new_tag_id)
            elif attribute_str == wbd.db.DbSchemaM.EntryTable.Cols.text:
                text_str = raw_value_str
            elif attribute_str == ATTRIBUTE_IMAGE_FILE_NAME_STR:
                image_file_name_str = raw_value_str
                if image_file_name_str != NO_IMAGE_FOR_ENTRY_STR:
                    image_file_path_str = wbd.wbd_global.get_user_exported_images_path(image_file_name_str)
                    image_file_bytes = wbd.wbd_global.jpg_image_file_to_bytes(image_file_path_str)
                    """
                    image_name_ending_str = image_date_and_hash_str + JPEG_FILE_SUFFIX_STR
                    image_file_name_str = ""
                    for file_name_str in image_files_list:
                        if file_name_str.endswith(image_name_ending_str):
                            image_file_name_str = file_name_str
                    """
                    # image_available_bool = True
            else:
                pass  # -not recognized

        # if image_available_bool:

        new_entry_id_int = EntryM.add(
            datetime_str,
            i_diary_text=text_str,
            i_image_file=image_file_bytes,
            i_rating=rating_int
        )
        for tag_id in tag_id_list:
            add_tag_entry_relation(tag_id, new_entry_id_int)


def my_datetime_function(i_days_previous: int = 0, i_hour: int = -1) -> (bool, int, str):
    now_pdt = datetime.datetime.now()
    datetime_pdt: datetime.datetime = now_pdt
    datetime_pdt = datetime_pdt - datetime.timedelta(days=i_days_previous)
    if i_hour == -1:
        datetime_as_iso_str = datetime_pdt.strftime(wbd.wbd_global.PY_DATE_ONLY_FORMAT_STR)
    else:
        hour_int = i_hour
        datetime_pdt = datetime_pdt.replace(hour=hour_int, minute=0, second=0)
        datetime_as_iso_str = datetime_pdt.strftime(wbd.wbd_global.PY_DATETIME_FORMAT_STR)
    ret_tuple = (datetime_as_iso_str, 0)
    return ret_tuple


# noinspection PyTypeChecker
def populate_db(i_testing: bool):
    # Populating with setup data

    # Tags

    contribution_tag_id_int = TagM.add("Contribution", "Contribution and generosity")

    """
    TODO:
    * insight
    * reflection
    * rememberance
      * gratitude
    * encouragement    
    """

    interbeing_tag_id_int = TagM.add("Inter-being", '"This is because that is"')
    impermanence_tag_id_int = TagM.add("Impermanence", "Things are always changing")

    meaning_tag_id_int = TagM.add("Meaning", "")
    growth_tag_id_int = TagM.add("Growth", "")
    connection_tag_id_int = TagM.add("Connection", "")
    kindness_tag_id_int = TagM.add("Kindness", "")
    play_tag_id_int = TagM.add("Play and fun", "")
    to_be_seen_tag_id_int = TagM.add("To be seen", "")

    insight_tag_id_int = TagM.add("Insight", "")
    reflection_tag_id_int = TagM.add("Reflection", "")
    encouragement_tag_id_int = TagM.add("Encouragement", "")
    thinking_tag_id_int = TagM.add("Thinking", "")
    speech_tag_id_int = TagM.add("Speech", "")
    action_tag_id_int = TagM.add("Action", "Bodily actions. Ex:_")
    # -splitting this into three parts?
    # -does this cover negative thinking for example?

    wisdom_tag_id_int = TagM.add("Wisdom", ".... There are some aspects to wisdom:\n"
                                           "1. Spending time listening to wise people\n2. Remembering\n3. Contempating\n4. Putting into practice"
                                 )

    greed_tag_id_int = TagM.add("Greed", "Expectations")
    illwill_tag_id_int = TagM.add("Ill-will", "Anger, hatred, ill-will")
    delusion_tag_id_int = TagM.add("Delusion", "Ignorance, delusion")
    anxiety_tag_id_int = TagM.add("Anxiety", "Anxiety description")
    tired_tag_id_int = TagM.add("Tired", "")

    mindfulness_tag_id_int = TagM.add("Mindfulness", "There are four foundations of mindfulness: "
                                                     "1. Body 2. Feelings 3. Mind 4. Objects of Mind"
                                      )
    love_tag_id_int = TagM.add("Love", "Loving-kindness for myself and others")
    compassion_tag_id_int = TagM.add("Compassion", "Compassion for myself and others")
    joy_tag_id_int = TagM.add("Joy", "Joy and sympathetic joy (sharing the joy of others)")
    peace_tag_id_int = TagM.add("Peace", "Peace, equanimity, non-discrimination")

    # kind_actions_id_tag_int = TagM.add_tag("Love", "Loving-kindness for myself and others")

    suffering_tag_id_int = TagM.add("Suffering", "Pain and suffering (which often has mental causes and conditions)")
    selfcompassion_tag_id_int = TagM.add("Self-compassion", "Self-compassion description")
    refuge_tag_id_int = TagM.add("Refuge",
                                 "Ex: Taking refuge in self-compassion, or in mindfulness, or people you trust")

    gratitude_tag_id_int = TagM.add("Gratitude", "Some recurring things I am grateful for:\n"
                                                 "* Breathing\n* Nature\n* Please continue to fill this list"
                                    )
    # https://accesstoinsight.org/tipitaka/kn/khp/khp.5.nara.html

    nature_tag_id_int = TagM.add("Nature", "Being out in nature, getting fresh air and sunshine")
    exercise_tag_id_int = TagM.add("Exercise", "Moving the body and staying fit")

    # mindful_walking_tag_id_int = TagM.add_tag("Mindful walking", "Mindfulness description")
    # mindful_breathing_tag_id_int = TagM.add_tag("Mindful breathing", "Mindfulness description")

    # mind_cultivation_tag_id_int = TagM.add_tag("Mind cultivation","mind cultivation description")

    # N8P
    # x view / wisdom
    # thinking / intention
    # speech
    # action
    # livelihood
    # diligence
    # x mindfulness
    # concentration

    # Views

    entry_type_view_id_int = ViewM.add("Entry Type")
    add_view_tag_relation(entry_type_view_id_int, insight_tag_id_int)
    add_view_tag_relation(entry_type_view_id_int, reflection_tag_id_int)
    add_view_tag_relation(entry_type_view_id_int, encouragement_tag_id_int)
    add_view_tag_relation(entry_type_view_id_int, thinking_tag_id_int)
    add_view_tag_relation(entry_type_view_id_int, speech_tag_id_int)
    add_view_tag_relation(entry_type_view_id_int, action_tag_id_int)

    state_of_mind_view_id_int = ViewM.add("States of mind")
    add_view_tag_relation(state_of_mind_view_id_int, anxiety_tag_id_int)
    add_view_tag_relation(state_of_mind_view_id_int, tired_tag_id_int)
    add_view_tag_relation(state_of_mind_view_id_int, greed_tag_id_int)
    add_view_tag_relation(state_of_mind_view_id_int, illwill_tag_id_int)
    add_view_tag_relation(state_of_mind_view_id_int, delusion_tag_id_int)
    add_view_tag_relation(state_of_mind_view_id_int, love_tag_id_int)
    add_view_tag_relation(state_of_mind_view_id_int, compassion_tag_id_int)
    add_view_tag_relation(state_of_mind_view_id_int, joy_tag_id_int)
    add_view_tag_relation(state_of_mind_view_id_int, peace_tag_id_int)

    needs_view_id_int = ViewM.add("Needs")
    add_view_tag_relation(needs_view_id_int, connection_tag_id_int)
    add_view_tag_relation(needs_view_id_int, meaning_tag_id_int)
    add_view_tag_relation(needs_view_id_int, growth_tag_id_int)
    add_view_tag_relation(needs_view_id_int, kindness_tag_id_int)
    add_view_tag_relation(needs_view_id_int, play_tag_id_int)
    add_view_tag_relation(needs_view_id_int, to_be_seen_tag_id_int)

    gratitudes_view_id_int = ViewM.add("Gratitudes")
    # add_view_tag_relation(gratitudes_view_id_int, connection_tag_id_int)
    # add_view_tag_relation(gratitudes_view_id_int, connection_tag_id_int)

    # places_view_id_int = ViewM.add_view("Places")

    friends_view_id_int = ViewM.add("Friends")
    # add_view_tag_relation(friends_view_id_int, love_tag_id_int)
    # add_view_tag_relation(friends_view_id_int, compassion_tag_id_int)
    # -Maybe removing these two tags?
    # -TODO: Wizard for adding friends

    # inter_being_view_id_int = ViewM.add_view("Inter-being")

    # n8p_view_id_int = ViewM.add_view("Noble 8-fold Path")
    # add_view_tag_relation(n8p_view_id_int, wisdom_tag_id_int)

    # Filter presets

    FilterPresetM.add(
        "Rating >= 1",
        False, wbd.wbd_global.NO_ACTIVE_TAG_INT,
        False, "",
        True, 1,
        False, wbd.wbd_global.DATETIME_NOT_SET_STR, wbd.wbd_global.DATETIME_NOT_SET_STR
    )
    FilterPresetM.add(
        "Gratitude",
        True, gratitude_tag_id_int,
        False, "",
        False, 0,
        False, wbd.wbd_global.DATETIME_NOT_SET_STR, wbd.wbd_global.DATETIME_NOT_SET_STR
    )

    # Questions

    kindness_q_id_int = QuestionM.add(
        "Kindness?",
        "What acts of kindness did I see today?"
        "(Could be towards me or between other people, or in a film or tv series)"
    )
    add_tag_question_relation(love_tag_id_int, kindness_q_id_int, False)
    add_tag_question_relation(compassion_tag_id_int, kindness_q_id_int, False)

    # ..mental food
    mental_food_q_id_int = QuestionM.add(
        "What mental food did i take in?",
        "What mental food did i take in? What's one thing I did to cultivate loving kindness, compassion, "
        "joy or equanimity today? "
    )
    add_tag_question_relation(love_tag_id_int, mental_food_q_id_int, False)
    add_tag_question_relation(compassion_tag_id_int, mental_food_q_id_int, False)
    add_tag_question_relation(joy_tag_id_int, mental_food_q_id_int, False)
    add_tag_question_relation(peace_tag_id_int, mental_food_q_id_int, False)
    add_tag_question_relation(interbeing_tag_id_int, mental_food_q_id_int, False)

    # ..gratitude
    gratitude_q_id_int = QuestionM.add(
        "Gratitude",
        "What's one thing I am grateful for today? It may be something ordinary, something i see every day, "
        "or it may be something unusual. It could be a small thing or a big thing. It can be freedom from suffering."
    )
    add_tag_question_relation(gratitude_tag_id_int, gratitude_q_id_int, True)
    # add_tag_question_relation(interbeing_tag_id_int, gratitude_q_id_int, False)
    # TODO: Adding more tags here like for example: family, friends, health
    # possibly having a wizard where the user is asked what she is grateful for

    contribution_q_id_int = QuestionM.add(
        "Contributing and supporting others",
        "What's one thing I did to support or contribute to the well-being of another person today? It might be "
        "something material or practical, or listening to someone, or setting a positive intention which will effect "
        "how I interact with this person in the future."
    )
    add_tag_question_relation(contribution_tag_id_int, contribution_q_id_int, True)

    connection_q_id_int = QuestionM.add(
        "Connection to other people and to the world",
        "What are some things that i did that are important to other people? It could be a thing as "
        "simple as staying aware of my breathing, being peaceful, etc. Did I remember that I am practicing "
        "for everyone and not just myself? Did I see that my way of being will model a way for others also?"
    )
    add_tag_question_relation(interbeing_tag_id_int, connection_q_id_int, True)
    # TODO: We could have friends and family members here through a wizard which asks about these

    activities_of_friends_q_id_int = QuestionM.add(
        "Activities of friends and family",
        "What one thing a friend or family member did? What was enjoyable for them today, and what was difficult?"
    )
    add_tag_question_relation(interbeing_tag_id_int, connection_q_id_int, True)

    # ..suffering
    suffering_q_id_int = QuestionM.add(
        "Difficulties/suffering",
        "What's one difficult thing that happened to me today?\n"
        "* How did it feel in the body? What feelings were there?\n"
        "* (Anxiety?) What are some other people with similar problems?\n"
        "* How did I give care and compassion to myself?\n"
        "* Where can I go for refuge?\n"
        "* If something similar happens to a friend or family member, how would I help them?\n"
        "Please write in a kind way, as if writing to a dear friend."
    )
    add_tag_question_relation(suffering_tag_id_int, suffering_tag_id_int, True)
    add_tag_question_relation(selfcompassion_tag_id_int, suffering_q_id_int, True)
    add_tag_question_relation(refuge_tag_id_int, suffering_q_id_int, False)
    add_tag_question_relation(anxiety_tag_id_int, suffering_q_id_int, False)
    add_tag_question_relation(greed_tag_id_int, suffering_q_id_int, False)
    add_tag_question_relation(illwill_tag_id_int, suffering_q_id_int, False)
    add_tag_question_relation(delusion_tag_id_int, suffering_q_id_int, False)

    # ..mindfulness
    mindfulness_q_id_int = QuestionM.add(
        "Mindfulness",
        "Was I able to stay mindful of my steps when walking outside and inside? How many steps did I take for each "
        "breath? Could i maintain my mindfulness of breathing for long periods of time? In one of my daily "
        "activities, did I (in the moment) remember my connection to other people and to the world?"
    )
    add_tag_question_relation(mindfulness_tag_id_int, mindfulness_q_id_int, True)
    add_tag_question_relation(interbeing_tag_id_int, mindfulness_q_id_int, False)
    # breathing, walking

    learning_q_id_int = QuestionM.add(
        "Learning something helpful",
        "What's one thing that I learned today that I can take with me and that could help me increase happiness and "
        "peace, and reduce suffering?"
    )
    add_tag_question_relation(wisdom_tag_id_int, learning_q_id_int, True)

    # Populating with additional test data

    if i_testing:
        friend_1_tag_id_int = TagM.add("Friend 1", "Description")
        dharma_talk_tag_id_int = TagM.add("Dharma talk", "Description")
        # father_tag_id_int = TagM.add_tag("Father", "Description")
        # mother_tag_id_int = TagM.add_tag("Mother", "Description")

        # Entries

        datetime_tuple = my_datetime_function(0)
        entry_str = "Today i practiced sitting meditation before meeting a friend of mine to be able to be more present during our meeting"
        entry_id = EntryM.add(*datetime_tuple, entry_str)
        add_tag_entry_relation(mindfulness_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(0, 13)
        entry_str = "I'm grateful for being able to breathe!"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 3)
        add_tag_entry_relation(gratitude_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(1, 20)
        entry_str = "Most difficult today was my negative thinking, practicing with this by changing the peg from negative thoughts to positive thinking, remembering many people are struggling with this, for example my friend x"
        entry_id = EntryM.add(*datetime_tuple, entry_str)
        add_tag_entry_relation(selfcompassion_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(7)
        entry_str = "Grateful for having a place to live, a roof over my head, food to eat, and people to care for"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(gratitude_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(7)
        entry_str = "Grateful for the blue sky and the white clouds"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 2)
        add_tag_entry_relation(gratitude_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(3, 21)
        entry_str = "Today i read about the four foundations of mindfulness. Some important parts: 1. Body 2. Feelings 3. Mind 4. Objects of mind"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 2)
        add_tag_entry_relation(mindfulness_tag_id_int, entry_id)
        add_tag_entry_relation(wisdom_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(4, 19)
        entry_str = "Programming and working on the application. Using Python and Qt. Cooperating with x and y. Hope that this will benefit many people"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(contribution_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(4)
        entry_str = "Listened to a Dharma talk from Plum-Village, about inter-being and impermanence"
        entry_id = EntryM.add(*datetime_tuple, entry_str)
        add_tag_entry_relation(interbeing_tag_id_int, entry_id)
        add_tag_entry_relation(impermanence_tag_id_int, entry_id)
        add_tag_entry_relation(wisdom_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(4)
        entry_str = "Programming and working on the application. Using Python and Qt. Cooperating with x and y. Hope that this will benefit many people"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(contribution_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(4)
        entry_str = "Lied down under a tree, contemplating the branches and leaves"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(nature_tag_id_int, entry_id)
        add_tag_entry_relation(gratitude_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(4, 12)
        entry_str = "Seeing the moon rise over the treeline horizon in real-time!"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(nature_tag_id_int, entry_id)
        add_tag_entry_relation(gratitude_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(4, 15)
        entry_str = "Walking up to Masthuggskyrkan together with friend 1, and enjoying the scenery"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(friend_1_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(3)
        entry_str = "Helped friend 1 with ____"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(friend_1_tag_id_int, entry_id)
        add_tag_entry_relation(contribution_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(4)
        entry_str = "When lying awake with anxiety in bed i remembered Buddha, Dharma, Sangha and this helped me calm my mind"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(anxiety_tag_id_int, entry_id)
        add_tag_entry_relation(selfcompassion_tag_id_int, entry_id)
        add_tag_entry_relation(suffering_q_id_int, entry_id)

        datetime_tuple = my_datetime_function(4)
        entry_str = "Protected by the compassion i generated when listening to a Dhamma talk"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(compassion_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(4, 13)
        entry_str = "I can be true to my own feelings and not play a different role than what i am at that moment"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(wisdom_tag_id_int, entry_id)

        entry_str = (
            """Dharma talk 2018-11-05
            1. Awareness of our own body is the secret to meditation practice
            2. Mindfulness, concentration and insight can come when we practice awareness of our breathing, or when pouring tea
            3. The means are the end (ex: Peace walk with 500,000 people)
            Mindfulness -> Concentration -> Insight
            """
        )
        datetime_tuple = my_datetime_function(4)
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(dharma_talk_tag_id_int, entry_id)

        datetime_tuple = my_datetime_function(1, 13)
        entry_str = "On a walk in nature, wonderful air and sun!"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 2)
        add_tag_entry_relation(nature_tag_id_int, entry_id)
        raw_image_path_str = wbd.wbd_global.get_testing_images_path("DSC_1032.JPG")
        (image_bytes, _) = wbd.wbd_global.process_image(
            raw_image_path_str
        )
        EntryM.update_image(entry_id, image_bytes)

        datetime_tuple = my_datetime_function(1, 12)
        entry_str = "Path in nature"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 2)
        add_tag_entry_relation(nature_tag_id_int, entry_id)
        raw_image_path_str = wbd.wbd_global.get_testing_images_path("DSC_1098.JPG")
        (image_bytes, _) = wbd.wbd_global.process_image(
            raw_image_path_str
        )
        EntryM.update_image(entry_id, image_bytes)

        datetime_tuple = my_datetime_function(1)
        entry_str = "Is this link clickable? https://basket-notepads.github.io/screenshots.html"
        entry_id = EntryM.add(*datetime_tuple, entry_str, 1)
        add_tag_entry_relation(compassion_tag_id_int, entry_id)
