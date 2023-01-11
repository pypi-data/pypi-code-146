from django.db import models
from xj_user.models import Platform


# Create your models here.

# 1、migrate_platform_table  迁移平台表 [NF1]
class MigratePlatformTable(models.Model):
    plaform = models.ForeignKey(Platform, verbose_name='用户', on_delete=models.DO_NOTHING, db_column='plaform_id',
                                help_text='')
    # plaform_id = models.IntegerField(verbose_name='平台id', blank=True, null=True, db_index=True)
    table_name = models.CharField(verbose_name='平台表名', max_length=128, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'migrate_platform_table'
        verbose_name_plural = "01. 迁移平台表"

    def __str__(self):
        return f"{self.plaform_id}"


# 2、migrate_old_to_new  迁移旧表到新表id的映射表 [NF1]
class MigrateOldToNew(models.Model):
    old_table = models.ForeignKey(MigratePlatformTable, verbose_name='旧表id', on_delete=models.DO_NOTHING,
                                  related_name="old_table")
    new_table = models.ForeignKey(MigratePlatformTable, verbose_name='旧表id', on_delete=models.DO_NOTHING,
                                  related_name="new_table"
                                  )
    old_data_id = models.IntegerField(verbose_name='旧表主键id', blank=True, null=True, db_index=True)
    new_data_id = models.IntegerField(verbose_name='新表主键id', blank=True, null=True, db_index=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, )
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True, blank=True, null=True, )

    class Meta:
        db_table = 'migrate_old_to_new'
        verbose_name_plural = "02. 迁移旧表到新表id的映射表"

    def __str__(self):
        return f"{self.old_table_id}"


# 3、migrate_table_key_map  迁移键名映射表 [NF1]
class MigrateTableKeyMap(models.Model):
    old_table = models.ForeignKey(MigratePlatformTable, verbose_name='旧表id', on_delete=models.DO_NOTHING,
                                  related_name="old_tables")
    new_table = models.ForeignKey(MigratePlatformTable, verbose_name='旧表id', on_delete=models.DO_NOTHING,
                                  related_name="new_tables"
                                  )
    old_key_name = models.CharField(verbose_name='旧表映射字段', max_length=255, blank=True, null=True, help_text='')
    new_key_name = models.CharField(verbose_name='新表映射字段', max_length=255, blank=True, null=True, help_text='')
    is_primary_key = models.IntegerField(verbose_name='是否主键idid', blank=True, null=True, db_index=True)
    config = models.CharField(verbose_name='配置', max_length=255, blank=True, null=True, help_text='')

    class Meta:
        db_table = 'migrate_table_key_map'
        verbose_name_plural = "03. 迁移键名映射表"

    def __str__(self):
        return f"{self.old_table_id}"
