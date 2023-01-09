import json
import pprint

from spackle import dynamodb, log


class Customer:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    @staticmethod
    def retrieve(customer_id):
        log.log_debug("Retrieving customer data for %s" % customer_id)
        dynamodb_client = dynamodb.get_client()
        response = dynamodb_client.get_item(
            {
                "CustomerId": {"S": customer_id},
            }
        )

        data = json.loads(response["Item"]["State"]["S"])
        log.log_debug("Retrieved customer data for %s: %s" % (customer_id, data))
        return Customer(customer_id, data)

    def enabled(self, key):
        for feature in self.data["features"]:
            if feature["key"] == key:
                return feature["value_flag"]

        return False

    def limit(self, key):
        for feature in self.data["features"]:
            if feature["key"] == key:
                return feature["value_limit"]

        return 0

    def __repr__(self):
        return f"<Customer ({self.id}):\n{pprint.pformat(self.data)}>"
