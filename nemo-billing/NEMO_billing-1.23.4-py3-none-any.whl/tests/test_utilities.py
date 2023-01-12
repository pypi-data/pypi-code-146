from NEMO.models import Account, Area, Project, Tool, User

from NEMO_billing.invoices.models import ProjectBillingDetails


def basic_data() -> (User, Project, Tool, Area):
    test_user = User.objects.create(
        username="test", first_name="Test", last_name="Test", is_staff=False, badge_number=1
    )
    test_project = Project.objects.create(name="Test Project", account=Account.objects.create(name="Test Account"))
    test_project.projectbillingdetails = ProjectBillingDetails.objects.create(project=test_project)
    tool = Tool.objects.create(name="tool")
    area = Area.objects.create(name="Cleanroom")
    return test_user, test_project, tool, area
