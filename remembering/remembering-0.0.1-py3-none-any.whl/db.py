import datetime
import logging
import os
import shutil
import sqlite3

SQLITE_FALSE = 0
SQLITE_TRUE = 1
SQLITE_NULL = "NULL"
NO_REFERENCE = -1
ALWAYS_AT_TOP_INT = -1


def get_schema_version(i_db_conn):
    t_cursor = i_db_conn.execute("PRAGMA user_version")
    return t_cursor.fetchone()[0]


def set_schema_version(i_db_conn, i_version_it):
    i_db_conn.execute("PRAGMA user_version={:d}".format(i_version_it))


def db_exec(i_sql_string: str, i_values: tuple) -> sqlite3.Cursor:
    # i_sql_string is required to hold VALUES(,) or "?"
    db_connection = DbHelperM.get_db_connection()
    db_cursor = db_connection.cursor()
    if isinstance(i_values, bytes):
        logging.debug("db_exec - i_sql_string = " + i_sql_string + " i_values = " + str(i_values))
    try:
        db_cursor = db_cursor.execute(
            i_sql_string,
            i_values
        )
    except sqlite3.IntegrityError:
        pass
        ###wbd.exception_handling.error("sqlite3.IntegrityError", "sqlite3.IntegrityError")
    db_connection.commit()
    return db_cursor


class DbSchemaM:
    # The reason that an integer is used as the key for the questions and tags rather than the title (which is unique)
    # is that we are storing the id in the relation tables, and we don't want to update these tables whenever the title
    # changes. Another reason for keeping the integer is that it's faster. The tables themselves doesn't have many
    # entries, but they are referenced in the relation tables, which can be large

    """

    self.permanent_bool = False

    self.next_notif_ts_int = NO_VALUE_SET_INT

    self.notif_spec_secs_list = []  # -please note that these are stored in secs (unix timestamp)
    self.notif_freq_secs_int = NO_VALUE_SET_INT  # -both of these are possible, though this may result in overlap

    self.notif_active_bool = True
    self.notif_fired_bool = False


    self.title_str = NO_VALUE_SET_STR

    self.content_type_enum = ContentType.not_set
    self.content_str = NO_VALUE_SET_STR  # -can be a text, a webpage link, a file image name, or a custom command

    self.id_int = NO_VALUE_SET_INT
    self.last_activated_ts_int = NO_VALUE_SET_INT  # -default: never activated


    """

    class RemembranceTable:
        name = "remembrance"

        class Cols:
            id = "id"  # key
            title = "title"
            content_type = "content_type"
            content_str = "content_str"

            last_activated = "last_activated"
            next_notif_ts = "next_notif_ts"

    class EntryTable:
        name = "entry"

        class Cols:
            id = "id"  # key
            datetime_added = "datetime_added"
            sort_order = "sort_order"  # unused
            rating = "rating"
            text = "diary_text"
            image_file = "image_file"

    class TagTable:
        name = "tag"

        class Cols:
            id = "id"  # key
            sort_order = "sort_order"
            title = "title"  # unique
            description = "description"

    class ViewTable:
        name = "view"

        class Cols:
            id = "id"  # key
            sort_order = "sort_order"
            title = "title"  # unique

    class ViewTagRelationTable:
        name = "view_tag_relation"

        class Cols:
            view_id_ref = "view_id"
            tag_id_ref = "tag_id"
            # -these two above create the composite keys
            sort_order = "sort_order"

    class TagQuestionRelationTable:
        name = "tag_question_relation"

        class Cols:
            tag_id_ref = "tag_id"
            question_id_ref = "question_id"
            # -these two above create the composite keys
            sort_order = "sort_order"
            tag_is_preselected = "tag_is_preselected"

    class TagEntryRelationTable:
        name = "tag_entry_relation"

        class Cols:
            tag_id_ref = "tag_id"
            entry_id_ref = "entry_id"
            sort_order = "sort_order"
            # -these two above create the composite keys
            # TODO: Add index for entry_id?


