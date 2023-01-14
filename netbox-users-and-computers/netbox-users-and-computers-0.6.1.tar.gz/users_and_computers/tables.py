import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import Risk, RiskRelation#, RiskAssignment


class RiskTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    # default_action = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = Risk
        fields = ('pk', 'name', 'sAMAccountName',
                  'status',
                  'firstname',
                  'lastname', 'ad_guid', 'ad_description', 'position', 'department', 'comment',
                  'vpnIPaddress', 'description')
        default_columns = ('name', 'sAMAccountName',
                  'status',
                  'firstname',
                  'lastname', 'ad_guid', 'description')


class RiskRelationTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = RiskRelation
        fields = ('pk', 'name', 'description')
        default_columns = ('name', 'description')


