

class CustomerService:
    api_url = "customers"

    def __init__(self, servicefusion):
        super().__init__(servicefusion)
    
    def get_customer_by_id(self, customer_id):
        params = {
            'expand': 'contacts.emails, custom_fields, contacts.phones, locations'
        }
        return self._get(f'{self.api_url}/{customer_id}', **params)

    def get_customer_by_name(self, firstname, lastname):
        params = {
            'filters[name]': f"{firstname} {lastname}",
            'fields': 'id',
            'expand': 'contacts.emails, contacts.phones'
        }
        return self._get(f'{self.api_url}', **params)

    def get_customer_by_email(self, customer_email):
        params = {
            'filters[email]': customer_email,
            'fields': 'id'
        }
        return self._get(f'{self.api_url}', **params)
