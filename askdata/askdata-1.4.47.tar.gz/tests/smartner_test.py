import pandas as pd
from askdata.human2query import nlp, smartner_automated_analysis
import time

if __name__ == "__main__":

    # ---------------------------------------------------------------------------------------------------------------- #
    print("#--------------------------SmartNER Online Test--------------------------#")

    # Prod
    # token = ""
    # datasets = [""]
    # language = "en"
    # env = "prod"

    # Dev
    token = ""
    datasets = []
    language = "en"
    env = "dev"

    # Usage
    nl = "units"
    df = pd.read_excel("./dataset.xlsx")

    start = time.time()
    smartquery_list = nlp(nl=nl, token=token, datasets=datasets, response_type="query2sql")
    end = time.time()

    print("SmartNER  Online")
    for sq in smartquery_list:
        print(sq)
        print()

    print("Time: ", end - start, "s")
    print()

    # ---------------------------------------------------------------------------------------------------------------- #
    print("#--------------------------SmartNER Offline Test--------------------------#")

    # Usage
    nl = "units ordered"
    df = pd.read_excel("./inventory.xlsx")

    start = time.time()
    smartquery_list = nlp(nl=nl, dataframe=df)
    end = time.time()

    print("SmartNER Offline")
    for sq in smartquery_list:
        print(sq)
        print()

    print("Time: ", end - start, "s")
    print()

    # ---------------------------------------------------------------------------------------------------------------- #
    # print("#--------------------------SmartNER Automated Test--------------------------#")

    # suggestions = [["{{dimension.A}} and {{measure.A}}", {"{{measure.A}}": {"code": "DOWNLOAD", "value": "Download", "dataset": "f2c705dd-f63f-475b-95a9-c1ad20f33716-MYSQL-70c82ef8-2cb2-40dd-a92f-b49a80d0a305"}, "{{dimension.A}}": {"code": "WEB SITE", "value": "Web site", "dataset": "f2c705dd-f63f-475b-95a9-c1ad20f33716-MYSQL-70c82ef8-2cb2-40dd-a92f-b49a80d0a305"}}, ["f2c705dd-f63f-475b-95a9-c1ad20f33716-MYSQL-70c82ef8-2cb2-40dd-a92f-b49a80d0a305"]]]
    #
    # start = time.time()
    # smartquery_list = smartner_automated_analysis(suggestions, token, env="dev", response_type="deanonymize")
    # end = time.time()
    #
    # print("Automated analysis")
    # for sq in smartquery_list:
    #     print(sq)
    #     print()
    #
    # print("Time: ", end - start, "s")
