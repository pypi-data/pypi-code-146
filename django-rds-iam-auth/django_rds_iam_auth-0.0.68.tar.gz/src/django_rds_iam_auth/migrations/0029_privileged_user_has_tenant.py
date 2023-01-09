from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('django_rds_iam_auth', '0028_privileged_get_user_tenants'),
    ]

    operations = [
        migrations.RunSQL("""
                create function privileged_user_has_tenant(user_to_check text, tenant_to_check text) returns boolean
                    security definer
                    language sql
                as
                $$
                SELECT tenant_to_check in (select privileged_get_user_tenants(user_to_check));
                $$;
            """, reverse_sql="drop function privileged_user_has_tenant(text, text);"),
    ]
