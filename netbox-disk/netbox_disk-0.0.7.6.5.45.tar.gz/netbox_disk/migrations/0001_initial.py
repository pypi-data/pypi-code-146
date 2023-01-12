from django.db import migrations, models
import utilities.json


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name="Disk",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("vg_name", models.CharField(max_length=255)),
                ("lv_name", models.CharField(max_length=1000)),
                ("size", models.PositiveIntegerField()),
                ("path", models.CharField(max_length=255)),
                ('cluster',
                 models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='disks',
                                   to='virtualization.cluster')),
                ('virtual_machine',
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                                 related_name='disks', to='virtualization.virtualmachine')),
                ("description", models.CharField(max_length=1000)),
            ],
            options={
                "ordering": ("lv_name", "id"),
            },
        ),
        migrations.CreateModel(
            name="Filesystem",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("fs", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("fs", "id"),
            },
        ),
        migrations.CreateModel(
            name="Physicalvolume",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("size", models.PositiveIntegerField()),
                ('cluster',
                 models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='pv',
                                   to='virtualization.cluster')),
                ('virtual_machine',
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                   related_name='pv', to='virtualization.virtualmachine')),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("size", "id"),
            },
        ),
    ]
