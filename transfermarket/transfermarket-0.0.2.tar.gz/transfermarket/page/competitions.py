"""
This module contains page objects for the competitions page.
"""

from transfermarket.common.utils import urljoin
from transfermarket.models.competition import Competition
from transfermarket.page.object import PageObject
from transfermarket.page.utils import BASE_URL

# def parse_competition(table_row):
#     data = {}
#
#     return data
#
#     # return {
#     #     "id": DataCell(table_row[2]).link_href().extract_competition_id().read(),
#     #     "name": DataCell(table_row[2]).link_title().read(),
#     #     "country": DataCell(table_row[3]).img_title().read(),
#     #     "total_clubs": DataCell(table_row[4]).to_int().read(),
#     #     "total_players": DataCell(table_row[5]).to_int().read(),
#     #     "avg_age": DataCell(table_row[6]).to_float().read(),
#     #     "foreigners_percent":
#     #     DataCell(table_row[7]).to_string().parse_percentage().read(),
#     #     "total_value": DataCell(table_row[9]).to_string().read(),
#     # }


class CompetitionsPage(PageObject):
    """
    This class provides the logic to parse the competitions page.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        page = kwargs.get("page", 1)

        # Original: https://www.transfermarkt.com/wettbewerbe/europa/wettbewerbe
        self.url = urljoin(BASE_URL, f"/wettbewerbe/europa?ajax=yw1&page={page}")
        self.headers = {"user-agent": "transfermarkt"}

        if kwargs.get("auto_load", False):
            self.load()

    def get_page_count(self):
        """
        Returns the total number of pages.
        """
        unordered_list = self.soup.find("ul", {"class", "tm-pagination"})
        last_number = unordered_list.find_all("li")[-3].text.strip()
        last_number = int(last_number)

        return last_number

    def get_competitions(self) -> list:
        """
        Returns a list of competitions.
        """
        competitions = []

        tables = self.soup.find_all("table", {"class": "items"})
        items_table = tables[0]
        content = items_table.select("tbody > tr")[1:]

        tier = "First Tier"
        for row in content:
            columns = row.select("td")

            if len(columns) == 1:
                tier = columns[0].text.strip()
            else:
                competition = Competition()
                competition.name = columns[0].text.strip()

                anchors = columns[0].select("a")
                competition.id = anchors[1]["href"].split("/")[-1]

                competition.country = columns[3].select("img")[0]["title"]
                competition.total_clubs = int(columns[4].text.strip())
                competition.total_players = int(columns[5].text.strip())
                competition.avg_age = float(columns[6].text.strip())
                competition.foreigners_percent = float(columns[7].text.strip().replace("%", ""))
                competition.total_value = columns[9].text.strip()
                competition.tier = tier

                competitions.append(competition)

        return competitions

    @staticmethod
    def get_all_competitions():
        """
        Returns all competitions.
        """
        page = CompetitionsPage(page=1)
        competitions = page.get_competitions()

        page_count = page.get_page_count()
        for page_number in range(2, page_count + 1):
            page = CompetitionsPage(page=page_number)
            competitions.extend(page.get_competitions())

        return competitions


if __name__ == "__main__":
    # service = TransferMarketService()
    #
    # competition_count = 0
    # team_count = 0
    # player_count = 0
    # competitions = CompetitionsPage.get_all_competitions()
    # for competition in competitions:
    #     try:
    #         competition_count += 1
    #         print(competition)
    #
    #         teams = service.get_teams(identifier=competition.id)
    #         for team in teams:
    #             team_count += 1
    #             print(f"\t{team}")
    #
    #             players = service.get_players(identifier=team.id)
    #             for player in players:
    #                 player_count += 1
    #                 print(f"\t\t{player}")
    #     except Exception as e:
    #         print(e)
    #
    # print(f"Competitions: {competition_count}")
    # print(f"Teams: {team_count}")
    # print(f"Players: {player_count}")
    pass