def initial_schema_and_setup(i_db_conn):
    # Auto-increment is not needed for the primary key in our case:
    # https://www.sqlite.org/autoinc.html

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.FilterPresetTable.name
        + "(" + DbSchemaM.FilterPresetTable.Cols.id + " INTEGER PRIMARY KEY"
        + ", " + DbSchemaM.FilterPresetTable.Cols.sort_order + " INTEGER NOT NULL"
        + ", " + DbSchemaM.FilterPresetTable.Cols.title + " TEXT NOT NULL UNIQUE"
        + ", " + DbSchemaM.FilterPresetTable.Cols.tag_active + " INTEGER NOT NULL DEFAULT " + str(SQLITE_FALSE)
        + ", " + DbSchemaM.FilterPresetTable.Cols.tag_id_ref + " INTEGER NOT NULL DEFAULT "
        + str(wbd.wbd_global.NO_ACTIVE_TAG_INT)
        + ", " + DbSchemaM.FilterPresetTable.Cols.search_active + " INTEGER NOT NULL DEFAULT " + str(SQLITE_FALSE)
        + ", " + DbSchemaM.FilterPresetTable.Cols.search_term + " TEXT NOT NULL DEFAULT ''"
        + ", " + DbSchemaM.FilterPresetTable.Cols.rating_active + " INTEGER NOT NULL DEFAULT " + str(SQLITE_FALSE)
        + ", " + DbSchemaM.FilterPresetTable.Cols.rating + " INTEGER NOT NULL DEFAULT " + str(0)
        + ", " + DbSchemaM.FilterPresetTable.Cols.datetime_active + " INTEGER NOT NULL DEFAULT " + str(SQLITE_FALSE)
        + ", " + DbSchemaM.FilterPresetTable.Cols.start_date + " TEXT NOT NULL DEFAULT "
        + "'" + str(wbd.wbd_global.DATETIME_NOT_SET_STR) + "'"
        + ", " + DbSchemaM.FilterPresetTable.Cols.end_date + " TEXT NOT NULL DEFAULT "
        + "'" + str(wbd.wbd_global.DATETIME_NOT_SET_STR) + "'"
        + ")"
    )

    i_db_conn.execute(
        "INSERT INTO " + DbSchemaM.FilterPresetTable.name
        + "(" + DbSchemaM.FilterPresetTable.Cols.id
        + ", " + DbSchemaM.FilterPresetTable.Cols.sort_order
        + ", " + DbSchemaM.FilterPresetTable.Cols.title
        + ") VALUES (?, ?, ?)",
        (wbd.wbd_global.NO_ACTIVE_FILTER_PRESET_INT, ALWAYS_AT_TOP_INT, "<i>no filter</i>")
    )

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.QuestionTable.name
        + "(" + DbSchemaM.QuestionTable.Cols.id + " INTEGER PRIMARY KEY"
        + ", " + DbSchemaM.QuestionTable.Cols.sort_order + " INTEGER NOT NULL"
        + ", " + DbSchemaM.QuestionTable.Cols.title + " TEXT NOT NULL UNIQUE"
        + ", " + DbSchemaM.QuestionTable.Cols.description + " TEXT NOT NULL DEFAULT ''"
        + ")"
    )
    i_db_conn.execute(
        "INSERT INTO " + DbSchemaM.QuestionTable.name
        + "(" + DbSchemaM.QuestionTable.Cols.id
        + ", " + DbSchemaM.QuestionTable.Cols.sort_order
        + ", " + DbSchemaM.QuestionTable.Cols.title
        + ", " + DbSchemaM.QuestionTable.Cols.description
        + ") VALUES (?, ?, ?, ?)",
        (wbd.wbd_global.NO_ACTIVE_QUESTION_INT, ALWAYS_AT_TOP_INT, "<i>No question (free writing)</i>", "")
    )

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.EntryTable.name
        + "(" + DbSchemaM.EntryTable.Cols.id + " INTEGER PRIMARY KEY"
        + ", " + DbSchemaM.EntryTable.Cols.datetime_added + " TEXT"
        + ", " + DbSchemaM.EntryTable.Cols.sort_order + " INTEGER"
        + ", " + DbSchemaM.EntryTable.Cols.rating + " INTEGER NOT NULL DEFAULT '" + str(1) + "'"
        + ", " + DbSchemaM.EntryTable.Cols.text + " TEXT"
        + ", " + DbSchemaM.EntryTable.Cols.image_file + " BLOB DEFAULT " + SQLITE_NULL
        + ")"
    )
    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.TagTable.name
        + "(" + DbSchemaM.TagTable.Cols.id + " INTEGER PRIMARY KEY"
        + ", " + DbSchemaM.TagTable.Cols.sort_order + " INTEGER NOT NULL"
        + ", " + DbSchemaM.TagTable.Cols.title + " TEXT NOT NULL UNIQUE"
        + ", " + DbSchemaM.TagTable.Cols.description + " TEXT NOT NULL DEFAULT ''"
        + ")"
    )
    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.ViewTable.name
        + "(" + DbSchemaM.ViewTable.Cols.id + " INTEGER PRIMARY KEY"
        + ", " + DbSchemaM.ViewTable.Cols.sort_order + " INTEGER NOT NULL"
        + ", " + DbSchemaM.ViewTable.Cols.title + " TEXT NOT NULL UNIQUE"
        + ")"
    )

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.TagEntryRelationTable.name
        + "(" + DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref + " INTEGER REFERENCES "
        + DbSchemaM.TagTable.name + "(" + DbSchemaM.TagTable.Cols.id + ")"
        + ", " + DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref + " INTEGER REFERENCES "
        + DbSchemaM.EntryTable.name + "(" + DbSchemaM.EntryTable.Cols.id + ")"
        + ", " + DbSchemaM.TagEntryRelationTable.Cols.sort_order + " INTEGER NOT NULL"
        + ", PRIMARY KEY (" + DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref + ", " + DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref + ")"
        + ") WITHOUT ROWID"
    )

    index_name_str = "idx_tagentryrelation_tagid"
    i_db_conn.execute(
        "CREATE INDEX " + index_name_str + " ON " + DbSchemaM.TagEntryRelationTable.name
        + " (" + DbSchemaM.TagEntryRelationTable.Cols.tag_id_ref + ")"
    )
    index_name_str = "idx_tagentryrelation_entryid"
    i_db_conn.execute(
        "CREATE INDEX " + index_name_str + " ON " + DbSchemaM.TagEntryRelationTable.name
        + " (" + DbSchemaM.TagEntryRelationTable.Cols.entry_id_ref + ")"
    )

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.TagQuestionRelationTable.name
        + "(" + DbSchemaM.TagQuestionRelationTable.Cols.tag_id_ref + " INTEGER REFERENCES "
        + DbSchemaM.TagTable.name + "(" + DbSchemaM.TagTable.Cols.id + ")"
        + ", " + DbSchemaM.TagQuestionRelationTable.Cols.question_id_ref + " INTEGER REFERENCES "
        + DbSchemaM.QuestionTable.name + "(" + DbSchemaM.QuestionTable.Cols.id + ")"
        + ", " + DbSchemaM.TagQuestionRelationTable.Cols.sort_order + " INTEGER NOT NULL DEFAULT " + str(SQLITE_FALSE)
        + ", " + DbSchemaM.TagQuestionRelationTable.Cols.tag_is_preselected + " INTEGER NOT NULL DEFAULT " + str(
            SQLITE_FALSE)
        + ", PRIMARY KEY (" + DbSchemaM.TagQuestionRelationTable.Cols.tag_id_ref + ", " + DbSchemaM.TagQuestionRelationTable.Cols.question_id_ref + ")"
        + ") WITHOUT ROWID"
    )

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.ViewTagRelationTable.name
        + "(" + DbSchemaM.ViewTagRelationTable.Cols.view_id_ref + " INTEGER REFERENCES "
        + DbSchemaM.ViewTable.name + "(" + DbSchemaM.ViewTable.Cols.id + ")"
        + ", " + DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref + " INTEGER REFERENCES "
        + DbSchemaM.TagTable.name + "(" + DbSchemaM.TagTable.Cols.id + ")"
        + ", " + DbSchemaM.ViewTagRelationTable.Cols.sort_order + " INTEGER NOT NULL DEFAULT " + str(SQLITE_FALSE)
        + ", PRIMARY KEY (" + DbSchemaM.ViewTagRelationTable.Cols.view_id_ref + ", " + DbSchemaM.ViewTagRelationTable.Cols.tag_id_ref + ")"
        + ") WITHOUT ROWID"
    )


