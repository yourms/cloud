from django.db import models


class Manager(models.Model):
    mno = models.IntegerField(primary_key=True, auto_created=True)
    idweb = models.CharField(max_length=10, blank=False)
    passwordweb = models.CharField(max_length=20, blank=False)
    emailweb = models.CharField(max_length=100, blank=False)
    phoneweb = models.CharField(max_length=11, blank=False)
    addressweb = models.CharField(max_length=100, blank=False)

    class Meta:
        db_table = 'manager'


class Notepadmdl(models.Model):
    noteno = models.IntegerField(primary_key=True, auto_created=True)
    writer = models.CharField(max_length=100, blank=False)
    info1 = models.CharField(max_length=200)
    info2 = models.CharField(max_length=200)
    info3 = models.CharField(max_length=200)
