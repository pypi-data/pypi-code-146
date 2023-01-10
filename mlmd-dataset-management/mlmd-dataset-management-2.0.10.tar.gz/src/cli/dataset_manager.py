import requests
import json

def program(a1, a2):
    print(a1, a2)

def main():
    import sys
    import os
    arg1 = sys.argv[1]
    if arg1 == "run-moap":
        headers = {
            
        }
        requests.post("http://dev.analytics.esmartapi.com/moap/execute_ds", data=json.dumps({

        }))
        return
    if arg1 == "get-prediction":
        program(arg1)
        return
    if arg1 == "get-validation":
        program(arg1)
        return
    if arg1 == "set-dataset":
        arg2 = sys.argv[1]
        os.environ["DATASET_MANAGEMENT"] = arg2
        return
    if arg1 == "get-dataset":
        print(os.environ["DATASET_MANAGEMENT"])
        return
    print("Unsupport command: {}".format(arg1))

if __name__ == "__main__":
    main()