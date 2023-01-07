# Generated by Django 2.2.24 on 2021-10-07 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trosnoth', '0033_trosnotharena_extra_bot_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='trosnothserversettings',
            name='manhole_authorised_keys',
            field=models.TextField(blank=True, help_text='Public key strings to be accepted by manhole.', verbose_name='Authorised manhole public keys'),
        ),
    ]
