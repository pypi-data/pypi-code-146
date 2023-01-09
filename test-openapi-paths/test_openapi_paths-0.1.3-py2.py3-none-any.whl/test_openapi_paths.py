import schemathesis


# before moved to data folder
# schema = schemathesis.from_path('./test_openapi_paths/pet3.json')

schema = schemathesis.from_path('./data/pet3.json')
schema.base_url = "https://petstore3.swagger.io/api/v3/"


@schema.parametrize()
def test_api(case):
    response = case.call()

    print(case)
    print(response)
    print(response.text)
    print("***** ***** *****")

    case.validate_response(response)


def add_one(number):
    return number + 1
