from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_rds_iam_auth', '0026_tenant_parent_tenant'),
    ]

    operations = [
        migrations.RunSQL("""
            create function user_has_tenants(user_to_check text, tenant_to_check text) returns boolean
                security definer
                language plpgsql
            as
            $$
            DECLARE
                parent_tenant text;
                is_user_has_tenant boolean;
            BEGIN
                parent_tenant := (select parent_tenant_id from api_tenant where id = tenant_to_check);
                is_user_has_tenant := (select tenant_to_check in (
                    select origin_tenant_id from api_user where id = user_to_check
                ));
                if is_user_has_tenant then
                    return true;
                end if;
                if parent_tenant is null then
                    return false;
                else
                    return (select user_has_tenants(user_to_check, parent_tenant));
                end if;
            END;
            $$;
            """, reverse_sql="drop function user_has_tenants(text, text);"),
    ]
