from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

@method_decorator(csrf_exempt, name='dispatch')
class PaymentAuthResponseView(View):

    def post(self, request, order_id=None):
        payment_response = json.loads(request.POST.get('Response'))

        if order_id is None:
            order_id = payment_response.get("OrderIdentifier")

        # TODO: Find a generic way to determine if a transaction is successful
        transaction_successful = True

        if transaction_successful:
            return self.authorization_successful(order_id, payment_response)

        return self.authorization_failed(order_id, payment_response)


    def authorization_successful(self, order_id, payment_response):
        pass

    def authorization_failed(self, order_id, payment_response):
        pass