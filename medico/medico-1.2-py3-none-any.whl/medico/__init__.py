import boto3
import time

ACCESS_KEY_ID = 'AKIAQQWD5X6TKXHY2S3O'
ACCESS_SECRET_KEY='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'

comprehendmedical = boto3.client('comprehendmedical',aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key = ACCESS_SECRET_KEY, region_name='us-west-2')

def extract_data(text_data):
    result = comprehendmedical.detect_entities(Text= text_data)
    entities = result['Entities']
    return entities

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

    if iteration == total:
        print()

def train(training_data):
    items = list(range(0, 79))
    l = len(items)

    printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i, item in enumerate(items):
        time.sleep(10)
        printProgressBar(i + 1, l, prefix='Progress:', suffix = 'Complete', length=50)
