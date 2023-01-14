from extras.plugins import PluginTemplateExtension
from django.contrib.contenttypes.models import ContentType
# from users_and_computers.models import RiskAssignment


class RiskVMPanel(PluginTemplateExtension):
    # model = 'users_and_computers.risk'
    model = 'virtualization.virtualmachine'




class RiskDevicePanel(PluginTemplateExtension):
    # model = 'users_and_computers.RiskRelation'
    model = 'dcim.device'
    # model = 'users_and_computers.riskrelation'




template_extensions = [RiskVMPanel, RiskDevicePanel]
