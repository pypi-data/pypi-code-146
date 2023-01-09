from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_rds_iam_auth', '0057_applicationrestriction'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                DROP POLICY api_user_table_policy ON api_user;
                CREATE POLICY api_user_table_policy ON api_user
                USING (((id)::text = CURRENT_USER) OR privileged_user_has_tenant((CURRENT_USER)::text, (origin_tenant_id)::text))
                WITH CHECK (((id)::text = CURRENT_USER) OR
                privileged_user_has_tenant((CURRENT_USER)::text, (origin_tenant_id)::text));
            """,
            reverse_sql="DROP POLICY api_user_table_policy ON api_user;"
        ),
    ]
