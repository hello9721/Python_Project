# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Srtfcst(models.Model):
    datetime = models.TextField(db_column='Datetime', unique=True, blank=True, null=True)  # Field name made lowercase.
    t1h = models.TextField(db_column='T1H', blank=True, null=True)  # Field name made lowercase.
    rn1 = models.TextField(db_column='RN1', blank=True, null=True)  # Field name made lowercase.
    sky = models.TextField(db_column='SKY', blank=True, null=True)  # Field name made lowercase.
    reh = models.TextField(db_column='REH', blank=True, null=True)  # Field name made lowercase.
    pty = models.TextField(db_column='PTY', blank=True, null=True)  # Field name made lowercase.
    vec = models.TextField(db_column='VEC', blank=True, null=True)  # Field name made lowercase.
    wsd = models.TextField(db_column='WSD', blank=True, null=True)  # Field name made lowercase.
    uuu = models.TextField(db_column='UUU', blank=True, null=True)  # Field name made lowercase.
    vvv = models.TextField(db_column='VVV', blank=True, null=True)  # Field name made lowercase.
    lgt = models.TextField(db_column='LGT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        app_label = "Weather"
        db_table = 'SrtFcst'


class Srtncst(models.Model):
    datetime = models.TextField(db_column='Datetime', unique=True, blank=True, null=True)  # Field name made lowercase.
    t1h = models.TextField(db_column='T1H', blank=True, null=True)  # Field name made lowercase.
    rn1 = models.TextField(db_column='RN1', blank=True, null=True)  # Field name made lowercase.
    reh = models.TextField(db_column='REH', blank=True, null=True)  # Field name made lowercase.
    pty = models.TextField(db_column='PTY', blank=True, null=True)  # Field name made lowercase.
    vec = models.TextField(db_column='VEC', blank=True, null=True)  # Field name made lowercase.
    wsd = models.TextField(db_column='WSD', blank=True, null=True)  # Field name made lowercase.
    uuu = models.TextField(db_column='UUU', blank=True, null=True)  # Field name made lowercase.
    vvv = models.TextField(db_column='VVV', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        app_label = "Weather"
        db_table = 'SrtNcst'


class Vilagefcst(models.Model):
    datetime = models.TextField(db_column='Datetime', unique=True, blank=True, null=True)  # Field name made lowercase.
    pop = models.TextField(db_column='POP', blank=True, null=True)  # Field name made lowercase.
    pty = models.TextField(db_column='PTY', blank=True, null=True)  # Field name made lowercase.
    pcp = models.TextField(db_column='PCP', blank=True, null=True)  # Field name made lowercase.
    reh = models.TextField(db_column='REH', blank=True, null=True)  # Field name made lowercase.
    sno = models.TextField(db_column='SNO', blank=True, null=True)  # Field name made lowercase.
    sky = models.TextField(db_column='SKY', blank=True, null=True)  # Field name made lowercase.
    tmp = models.TextField(db_column='TMP', blank=True, null=True)  # Field name made lowercase.
    tmn = models.TextField(db_column='TMN', blank=True, null=True)  # Field name made lowercase.
    tmx = models.TextField(db_column='TMX', blank=True, null=True)  # Field name made lowercase.
    vec = models.TextField(db_column='VEC', blank=True, null=True)  # Field name made lowercase.
    wsd = models.TextField(db_column='WSD', blank=True, null=True)  # Field name made lowercase.
    uuu = models.TextField(db_column='UUU', blank=True, null=True)  # Field name made lowercase.
    vvv = models.TextField(db_column='VVV', blank=True, null=True)  # Field name made lowercase.
    wav = models.TextField(db_column='WAV', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        app_label = "Weather"
        db_table = 'VilageFcst'

class Location(models.Model):
    one = models.TextField(db_column='ONE', blank=True, null=True, default='')  # Field name made lowercase.
    two = models.TextField(db_column='TWO', blank=True, null=True, default='')  # Field name made lowercase.
    thr = models.TextField(db_column='THR', blank=True, null=True, default='')  # Field name made lowercase.
    x = models.IntegerField(db_column='X', blank=True, null=True, default='')  # Field name made lowercase.
    y = models.IntegerField(db_column='Y', blank=True, null=True, default='')  # Field name made lowercase.
    lng = models.TextField(db_column='LNG', blank=True, null=True, default='')  # Field name made lowercase.
    lat = models.TextField(db_column='LAT', blank=True, null=True, default='')  # Field name made lowercase.

    class Meta:
        managed = True
        app_label = "default"
        db_table = 'LOCATION'