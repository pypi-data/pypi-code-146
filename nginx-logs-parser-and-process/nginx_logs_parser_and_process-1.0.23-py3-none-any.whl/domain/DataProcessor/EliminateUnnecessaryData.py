from pandas import DataFrame
from nginx_logs_parser_and_process.domain.Server.Server import Server


class EliminateUnnecessaryData:
    def __init__(self, pd, server: Server):
        self.pd = pd
        self.server = server

    def process(self, dataframe: DataFrame) -> DataFrame:
        # dataframe = dataframe.loc[dataframe["referer"] == '"https://seb.ops1.thunderbees.com.br/sgi/"']
        # filtered_data: DataFrame = DataFrame(columns=dataframe.columns)
        # for filter in self.server.data_filter:
        #     clean_dataframe = dataframe.loc[dataframe[filter["field"]].str.contains(filter["value"], regex=True)]
        #     filtered_data = self.pd.concat([filtered_data, clean_dataframe])
        # return filtered_data
        filtered_data: DataFrame = DataFrame(columns=dataframe.columns)
        clean_dataframe = dataframe.loc[~dataframe["request"].str.contains('"POST /sounds/getSounds HTTP/1.1"', regex=True)]
        filtered_data = self.pd.concat([filtered_data, clean_dataframe])
        return filtered_data
