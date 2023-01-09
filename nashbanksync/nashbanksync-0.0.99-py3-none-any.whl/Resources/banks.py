from bank_sync.Resources.resource import Resource
from bank_sync.Resources.accounts import Accounts
from bank_sync.Resources.payments import Payments
from bank_sync.models import IPN
from django.core.exceptions import ObjectDoesNotExist
try:
    from django.conf import settings
except Exception as e:
    pass


class Bank(Resource):

    _resources = {
        "Accounts": Accounts(),
        "Payments": Payments(),
    }

    # use the nash object to confirm if the user accessing the banks is logged in
    _nash = None

    urls = {}

    # By default the library will set a url to use for ipn callbacks when registering an IPN
    bank_sync_ipn_urls = {}

    # This IPN callback is set in the django settings module
    # When a user registeres for an IPN using this service the sync will save the user url and forward the service url to Nash core
    # Nash will then forward ipn data to this service whihc then forwards it to the saved/registered user url
    try:
        bank_sync_ipn_urls = getattr(
            settings, 'BANK_SYNC_IPN_URLS', bank_sync_ipn_urls)
    except Exception as e:
        pass

    def __init__(self, nash, bank_id=None):
        self._nash = nash
        super().__init__("BankAPI", self._nash.get_headers(), self._nash.get_params())
        super().set_bank_id(bank_id)

        super().refresh_identity_token()

    def resource(self, resource_name):
        resource = self._resources[resource_name].set_bank_id(
            super().get_bank_id()).set_headers(self._nash.get_headers()).set_identity_token(identity_token=super().get_identity_token)

        return resource

    def get_resources(self):
        return list(self._resources.keys())

    def callback(self, bank_name=None, payload=None, method='POST', endpoint='/callback'):

        if bank_name is not None:
            endpoint = f'{endpoint}/{bank_name}'

        return super().read(payload, method, endpoint)

    # This is a 'global' function
    # Used to get operations supported by Nash
    def bank_operations(self):
        return self.exec_global_function(operation=super().OPERATIONS)

    # This is a 'global' function
    # Used to get banks supported by Nash
    def bank_types(self):
        return self.bank_types_by_id()

    # This is a 'global' function
    # Used to get results of jobs that were scheduled
    def jobs(self, operation=None, payload=None):

        # The response returned is the raw response sent by banks before any standardizations
        rsp = self.exec_global_function(
            operation=operation, payload=payload).response()

        # The jobs that are currently being run are Account APIs get Account Balance and Account Full Statement API
        # For the above reason we will then initia.ize an Account Class that is responsible for standardizing Account APIs responses
        accounts = Accounts()
        # Set the bank id to identify the bank response being standardized
        accounts.set_bank_id(bank_id=rsp.get('bank_id'))
        # Set the operation to identify the bank api being standardized
        accounts.set_operation(operation=operation)
        # The set the response method is where the responses are standardized
        accounts.set_response(response=rsp)

        return accounts

    # This is a 'global' function used to:
    # 1. Register a user's I.P.N.'s in Nash
    # 2. Get a user's registered I.P.N.'s in Nash
    # 3. Update a user's registered I.P.N.'s in Nash
    # 4. Delete a user's registered I.P.N.'s in Nash

    # Here once an IPN is saved in Nash, we will create a replica DB that will also store, update or delete the IPN

    # We do this so that when an IPN is sent to us, we simply confirm if the if the IPN sent is coming from Nash
    # by comparing the security credentials and the account number sent at the endpoint responsible of standardizing
    # the response
    def ipn(self, operation=None, payload=None):
        # Get the user passed url
        user_url = payload.get('url', '')

        # if a user passed a url, swap it with the service url
        if 'url' in payload.keys():
            payload['url'] = self.bank_sync_ipn_urls.get("payments", "")

        # excute the IPN call
        exec_global = self.exec_global_function(
            operation=operation, payload=payload)

        try:

            if operation in [super().IPN_REGISTER]:
                # get the response and change the url saved, which it the service url, with the user url
                rsp = super().response()
                rsp['url'] = user_url
                super().set_response(response=rsp)

            # If the operation performed is to create an IPN
            if operation == super().IPN_REGISTER:
                # If succesfull Nash returns the generated client id and client secret
                if 'client_id' in super().response().keys() and 'client_secret' in super().response().keys():
                    signature = self.generate_signature(secret=super().response().get(
                        'client_secret'), message=f"{super().response().get('client_id')}:{super().response().get('client_secret')}")

                    IPN.objects.create(bank_id=payload.get('bank_id', ''), client_id=super().response().get(
                        'client_id', ''), signature=signature, country_code=payload.get('country_code', ''), account_number=payload.get('account_number', ''), url=user_url)

            # If the operation performed is to update an IPN
            elif operation == super().IPN_GET:
                # If succesfull Nash returns the client id and account_number
                if 'client_id' in super().response().keys() and 'account_number' in super().response().keys():

                    data = IPN.objects.get(client_id=super().response().get(
                        'client_id', ''), account_number=super().response().get('account_number', ''))

                    # if bool(len(data)):
                    #     data = data.first()

                    rsp = super().response()
                    rsp['url'] = data.url
                    super().set_response(response=rsp)

            # If the operation performed is to update an IPN
            elif operation == super().IPN_GENERATE_CLIENT_SECRET:
                # If succesfull Nash returns the client id
                if 'client_id' in super().response().keys():

                    data = IPN.objects.get(client_id=payload.get(
                        'client_id', ''), account_number=payload.get('account_number', ''))

                    if 'client_secret' in super().response().keys():
                        data.signature = self.generate_signature(secret=super().response().get(
                            'client_secret'), message=f"{super().response().get('client_id')}:{super().response().get('client_secret')}")

                    data.save()

            # If the operation performed is to update an IPN
            elif operation == super().IPN_UPDATE:
                # If succesfull Nash returns the client id
                if 'client_id' in super().response().keys():

                    data = IPN.objects.get(
                        client_id=payload.get('client_id', ''))
                        
                    if 'bank_id' in payload.keys():
                        data.bank_id = payload.get('bank_id')
                    if 'account_number' in payload.keys():
                        data.account_number = payload.get(
                            'account_number')
                    if 'country_code' in payload.keys():
                        data.country_code = payload.get('country_code')
                    if 'url' in payload.keys():
                        data.url = user_url
                    if 'status' in payload.keys():
                        data.status = payload.get('status')
                    if 'ipn_type' in payload.keys():
                        data.ipn_type = payload.get('ipn_type')

                    data.save()

            # If the operation performed is to delete an IPN
            elif operation == super().IPN_DELETE:
                # If succesfull Nash returns the client id
                if 'client_id' in super().response().keys():

                    data = IPN.objects.get(client_id=payload.get(
                        'client_id', ''))
                        
                    data.delete()

        except ObjectDoesNotExist:
            print("Either the blog or entry doesn't exist.")

        return exec_global

    # This is a 'global' function
    # Used to get banks supported by Nash
    def bank_types_by_id(self, bank_id=None):
        return self.exec_global_function(operation=super().BANKS_BY_ID, bank_id=bank_id)

    # This is a 'global' function
    # Used to get banks supported by Nash
    def bank_types_by_code(self, bank_code=None):
        return self.exec_global_function(operation=super().BANKS_BY_CODE, bank_id=bank_code)

    # This is a 'global' function
    # Used to get sample_payloads for a resource's end point
    def sample_payload(self, bank_id=None, payload=None):
        return self.exec_global_function(operation=super().SAMPLE_DATA, bank_id=bank_id, payload=payload)

    # This is a 'global' function
    # Used to get sample_payloads for a resource's end point
    def countries(self, payload=None):
        return self.exec_global_function(operation=super().COUNTRIES, payload=payload)

    # This method is responsible for returning the bank id that's to execute the 'global' functions
    def exec_global_function(self, operation=0, bank_id=None, payload=None):
        data = {}
        # Set the operation to be performed
        super().set_operation(operation)

        # If a bank id is supplied
        if bank_id is not None:
            # If a user did not set a bank id
            if super().get_bank_id() < 1:
                # If a user did not set a bank id, set the bank_id to the Global Biller ID 0
                super().set_bank_id(super().GLOBAL)
                # Executing the method below after setting the Global Biller ID will ensure
                # that we are calling/get access to the SAMPLE_DATA operation found
                # linked to the Global ID. Pass the bank id whose sample data the user wants
                data = super().read(payload, params=f'bank_id={bank_id}')

            # If a user set a bank id
            elif super().get_bank_id() > 0:
                # Since operations are linked to a bank id, we want to get access to the Global Biller ID,
                # so as to get access to the SAMPLE_DATA operation, execute the call, then set bank id to
                # the user's bank ID

                # Get the user's bank id and save it temporarily (temp)
                temp = super().get_bank_id()
                # Set the bank id to the Global Biller ID
                super().set_bank_id(super().GLOBAL)

                # Execite the SAMPLE_DATA operation
                # Pass the bank id whose sample data the user wants
                data = super().read(payload, params=f'bank_id={bank_id}')

                # reset the bank_id to the bank id set by the user before (temp)
                super().set_bank_id(temp)

        # If a bank id is not supplied
        else:
            # If a user did not set a bank id
            if super().get_bank_id() < 1:
                # If a user did not set a bank id, set the bank_id to the Global Biller ID 0
                super().set_bank_id(super().GLOBAL)
                # Executing the method below after setting the Global Biller ID will ensure
                # that we are calling/get access to the SAMPLE_DATA operation found
                # linked to the Global ID. Pass the bank id whose sample data the user wants
                data = super().read(payload, params=f'bank_id={bank_id}')

            # If a user did set a bank id
            elif super().get_bank_id() > 0:
                # Since operations are linked to a bank id, we want to get access to the Global Biller ID,
                # so as to get access to the SAMPLE_DATA operation, execute the call, then set bank id to
                # the user's bank ID

                # Get the user's bank id and save it temporarily (temp)
                temp = super().get_bank_id()
                # Set the bank id to the Global Biller ID
                super().set_bank_id(super().GLOBAL)

                # Execite the SAMPLE_DATA operation
                # Pass the bank id whose sample data the user wants
                data = super().read(payload, params=f'bank_id={bank_id}')
                # Set bank id to back the user's orginal bank id
                super().set_bank_id(temp)

        # The 'if else' complexities above are done to ensure that the users can call this method
        # anywhere in their code, if they wish to get a sample data

        return data
