from django.contrib import admin
from bank_sync.models import Callbacks, RequestLogs, ResponseLogs, IPN, IPNData

# Register your models here.

admin.site.register(Callbacks)
admin.site.register(RequestLogs)
admin.site.register(ResponseLogs)
admin.site.register(IPN)
admin.site.register(IPNData)
