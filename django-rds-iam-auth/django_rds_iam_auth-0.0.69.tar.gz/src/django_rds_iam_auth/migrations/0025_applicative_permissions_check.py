from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_rds_iam_auth', '0025_api_scan_rls_generated'),
    ]

    operations = [
        migrations.RunSQL("""
                        create function ibrag_priviliged_has_applicative_permissions(text, text, text) returns boolean
                            security definer
                            language sql
                        as
                        $$
                        select case when count(id) > 0 then true else false end as result from api_user_user_permissions  where user_id=$1 and permission_id = (
                            select id from auth_permission where codename = concat($2,'_',$3))
                        $$; 
                    """, reverse_sql="drop function ibrag_priviliged_has_applicative_permissions(text, text, text);"),
    ]
