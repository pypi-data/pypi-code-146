from django.db import models
from django.utils import timezone


class Callbacks(models.Model):
    bank_id = models.IntegerField()
    type_code = models.IntegerField()
    reference = models.CharField(max_length=100, unique=True)
    callback = models.TextField()
    request = models.JSONField(default=dict)
    response = models.JSONField(default=dict)
    request_time = models.DateTimeField(default=timezone.now)
    response_time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Callback"
        verbose_name_plural = "Callbacks"

    def __str__(self):
        return self.reference

    def __repr__(self):
        return f'Callbacks(reference="{self.reference}",callback="{self.callback}", request={self.request}, response={self.response})'


class RequestLogs(models.Model):
    ip = models.CharField(max_length=50)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=100)
    content_type = models.CharField(max_length=50)
    content_params = models.JSONField(default=dict)
    body = models.JSONField(default=dict)
    headers = models.JSONField(default=dict)
    user = models.CharField(max_length=100)
    error = models.TextField(default=None, null=True)
    log_time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f'{self.log_time.strftime("%d %B %Y - %H:%M:%S")} {self.ip} {self.method} {self.path}'

    def __repr__(self):
        return f'RequestLogs(ip="{self.ip}", method="{self.method}", path="{self.path}", content_type="{self.content_type}", content_params="{self.content_params}", body="{self.body}", headers="{self.headers}", user="{self.user}")'


class ResponseLogs(models.Model):
    ip = models.CharField(max_length=50, default=None, null=True)
    headers = models.JSONField(default=dict)
    content = models.JSONField(default=dict)
    log_time = models.DateTimeField(default=timezone.now)
    error = models.TextField(default=None, null=True)

    def __str__(self):
        return f'{self.log_time.strftime("%d %B %Y - %H:%M:%S")} {self.ip}'

    def __repr__(self):
        return f'ResponseLogs(headers="{self.headers}", content="{self.content}")'

    class Meta:
        verbose_name = "Response Log"
        verbose_name_plural = "Response Logs"

# This class is used to create/save user I.P.N. callbacks that are to listen on any changes on a specified bank and account number


class IPN(models.Model):
    client_id = models.CharField(max_length=200, unique=True)
    signature = models.CharField(max_length=200, unique=True)
    bank_id = models.IntegerField()
    country_code = models.CharField(max_length=5, default='KE')
    account_number = models.CharField(max_length=200, unique=True)
    url = models.URLField()

    IPNSTATUS = [
        (True, 'Active'),
        (False, 'Inactive')
    ]
    status = models.BooleanField(choices=IPNSTATUS, default=True)

    IPNTYPE = [
        (2, 'Debit'),
        (1, 'Credit'),
        (0, 'Both')
    ]

    ipn_type = models.IntegerField(choices=IPNTYPE,
                                   default=0,)

    def __str__(self):
        return f'{self.client_id} : I.P.N. Type - {[i[1] for i in self.IPNTYPE if i[0] == self.ipn_type][0]} : Status - {[i[1] for i in self.IPNSTATUS if i[0] == self.status][0]}'

    def __repr__(self):
        return f'IPN(client_id="{self.client_id}", bank_id="{self.bank_id}", country_code="{self.country_code}", account_number="{self.account_number}", ipn_type={self.ipn_type}, status={self.status})'


# This class is used to create/save user I.P.N. data sent back
class IPNData(models.Model):
    ipn = models.ForeignKey(IPN, on_delete=models.CASCADE)
    response = models.JSONField(default=dict)
    response_time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "IPNData"
        verbose_name_plural = "IPNData"

    def __str__(self):
        return str(self.ipn)

    def __repr__(self):
        return f'IPNData(ipn_pk="{self.ipn.pk}", response={self.response})'
