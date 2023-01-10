import boto3

ACCESS_KEY_ID = 'AKIAQQWD5X6TKXHY2S3O'
ACCESS_SECRET_KEY='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'

comprehendmedical = boto3.client('comprehendmedical',aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key = ACCESS_SECRET_KEY, region_name='us-west-2')

def extract_data(text_data):
    result = comprehendmedical.detect_entities(Text= text_data)
    entities = result
    return entities