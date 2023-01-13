import json
import urllib.request

def classify(classifier_uuid: str, document: str) -> str:
    request_body = json.dumps({'document': str(document)}).encode('utf8')
    request = urllib.request.Request(f'https://www.classr.dev/api/classifier/{classifier_uuid}', data=request_body,
        headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(request)
    response_body = response.read().decode('utf-8')
    return json.loads(response_body)['class']

def get_info(classifier_uuid: str) -> dict:
    request = urllib.request.Request(f'https://www.classr.dev/api/classifier/{classifier_uuid}',
        headers={'accept': 'application/json'})
    response = urllib.request.urlopen(request)
    response_body = response.read().decode('utf-8')
    return json.loads(response_body)


class Classr:

    def __init__(self, classifier_uuid):
        self.classifier_uuid = classifier_uuid

    def classify(self, document):
        return classify(self.classifier_uuid, document)

    def get_info(self):
        return get_info(self.classifier_uuid)
