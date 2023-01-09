import logging
import feedparser
import requests
import sys

import Certfrtracker.NVD as NVD
import Certfrtracker.html_parser as html_parser
from Certfrtracker.sqlite import Sqlite
from Certfrtracker.version_parser import systems_filter

logger = logging.getLogger(__name__)


def exceptions_handler(type, value, tb):
    """
    new exception handler, to pipe all unexpected errors into the logger
    """
    logger.error("Uncaught exception: {0}".format(str(value)))


# change exception handler to custom exception handler
sys.excepthook = exceptions_handler


class Report:
    """
    Plain object returned by Router class as list of Report.
    It contains all information about each alert.
    """

    def __init__(self, alert_id: str, techno: str, version: str, status: str, score: float, publish_date: str,
                 update_date: str, description: str, source: str, details: str) -> None:
        self.alert_id = alert_id  # id of the Alert           | String | CVE-2022-1234,
        # CERTFR-2022-ALE-004, CERTFR-2022-AVI-004
        self.techno = techno  # Name of the Techno        | String | ex: Apache, Postgresql, Openjdk
        self.version = version  # Version of the Techno     | String | ex: 1.2.3, 1.2, 1.2.3-beta
        self.status = status  # Nature of Alert           | String | Open or Applicable
        self.score = score  # CVSS or NVD Score         | Float  | between 1 and 10
        self.publish_date = publish_date  # Publish Date              | String | ex: "2020-06-21
        self.update_date = update_date  # Update Date               | String | ex: "2020-06-21
        self.description = description  # Alert Description         | String
        # self.source = | String | ex: url
        self.source = source  # url of the alert | string
        self.details = details


