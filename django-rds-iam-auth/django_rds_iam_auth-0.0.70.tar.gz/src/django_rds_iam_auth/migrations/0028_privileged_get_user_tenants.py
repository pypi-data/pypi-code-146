from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_rds_iam_auth', '0027_user_has_tenants'),
    ]

    operations = [
        migrations.RunSQL("""
            create function privileged_get_user_tenants(text)
                returns SETOF text
                security definer
                language sql
                as
                $$
                    WITH RECURSIVE r AS (
                        SELECT tenant_id, parent_tenant_id
                        FROM (
                            select tenant_id, parent_tenant_id, user_id
                            from api_tenant_users
                            join api_tenant a
                            on a.id = api_tenant_users.tenant_id and user_id = $1
                        ) as temp_tenant_table
            
                        UNION
            
                        SELECT a.id, a.parent_tenant_id
                        FROM api_tenant a
                            JOIN r
                                 ON a.parent_tenant_id = r.tenant_id
                    )
                    SELECT tenant_id FROM r;
                $$;
            """, reverse_sql="drop function privileged_get_user_tenants(text);"),
    ]
