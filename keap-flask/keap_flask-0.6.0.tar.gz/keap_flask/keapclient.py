from json import dumps

from .keapcache import KeapCache
from .keaprestclient import KeapRestClient, KeapDataError


class KeapClient(KeapRestClient, KeapCache):

    def __init__(self, app):
        KeapRestClient.__init__(self, app)

    def update_contact_custom_field(self, contact_id, field_key, value):
        field_id = self.get_contact_custom_field_id(field_key=field_key)
        custom_fields = [{
            "id": f"{field_id}",
            "content": f"{value}"
        }]
        data = {
            "custom_fields": custom_fields
        }
        self.update_contact(contact_id, **data)

    def get_contacts(self, **kwargs):
        """
            To get all the contacts you can just call the method, to filter use limit, order, offset.
            For other options see the documentation of the API
            :return:
        """
        return self._get('contacts', **kwargs)

    def get_contact_by_email(self, email):
        response = self.get_contacts(**{"Email": email})
        if response.get('count') == 0:
            return None
        else:
            return response.get("contacts")

    def contact_exists(self, email):
        """
            returns true if contact with given email exists
            :param email:
            :return:
        """
        count = self.get_contacts(**{"Email": email}).get("count")
        if count > 0:
            return True
        else:
            return False

    def retrieve_contact(self, id, **kwargs):
        if not id:
            raise KeapDataError("The ID is required.")

        endpoint = 'contacts/{0}'.format(id)
        return self._get(endpoint, **kwargs)

    def create_contact(self, **kwargs):
        """
            For create a contact is obligatory to fill the email or the phone number.
            I also recommend to fill the given_name="YOUR NAME"
            :param email:
            :param phone_number:
            :param kwargs:
            :return:
        """
        if kwargs is not None:
            params = {}
            params.update(kwargs)
            return self._post('contacts', json_data=params)
        raise KeapDataError("To create a contact a valid name and email is necessary")

    def add_note(self, contact_id, note_title, note_body):
        params = {
            "contact_id": contact_id,
            "title": note_title,
            "body": note_body,
            "type": "Other"
        }

        return self._post('notes', json_data=params)

    def addwithdupecheck(self, **kwargs):
        """
            For create a contact is obligatory to fill the email or the phone number.
            I also recommend to fill the given_name="YOUR NAME"
            :param email:
            :param kwargs:
            :return:
        """
        if kwargs is not None:
            params = {'duplicate_option': 'EmailAndName'}
            params.update(kwargs)
            return self._put('contacts', json_data=params)
        raise KeapDataError("Email required to check for duplicates")

    def delete_contact(self, id):
        """
            To delete a contact is obligatory send The ID of the contact to delete
            :param id:
            :return:
        """
        if not id:
            raise KeapDataError("The ID is required.")

        endpoint = 'contacts/{0}'.format(id)
        return self._delete(endpoint)

    def update_contact(self, id, **kwargs):
        """
            To update a contact you must to send The ID of the contact to update
            For other options see the documentation of the API
            :param id:
            :param kwargs:
            :return:
        """
        if not id:
            raise KeapDataError("The ID is required.")

        params = {}
        endpoint = 'contacts/{0}'.format(id)
        params.update(kwargs)
        return self._patch(endpoint, json_data=params)

    def get_campaigns(self, **kwargs):
        """
            To get the campaigns just call the method or send options to filter
            For more options see the documentation of the API
            :return:
        """
        return self._get('campaigns', **kwargs)

    def retrieve_campaign(self, id, **kwargs):
        """
            To retrieve a campaign is necessary the campaign id
            For more options see the documentation of the API
            :param id:
            :param kwargs:
            :return:
        """
        if not id:
            raise KeapDataError("The ID is required.")

        endpoint = 'campaigns/{0}'.format(id)
        return self._get(endpoint, **kwargs)

    def get_emails(self, **kwargs):
        """
            To get the emails just call the method, if you need filter options see the documentation of the API.
            :param limit:
            :param offset:
            :param kwargs:
            :return:
        """
        return self._get('emails', **kwargs)

    def get_opportunities(self, **kwargs):
        """
            To get the opportunities you can just call the method.
            Also you can filter, see the options in the documentation API.
            :param limit:
            :param order:
            :param offset:
            :param kwargs:
            :return:
        """
        return self._get('opportunities', **kwargs)

    def get_opportunities_pipeline(self):
        """
            This method will return a pipeline of opportunities
            :return:
        """
        return self._get('opportunity/stage_pipeline')

    def get_opportunity_custom_fields(self):
        return self._get('opportunities/model')

    def get_opportunity_custom_field_id(self, field_name):
        custom_fields = self.get_opportunity_custom_fields().get('custom_fields')
        field_id = None
        for field in custom_fields:
            if field['field_name'] == field_name:
                field_id = field['id']

        return field_id

    def retrieve_opportunity(self, opp_id, **kwargs):
        """
            To retrieve a campaign is necessary the campaign id
            For more options see the documentation of the API
            :param opp_id:
            :return:
        """
        if not id:
            raise KeapDataError("The ID is required.")

        endpoint = 'opportunities/{0}'.format(opp_id)
        return self._get(endpoint, kwargs)

    def create_opportunity(self, **kwargs):
        """
            To create an opportunity is obligatory to send a title of the opportunity,
            the contact who have the opportunity, and stage.
            For more information see the documentation of the API.
            :param kwargs:
            :return:
        """
        if kwargs:
            params = {}
            params.update(kwargs)
            return self._post('opportunities', json_data=params)

    def update_opportunity(self, id, **kwargs):
        """
            To update an opportunity is obligatory The ID, the other fields you can see in the documentation.
            :param id:
            :param kwargs:
            :return:
        """
        if not id:
            raise KeapDataError("The ID is required.")

        params = {}
        endpoint = 'opportunities/{0}'.format(id)
        params.update(kwargs)
        return self._patch(endpoint, json_data=params)

    def get_products(self, **kwargs):
        return self._get('products/search', **kwargs)

    def retrieve_product(self, id):
        if not id:
            raise KeapDataError("The ID is required.")

        endpoint = "products/{0}".format(id)
        return self._get(endpoint)

    def get_tasks(self, **kwargs):
        return self._get('tasks', **kwargs)

    def create_task(self, **kwargs):
        if not kwargs:
            raise KeapDataError("title and a due_date are required to create a task.")

        params = {}
        params.update(kwargs)
        return self._post('tasks', json_data=params)

    def delete_task(self, id):
        if not id:
            raise KeapDataError("The ID is required.")

        endpoint = 'tasks/{0}'.format(id)
        return self._delete(endpoint)

    def update_task(self, id, **kwargs):
        if not id:
            raise KeapDataError("The ID is required.")

        params = {}
        endpoint = 'tasks/{0}'.format(id)
        params.update(kwargs)
        return self._patch(endpoint, json_data=params)

    def retrieve_task(self, id):
        if not id:
            raise KeapDataError("The ID is required.")

        endpoint = "tasks/{0}".format(id)
        return self._get(endpoint)

    def replace_task(self, id, **kwargs):
        if not id:
            raise KeapDataError("The ID is required.")

        endpoint = "tasks/{0}".format(id)
        return self._put(endpoint, **kwargs)

    def get_orders(self, **kwargs):
        return self._get('orders', **kwargs)

    def retrieve_order(self, id):
        if not id:
            raise KeapDataError("The ID is required.")

        endpoint = "tasks/{0}".format(id)
        return self._get(endpoint)

    def get_hook_events(self):
        callback = "{0}/{1}".format("hooks", "event_keys")
        return self._get(callback)

    def get_hook_subscriptions(self):
        return self._get('hooks')

    def verify_hook_subscription(self, id):
        if not id:
            raise KeapDataError("The ID is required.")
        callback = "{0}/{1}/{2}".format("hooks", id, "verify")
        return self._post(callback, data=None)

    def create_hook_subscription(self, event, callback):
        if not event:
            raise KeapDataError("The event is required.")
        if not callback:
            raise KeapDataError("The callback is required.")

        args = {"eventKey": event, "hookUrl": callback}
        return self._post('hooks', json_data=args)

    def update_hook_subscription(self, id, event, url):
        if not id:
            raise KeapDataError("The ID is required.")

        callback = "{0}/{1}".format("hooks", id)
        args = {"eventKey": event, "hookUrl": url}
        return self._post(callback, json_data=args)

    def delete_hook_subscription(self, id):
        if not id:
            raise KeapDataError("The ID is required.")

        callback = "{0}/{1}".format("hooks", id)
        return self._delete(callback)

    def apply_tag(self, tag_name: str, contact_ids, **kwargs):
        """
        Apply a tag to one or multiple contacts.
        :param tag_name: String, tag name.
        :param contact_ids: Either one contact ID or a list of contact IDs.
        :param kwargs:
        :return:
        """
        if not tag_name:
            raise KeapDataError("tag_name is required.")

        if not isinstance(contact_ids, (tuple, list, set)) or not contact_ids:
            if contact_ids:
                contact_ids = [contact_ids]
            else:
                raise KeapDataError("contact_ids has to be a list or a single contact id.")
        tag_id = self.tags.get(tag_name)

        data = {
            "ids": contact_ids
        }
        endpoint = 'tags/{tagId}/contacts'.format(tagId=tag_id)
        return self._post(endpoint, data=dumps(data))

    def remove_tag(self, tag_id, contact_id, **kwargs):
        """
        Remove a tag from a contact.
        :param tag_id: Integer tag ID.
        :param contact_id: Integer contact ID.
        :param kwargs:
        :return:
        """
        if not tag_id:
            raise KeapDataError("tag_id is required.")
        if not contact_id:
            raise KeapDataError("contact_id is required.")

        endpoint = 'tags/{tagId}/contacts/{contactId}'.format(tagId=tag_id, contactId=contact_id)
        return self._delete(endpoint, **kwargs)

    def achieve_goal(self, integration, callName, **kwargs):
        """
        Achieve an api goal
        :param integration: Integration name.
        :param callName: callname on the integration.
        :return:
        """
        if not integration:
            raise KeapDataError("integration is required.")
        if not callName:
            raise KeapDataError("callName is required.")

        if kwargs is not None:
            params = {}
            params.update(kwargs)
            endpoint = 'campaigns/goals/{integration_Name}/{call_Name}'.format(integration_Name=integration,
                                                                               call_Name=callName)
            return self._post(endpoint, json_data=params)
        raise KeapDataError("Data is required to achieve an api goal")

    def query_contact_custom_field(self, field_name, field_value, return_fields=None):
        """
        return id of contact matching query
        :param return_fields: fields to return from keap
        :param field_name: Name of the custom field in Keap. ex: _netsuiteid
        :param field_value: value to query on
        :return:
        """
        if not field_name:
            raise KeapDataError("field_name is required.")
        if not field_value:
            raise KeapDataError("field_value is required.")
        xmlrpc_client = self.get_xmlrpc_client()
        query = {
            f"{field_name}": f"{field_value}"
        }
        fields = ["Id"]
        if return_fields is not None:
            for field in return_fields:
                fields.append(field)
        return xmlrpc_client.DataService("query", "Contact", 1, 0, query, fields)
