from django.db import models


class Grade(models.Model):
    gno = models.AutoField(primary_key=True)
    grade = models.IntegerField(blank=True)

    class Meta:
        db_table = 'grade'


class User(models.Model):
    uno = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=10, blank=False)
    password = models.CharField(max_length=10, blank=False)
    email = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=10, blank=False)
    address = models.CharField(max_length=100, blank=False)
    gno = models.ForeignKey('Grade', models.DO_NOTHING, db_column='gno', blank=False, null=False)

    class Meta:
        db_table = 'user'


class Product(models.Model):
    pno = models.IntegerField(primary_key=True)
    id = models.IntegerField(max_length=10, blank=False)
    main = models.CharField(max_length=10, blank=False)
    sub1 = models.CharField(max_length=10, blank=False)
    sub2 = models.CharField(max_length=20, blank=False)
    specific = models.CharField(max_length=20, blank=False)
    quantity = models.CharField(max_length=10, blank=False)
    price = models.IntegerField(blank=False)
    section = models.CharField(max_length=20, blank=False)
    location = models.CharField(max_length=20, blank=False)
    stock = models.CharField(max_length=20, blank=False)

    class Meta:
        db_table = 'product'


class List(models.Model):
    lno = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(auto_now=True, null=False)
    pno = models.ForeignKey('User', models.DO_NOTHING, db_column='uno', blank=False, null=False)
    uno = models.ForeignKey('Product', models.DO_NOTHING, db_column='pno', blank=False, null=False)

    class Meta:
        db_table = 'list'