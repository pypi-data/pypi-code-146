from sqlite3 import connect
import logging

logger = logging.getLogger(__name__)

class Sqlite:
    """
    This class handles everything related to the database of the app.
    """

    def __init__(self, db_file):
        # If the file doesn't exist, the connection will create it.
        self.connection = connect(db_file)

    def close_connection(self):
        """
        Close the Sqlite connection.
        """
        self.connection.close()

    def create_data_base(self):
        """
        Creates the database if it doesn't exist. Updates scheme if needed.
        """
        logger.debug("Creating database file or/and updating it's scheme")
        # file always exists since the connection creates it, so no need to check if the file exists
        cur = self.connection.cursor()

        cur.executescript("""
            create table if not exists alerts (
                "Numéro" TEXT,
                "Date" TEXT,
                "SystèmesAffectés" TEXT,
                "Résumé" TEXT,
                "ScoreNVD" TEXT,
                "Source" TEXT,
                "Details" TEXT,
                UNIQUE(Numéro)
            );
        """)

        cur.executescript("""
            create table if not exists NextAlert (
                "NextScrap" TEXT
            );
            create table if not exists NextAvis (
                "NextScrap" TEXT
            );
        """)

        if not [row[0] for row in cur.execute("SELECT * FROM NextAlert")]:
            cur.execute("INSERT INTO NextAlert VALUES (?)", ["Null"])
        if not [row[0] for row in cur.execute("SELECT * FROM NextAvis")]:
            cur.execute("INSERT INTO NextAvis VALUES (?)", ["Null"])

        self.connection.commit()

    def add_new_alert(self, number, _date, affected_systems, summary, score_nvd, source, details):
        """
        Creates or updates a line in the table "alerts".
        :param number: str
        :param _date: str
        :param affected_systems: str
        :param summary: str
        :param score_nvd: str
        :param source: str
        :param details: str
        """
        cur = self.connection.cursor()

        if number not in [row[0] for row in cur.execute("select Numéro from alerts where Numéro = ?", [number])]:
            # if the alerts isn't in tha database yet.
            cur.execute("INSERT INTO alerts VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (number, _date, affected_systems, summary, score_nvd, source, details))
        else:
            # if the alert already exists in the database
            cur.execute("""UPDATE alerts SET
            Numéro = ?,
            Date = ?,
            SystèmesAffectés = ?,
            Résumé = ?,
            ScoreNVD = ?,
            Source = ?,
            Details = ?
            WHERE Numéro = ?
            """, (number, _date, affected_systems, summary, score_nvd, source, details, number))

        self.connection.commit()

    def get_all_alerts_names(self) -> [str]:
        """
        Returns a list of string containing all alert's names.
        :return: [str]
        """
        logger.debug(f"Getting every alert's names from database")
        cur = self.connection.cursor()

        res = []
        for row in cur.execute("select Numéro from alerts"):
            res.append(row[0])

        return res

    def get_alerts_newer_than(self, _date) -> [str]:
        """
        Returns a list of string containing all alert's names that are newer than the date given as argument.
        :return: [str]
        :param _date: "DD-MM-YYYY"
        """
        logger.debug(f"Getting all alert's names newer than {_date}")
        cur = self.connection.cursor()

        res = []
        for row in cur.execute("select Numéro from alerts where Date >= date(?)", ["-".join(_date.split('-')[::-1])]):
            res.append(row[0])

        return res

    def get_one_row_from_alerts(self, column, number) -> str:
        """
        Returns a string containing the content of the column related to the alert's number, both given as argument.
        :param column: str
        :param number: str
        :return: str
        """
        logger.debug(f"Getting {column} column from {number}")
        cur = self.connection.cursor()

        cur.execute("select " + column + " from alerts where Numéro = ?", [number])

        return cur.fetchall()[0][0]

    def set_next_scrap(self, table, next_scrap):
        """
        Either sets "NextAlert" or "NextAvis" token of the database for the next time.
        :param table: str - "NextAlert" or "NextAvis"
        :param next_scrap: str - CERTFR-AAAA-(ALE or AVI)-NNN
        """
        logger.debug(f"Updating Nextscrap token of {table} to {next_scrap}")
        cur = self.connection.cursor()

        cur.execute("UPDATE " + table + " SET NextScrap = ?", [next_scrap])

        self.connection.commit()

    def get_next_scrap(self, table) -> str:
        """
        Returns a string containing the value of the NextScrap token.
        :param table: str - "NextAlert" ou "NextAvis"
        :return: str
        """
        logger.debug(f"Getting Nextscrap token of {table}")

        cur = self.connection.cursor()

        cur.execute("select NextScrap from " + table)

        return cur.fetchall()[0][0]
