import json
from google.oauth2 import service_account
import google.cloud.firestore as firestore
from txp.common.utils import firestore_utils
import sys

credentials_path = "../../../common/credentials/pub_sub_to_bigquery_credentials.json"


def main():
    args = sys.argv[1:]
    if not len(args):
        print("Tenant id not specified")
        return
    tenant_id = args[0]

    with open(credentials_path, 'r') as file:
        credentials_str = file.read().replace('\n', '')

    json_dict_service_account = json.loads(credentials_str, strict=False)
    credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
    firestore_db = firestore.Client(credentials=credentials, project=credentials.project_id)

    tenant_doc = firestore_utils.pull_tenant_doc(firestore_db, tenant_id)
    tenant_dict = tenant_doc.to_dict()
    tenant_doc_ref = tenant_doc.reference

    for section_id in tenant_dict["sections"]:
        tenant_doc_ref.update({
            f"sections.{section_id}.next": ""
        })

        tenant_doc_ref.update({
            f"sections.{section_id}.last": ""
        })


if __name__ == "__main__":
    main()