"""
Example of db upgrade code:
def upgrade_2_3(i_db_conn):
    backup_db_file()
    i_db_conn.execute(
        "ALTER TABLE " + DbSchemaM.QuestionTable.name + " ADD COLUMN "
        + DbSchemaM.QuestionTable.Cols.labels + " TEXT DEFAULT ''"
    )
"""

upgrade_steps = {
    1: initial_schema_and_setup
}


class DbHelperM(object):
    __db_connection = None  # "Static"

    # noinspection PyTypeChecker
    @staticmethod
    def get_db_connection():
        if DbHelperM.__db_connection is None:
            DbHelperM.__db_connection = sqlite3.connect(wbd.wbd_global.get_database_filename())

            # Upgrading the database
            # Very good upgrade explanation:
            # http://stackoverflow.com/questions/19331550/database-change-with-software-update
            # More info here: https://www.sqlite.org/pragma.html#pragma_schema_version
            current_db_ver_it = get_schema_version(DbHelperM.__db_connection)
            target_db_ver_it = max(upgrade_steps)
            for upgrade_step_it in range(current_db_ver_it + 1, target_db_ver_it + 1):
                if upgrade_step_it in upgrade_steps:
                    upgrade_steps[upgrade_step_it](DbHelperM.__db_connection)
                    set_schema_version(DbHelperM.__db_connection, upgrade_step_it)
            DbHelperM.__db_connection.commit()

            # TODO: Where do we close the db connection? (Do we need to close it?)
            # http://stackoverflow.com/questions/3850261/doing-something-before-program-exit

            if wbd.wbd_global.testing_bool:
                wbd.model.populate_db(True)
            elif not wbd.wbd_global.db_file_exists_at_application_startup_bl:
                wbd.model.populate_db(False)
            sqlite3.enable_callback_tracebacks(wbd.wbd_global.debugging_bool)
            if wbd.wbd_global.debugging_bool:
                # DbHelperM.__db_connection.set_trace_callback(print)
                DbHelperM.__db_connection.set_trace_callback(logging.debug)

        return DbHelperM.__db_connection

    @staticmethod
    def close_db_connection():
        connection = DbHelperM.get_db_connection()
        connection.close()
        DbHelperM.__db_connection = None


