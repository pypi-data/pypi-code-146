from askdata.smartgraph import smart_title, smart_substitution
import threading
import time

if __name__ == "__main__":
    smartquery = {"components": [{"type": "chart", "queryId": "q0", "chartType": "LINE"}],
                  "queries": [{"datasets": [], "fields": [
                      {"aggregation": "MAX", "column": "totale_casi", "internalDataType": "NUMERIC"},
                      {"aggregation": "AVG", "column": "deceduti", "internalDataType": "NUMERIC"},
                      {"column": "denominazione_regione", "internalDataType": "STRING"},
                      {"column": "monthly", "internalDataType": "DATE"}], "id": "q0", "limit": "3",
                               "where": [{"field": {"column": "deceduti"}, "operator": "GOE", "value": ["30"]},
                                         {"field": {"column": "denominazione_regione"}, "operator": "IN",
                                          "negate": True, "value": ["Lazio"]},
                                         {"field": {"column": "monthly"}, "operator": "RANGE",
                                          "value": ["2020-07-13", "2020-10-16"]},
                                         {"field": {"column": "monthly"}, "operator": "RANGE", "direction": "CURR",
                                          "steps": "2"}]}]}
    metadata = {"totale_casi": "Totale casi", "deceduti": "Deceduti", "denominazione_regione": "Regione",
                "monthly": "Monthly"}

    sentence = "monuments <mask> Italy"

    thread_list = []
    t = threading.Thread(target=smart_title, args=[smartquery, metadata, "en-US"])
    t.start()
    thread_list.append(t)
    t = threading.Thread(target=smart_substitution, args=[sentence])
    t.start()
    thread_list.append(t)
    print(f'Active Threads: {threading.active_count()}')
    for t in thread_list:
        t.join()
    print(f'Active Threads: {threading.active_count()}')