class Router:
    """
    This class creates and updates the database to the certfr.
    It also compares the technos and versions you give as argument to the database and returns it as a list of Report
    """

    def __init__(self, db_file="CertfrTracker.db"):
        self.sqliteCon = Sqlite(db_file)
        self.sqliteCon.create_data_base()

    def __del__(self):
        self.sqliteCon.close_connection()

    def update_database(self, feed_type=""):
        """
        Updates the database by scrapping the certfr, and it's RSS stream.
        :param feed_type: str="" - "NextAlert" or "NextAvis", if null exec both.
        """
        if feed_type == "NextAvis":
            rss_link = 'https://www.cert.ssi.gouv.fr/avis/feed/'
            last_scrap = self.sqliteCon.get_next_scrap(feed_type)  # get lastScrap from database
            if last_scrap == "Null":
                last_scrap = "CERTFR-2015-AVI-001"
        elif feed_type == "NextAlert":
            rss_link = 'https://www.cert.ssi.gouv.fr/alerte/feed/'
            last_scrap = self.sqliteCon.get_next_scrap(feed_type)  # get lastScrap from database
            if last_scrap == "Null":
                last_scrap = "CERTFR-2014-ALE-001"
        else:
            self.update_database("NextAvis")
            self.update_database("NextAlert")
            return

        # TODO: secure errors
        logger.info(f"Starting new HTTPS connection: {rss_link}")
        news_feed = feedparser.parse(rss_link)

        # since the order of the feed is not sorted, we have to manually detect which of theses are the latest and
        # newest alerts
        data_set = {"date": [], "link": []}
        for entry in news_feed.entries:
            data_set["date"].append(entry.published_parsed)
            data_set["link"].append(entry.link)
        latest_feed = data_set["link"][data_set["date"].index(max(data_set["date"]))].split("/")[-2]
        oldest_feed = data_set["link"][data_set["date"].index(min(data_set["date"]))].split("/")[-2]

        # if the database is not up-to-date
        if last_scrap != latest_feed:
            self.update_database_using_rss(data_set["link"])
            self.sqliteCon.set_next_scrap(feed_type, latest_feed)  # set next_scrap to database

        # if there's a hole between the oldest rss and the latest from database :
        if int(last_scrap.split('-')[1]) <= int(oldest_feed.split('-')[1]) and int(last_scrap.split('-')[-1]) < int(
                oldest_feed.split('-')[-1]):
            self.update_database_using_crawler(feed_type=feed_type, last_scrap=last_scrap, max_crawl=oldest_feed)

        logger.info(f"{feed_type} Database is up-to-date")

    def update_database_using_rss(self, urls: [str]):
        """
        Updates the database by scrapping the certfr
        :param urls: [str] - a list containing all the alerts that are going to be saved.
        """
        logger.info(f"Updating via RSS")

        for url in urls:
            # Download from URL.
            r = requests.get(url)
            logger.info(f"Starting new HTTPS connection: {url}")
            logger.info(f"received status {r.status_code} from {url}")

            # Save to database.
            logger.info(f"Saving {url} alert into database...")
            self.alerts_to_database(url.split("/")[-2], url, r.content)

        logger.info(f"RSS Update finished")

    def update_database_using_crawler(self, feed_type, last_scrap, max_crawl):
        """
        Updates the database by crawling the certfr.
        :param feed_type: str - "NextAlert" or "NextAvis"
        :param last_scrap : str - the alert to begin the crawl with
        :param max_crawl : str - the alert to stop the crawl with
        """
        logger.info(f"Updating via Crawler")

        if feed_type == "NextAvis":
            url = 'https://www.cert.ssi.gouv.fr/avis/'
        else:
            url = 'https://www.cert.ssi.gouv.fr/alerte/'

        begin_year = int(last_scrap[7:11])
        begin_alert = int(last_scrap.split('-')[-1])

        max_number = 10000
        max_year = int(max_crawl[7:11])

        for year in range(begin_year, max_year + 1):
            if year != begin_year:
                begin_alert = 1
            # if this is the last year of crawling, it sets the max value to the value of crawl
            if year == max_year:
                max_number = int(max_crawl.split('-')[-1])

            for count in range(begin_alert, max_number):
                # Download from URL.
                alert_id = 'CERTFR-' + str(year) + '-' + feed_type.upper()[4:7] + '-' + str(count).zfill(3)
                r = requests.get(url + alert_id)
                logger.info(f"Starting new HTTPS connection: {url}{alert_id}")
                logger.info(f"received status {r.status_code} from {alert_id}")

                # return the next alert to begin with for next run
                if r.status_code == 404 and year == max_year:
                    logger.info(f"Crawler update finished")
                    return
                # go to next year once the actual is done
                elif r.status_code == 404:
                    break

                # Save to database.
                logger.info(f"Saving {alert_id} alert into database...")
                self.alerts_to_database(alert_id, url + alert_id, r.content)

    def alerts_to_database(self, alert_id, source, text):
        """
        Scraps the html file in argument and insert it into the database.
        :param alert_id: str - CERTFR-AAAA-(ALE or AVI)-NNN
        :param source: str - URL of the alert
        :param text: str - html content returned by the certfr
        """
        systems_affectes = html_parser.systems_parser(text)
        _date = html_parser.date_parser(text)
        summary = html_parser.header_summary_parser(text)
        documentation_texte, documentation_liens = html_parser.documentation_parser(text)

        # NVD score
        CVE = NVD.checkForCVE(documentation_liens, documentation_texte)

        score = 0.0
        if CVE != "":  # if a CVE has been detected it will replace 0.0 by the actual severity
            logger.debug(f"CVE \"{CVE}\" found for {alert_id} alert")
            score = NVD.getNVDScore(CVE)

        # get details link
        details = html_parser.define_details(score, CVE, documentation_liens)

        self.sqliteCon.add_new_alert(alert_id, _date, systems_affectes, summary, score, source, details)

    def compare_inventory_with_alerts(self, technos: [str], versions: [str], dates: [str]) -> [Report]:
        """
        returns a list of Report by comparing the inventory in entry with the database.
        :param technos: [str]
        :param versions: [str]
        :param dates: [str]
        :return: [Report]
        """
        reports = []

        for techno, version, _date, in zip(technos, versions, dates):
            reports += self.compare_one_techno_with_alerts(techno, version, _date)

        return reports

    def compare_one_techno_with_alerts(self, techno: str, version: str, _date: str) -> [Report]:
        """
        returns a list of Report by comparing the single techno in entry with the database.
        :param techno: str
        :param version: str
        :param _date: str
        :return: [Report]
        """
        logger.info(f"Comparing {techno} {version} with the database...")
        reports = []
        techno = techno.lower()
        if _date == "":
            _date = "01-01-2014"

        for alert in self.sqliteCon.get_alerts_newer_than(_date):
            for line in self.sqliteCon.get_one_row_from_alerts('SystèmesAffectés', alert).split("|"):
                result = systems_filter(techno, version, line)
                if result is not None:
                    score_nvd = self.sqliteCon.get_one_row_from_alerts('ScoreNVD', alert)
                    summary = self.sqliteCon.get_one_row_from_alerts('Résumé', alert)
                    release_date = self.sqliteCon.get_one_row_from_alerts('Date', alert)
                    source = self.sqliteCon.get_one_row_from_alerts('Source', alert)
                    details = self.sqliteCon.get_one_row_from_alerts('Details', alert)

                    report = Report(alert_id=alert, techno=techno, version=version, status=result,
                                    score=float(score_nvd), update_date=release_date, publish_date=release_date,
                                    description=summary, source=source, details=details)

                    reports.append(report)

        # to remove duplicated from list
        no_duplicates = []

        logger.debug(f"Removing duplicates in reports")
        for report in reports:
            token = True
            for index, no_duplicate in enumerate(no_duplicates):
                # check if alert_id already exists in "no_duplicate"
                if report.alert_id == no_duplicate.alert_id:
                    token = False
                    # check if the existing alert is "Applicable" or "Open"
                    # if the status of the existing alert is lower, it will replace it by the higher report
                    if report.status[0] == "A" and no_duplicate.status[0] == "O":
                        no_duplicates[index] = report

            if token:
                no_duplicates.append(report)

        return no_duplicates