BACKUP_USING_SQLITE_FILENAME_SUFFIX_STR = "_db_backup_using_sqlite.sqlite"


def backup_using_sqlite() -> int:
    date_sg = datetime.datetime.now().strftime(wbd.wbd_global.PY_DATETIME_FILENAME_FORMAT_STR)
    new_file_path_str = wbd.wbd_global.get_user_backup_path(date_sg + BACKUP_USING_SQLITE_FILENAME_SUFFIX_STR)

    backup_dir_str = wbd.wbd_global.get_user_backup_path()  # -alt: os.path.abspath(new_file_path_str)
    removing_oldest_files(backup_dir_str, BACKUP_USING_SQLITE_FILENAME_SUFFIX_STR, 3)

    source_connection = DbHelperM.get_db_connection()
    with sqlite3.connect(new_file_path_str) as dest_connection:
        source_connection.backup(dest_connection)
        # PLEASE NOTE: This .backup function is new in Python version 3.7

    file_size_in_bytes_int = os.path.getsize(new_file_path_str)
    return file_size_in_bytes_int


BACKUP_USING_COPY_FILENAME_SUFFIX_STR = "_db_backup_using_copy.sqlite"


def backup_db_file() -> int:
    if wbd.wbd_global.testing_bool:
        logging.warning("Cannot copy :memory: database to new file")
        return -1
    date_sg = datetime.datetime.now().strftime(wbd.wbd_global.PY_DATETIME_FILENAME_FORMAT_STR)

    backup_dir_str = wbd.wbd_global.get_user_backup_path()  # -alt: os.path.abspath(new_file_name_sg)
    removing_oldest_files(backup_dir_str, BACKUP_USING_COPY_FILENAME_SUFFIX_STR, 3)

    new_file_name_sg = wbd.wbd_global.get_user_backup_path(date_sg + BACKUP_USING_COPY_FILENAME_SUFFIX_STR)
    new_file_path_str = wbd.wbd_global.get_user_backup_path(new_file_name_sg)

    shutil.copyfile(wbd.wbd_global.get_database_filename(), new_file_path_str)
    # TODO: Catching exception if there's not enough diskspace available

    file_size_in_bytes_int = os.path.getsize(new_file_path_str)
    return file_size_in_bytes_int


ITER_DUMP_SUFFIX_STR = "_db_iter_dump.sql"


def take_iter_db_dump():
    connection = DbHelperM.get_db_connection()
    date_sg = datetime.datetime.now().strftime(wbd.wbd_global.PY_DATETIME_FILENAME_FORMAT_STR)
    file_path_str = wbd.wbd_global.get_user_iterdump_path(date_sg + ITER_DUMP_SUFFIX_STR)

    backup_dir_str = wbd.wbd_global.get_user_iterdump_path()
    removing_oldest_files(backup_dir_str, ITER_DUMP_SUFFIX_STR, 3)

    with open(file_path_str, 'w') as file:
        for sql_line_str in connection.iterdump():
            file.write(sql_line_str + '\n')
        # file.writelines(connection.iterdump())


def get_row_count() -> int:
    """
    Three ways to get the number of rows:
    1. using cursor.rowcount - https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.rowcount
    There are some things to be aware of here however: https://stackoverflow.com/q/839069/2525237
    2. using len(db_cursor.fetchall()) as described here: https://stackoverflow.com/a/21838197/2525237
    3. using SELECT COUNT(*)
    Please note that in all cases we need to have selected some table (it doesn't seem to be possible to count
    all the rows)
    :return:
    """
    db_connection = DbHelperM.get_db_connection()

    db_cursor = db_connection.cursor()
    db_cursor = db_cursor.execute(
        "SELECT * FROM " + wbd.db.DbSchemaM.EntryTable.name
    )
    db_connection.commit()

    ret_row_count_int = db_cursor.rowcount
    logging.debug("ret_row_count_int = " + str(ret_row_count_int))
    fetch_all_row_count_int = len(db_cursor.fetchall())
    logging.debug("fetch_all_row_count_int = " + str(fetch_all_row_count_int))

    sqlite_select_count_string_str = (
            "SELECT COUNT(*)"
            + " FROM " + wbd.db.DbSchemaM.EntryTable.name
    )

    return ret_row_count_int

    # Please note that it can be good to compare with len(cursor.fetchall), see this answer:
    # https://stackoverflow.com/a/21838197/2525237
