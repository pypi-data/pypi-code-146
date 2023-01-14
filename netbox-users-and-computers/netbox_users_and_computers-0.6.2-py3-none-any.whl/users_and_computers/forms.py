from netbox.forms import NetBoxModelForm
from pyrsistent import v
from .models import Risk, RiskRelation#, RiskAssignment
from utilities.forms import (
    BootstrapMixin, DynamicModelChoiceField)
from django import forms


class RiskForm(NetBoxModelForm):
    class Meta:
        model = Risk
        fields = ('name',
                  'sAMAccountName',
                  'status',
                  'firstname',
                  'lastname', 'ad_guid', 'ad_description', 'position', 'department', 'comment',
                  'vpnIPaddress',
                  'description',
                  'comments')


class RiskRelationForm(NetBoxModelForm):
    class Meta:
        model = RiskRelation
        fields = ('name', 'CN', 'DistinguishedName', 'ad_guid', 'ad_description', 'description')

