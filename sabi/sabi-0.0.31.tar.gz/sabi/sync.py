from sabi.api_client import ApiClient

class Sync(ApiClient):
    headers = None

    def __init__(self, api_key, host = None):
        version = 'v1'
        base = f'{version}/sync'
        super().__init__(api_key, base, host)

    def save_individuals(self, individuals):
        """
        Example for valid payload:

        [
            {
                "id": "1",
                "name": "joe"
            }
        ]
        """
        response = self.put('individuals',json=individuals)
        return response

    def save_states(self, states):
        """
        Example for valid payload:

        [
            {
                "id": "ddwe3-23sx-aas42",
                "name": "Backlog",
                "flow": "In Development",
                "position": 4,
                "is_complete": false,
                "is_wip": true
            }
        ]
        """
        response = self.put('status',json=states)
        return response

    def save_projects(self, states):
        """
        Example for valid payload:

        [
            {
                "project_id": "ddwe3-23sx-aas42",
                "name": "Testing Me",
                "short_name": "TM",
                "description":"",
                "json": {}
            }
        ]
        """
        response = self.put('projects',json=states)
        return response

    def save_labels(self, labels):
        """
        Example for valid payload:

        [
            {
                "id": "foo",
                "name": "foo"
            }
        ]
        """
        response = self.put('labels',json=labels)
        return response

    def save_fields(self, fields):
        """
        Example for valid payload:

        [
            {
                "id": "foo",
                "name": "foo",
                "is_custom": true,
                "type": "text",
                "json": "{}"
            }
        ]
        """
        response = self.put('fields',json=fields)
        return response
        
    def save_ticket_assignments(self, ticket_assignments):
        """
        Example for valid payload:
        
        [
            {
                "ticket_id": "ddwe3-23sx-aas42",
                "individual_id": "44fd-4rwas-3344",
                "add_or_remove": "added/removed",
                "datetime": "2019-03-28 17:43:58.48+00"
            }
        ]

        """
        response = self.put('tickets','assignment',json=ticket_assignments)
        return response

    def save_ticket_labels(self, ticket_labels):
        """
        Example for valid payload:
        
        [
            {
                "ticket_id": "ddwe3-23sx-aas42",
                "label_id": "44fd-4rwas-3344",
                "add_or_remove": "added/removed",
                "datetime": "2019-03-28 17:43:58.48+00"
            }
        ]

        """
        response = self.put('tickets','label',json=ticket_labels)
        return response

    def save_ticket_status_changes(self, ticket_status_changes):
        """
        Example for valid payload:

        [
            {
                "ticket_id": "344",
                "from_state": "State A",
                "to_state": "State B",
                "datetime": "2019-03-28 17:43:58.48+00"
            }
        ]
        """
        response = self.put('tickets','status','changes',json=ticket_status_changes)
        return response

    def save_tickets(self, tickets):
        """
        Example for valid payload:

        [
            {
                "ticket_id": "tt43d-344frf-w34d",
                "name": "Story name",
                "description": "Story description",
                "type": "Bug",
                "parent_id": "ff43d-sdd34-sd42",
                "created_at": "2021-04-04",
                "deleted": false,
                "estimate": 5
            }
        ]
        """
        response = self.put('tickets',json=tickets)
        return response
        
    def delete_tickets(self, tickets):
        """
        Example for valid payload:

        [
            {
                "ticket_id": "tt43d-344frf-w34d",
                "deleted": false
            }
        ]
        """
        response = self.delete('tickets',json=tickets)
        return response

    def save_pagination(self, pagination_information):
        """
        Example for valid payload:

        [
            {
                "object_type": "tickets",
                "next_pull": "https://clubhouse.com/api/v1/tickets/next_object/foo",
                "query": "2021-04-01..2021-04-31"
            }
        ]
        """
        response = self.put('pagination',json=pagination_information)
        return response

    def get_pagination(self):
        """
        No Payload Required, returns all paginiation rows
        """
        response = self.get('pagination')
        return response

    def get_missing_individuals(self):
        """
        No Payload Required, returns all missing individuals
        """
        response = self.get('individuals','missing')
        return response

    def get_missing_statuses(self):
        """
        No Payload Required, returns all missing individuals
        """
        response = self.get('status','missing')
        return response

    def get_ticket(self, ticket_id):
        response = self.get('tickets',ticket_id)
        return response

    def get_fields(self):
        response = self.get('fields')
        return response
