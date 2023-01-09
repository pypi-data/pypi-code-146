from django.db import migrations
import django_rds_iam_auth.aws.utils.rls_helpers


class Migration(migrations.Migration):

    dependencies = [
        ('django_rds_iam_auth', '0025_api_customer_rls_generated'),
        ('django_rds_iam_auth', '0024_auto_20200724_2024'),
    ]

    operations = [
        # django_rds_iam_auth.aws.utils.rls_helpers.CreateRLSPolicyOperation(
        #     table_name='api_scan',
        #     policy_name='api_scan_table_policy',
        #     useing_rule="(ibrag_is_super_admin(current_user) or (ibrag_user_has_role('tenant_admin') and ibrag_user_has_tenant(tenant_id)) or ibrag_priviliged_is_owner_of_user(owner_id, current_user))",
        #     with_check_rule="(ibrag_is_super_admin(current_user)  or (ibrag_user_has_role('tenant_admin') and ibrag_user_has_tenant(tenant_id)) or ibrag_priviliged_is_owner_of_user(owner_id, current_user))",
        # ),
    ]
