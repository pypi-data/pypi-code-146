# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Events(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    ra = models.FloatField()
    decl = models.FloatField()
    ra_original = models.FloatField()
    decl_original = models.FloatField()
    date_inserted = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True, null=True)
    year = models.PositiveSmallIntegerField()
    base26suffix = models.CharField(max_length=20)
    htm16id = models.BigIntegerField(db_column='htm16ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'events'
        unique_together = (('year', 'base26suffix'),)


class Akas(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Events, to_field='id', db_column='event_id', on_delete = models.CASCADE)
    object_id = models.BigIntegerField()
    aka = models.CharField(max_length=30, blank=True, null=True)
    ra = models.FloatField()
    decl = models.FloatField()
    survey_database = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    source_ip = models.CharField(max_length=20, blank=True, null=True)
    original_flag_date = models.DateField()
    date_inserted = models.DateTimeField()
    htm16id = models.BigIntegerField(db_column='htm16ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'akas'
        unique_together = (('object_id', 'survey_database'),)



class AbstractYear(models.Model):
    id = models.AutoField(primary_key=True)
    object_id = models.BigIntegerField()
    ra = models.FloatField()
    decl = models.FloatField()
    survey_database = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    source_ip = models.CharField(max_length=20, blank=True, null=True)
    date_inserted = models.DateTimeField()
    htm16id = models.BigIntegerField(db_column='htm16ID')  # Field name made lowercase.

    class Meta:
        abstract = True


class Y2013(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2013'
        unique_together = (('object_id', 'survey_database'),)

class Y2014(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2014'
        unique_together = (('object_id', 'survey_database'),)

class Y2015(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2015'
        unique_together = (('object_id', 'survey_database'),)

class Y2016(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2016'
        unique_together = (('object_id', 'survey_database'),)

class Y2017(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2017'
        unique_together = (('object_id', 'survey_database'),)

class Y2018(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2018'
        unique_together = (('object_id', 'survey_database'),)

class Y2019(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2019'
        unique_together = (('object_id', 'survey_database'),)

class Y2020(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2020'
        unique_together = (('object_id', 'survey_database'),)

class Y2021(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2021'
        unique_together = (('object_id', 'survey_database'),)

class Y2022(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2022'
        unique_together = (('object_id', 'survey_database'),)

class Y2023(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2023'
        unique_together = (('object_id', 'survey_database'),)

class Y2024(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2024'
        unique_together = (('object_id', 'survey_database'),)

class Y2025(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2025'
        unique_together = (('object_id', 'survey_database'),)

class Y2026(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2026'
        unique_together = (('object_id', 'survey_database'),)

class Y2027(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2027'
        unique_together = (('object_id', 'survey_database'),)

class Y2028(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2028'
        unique_together = (('object_id', 'survey_database'),)

class Y2029(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2029'
        unique_together = (('object_id', 'survey_database'),)

class Y2030(AbstractYear):

    class Meta:
        managed = False
        db_table = 'y2030'
        unique_together = (('object_id', 'survey_database'),)


