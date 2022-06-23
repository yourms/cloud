from django.db import models


class User(models.Model):
    uno = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=10, blank=False)
    name = models.CharField(max_length=10, blank=False)
    password = models.CharField(max_length=10, blank=False)
    email = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=11, blank=False)
    address = models.CharField(max_length=100, blank=False)
    regdate = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'user'


class Product(models.Model):
    pno = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=10, blank=False)
    main = models.CharField(max_length=10, blank=False)
    sub1 = models.CharField(max_length=10, blank=False)
    sub2 = models.CharField(max_length=20, blank=False)
    specific = models.CharField(max_length=20, blank=False)
    manufacture = models.CharField(max_length=20, blank=False)
    name = models.CharField(max_length=30, blank=False)
    quantitiy = models.CharField(max_length=10, blank=False)
    nutrition = models.TextField(blank=False)
    price = models.IntegerField(blank=False)
    section = models.CharField(max_length=20, blank=False)
    location = models.CharField(max_length=20, blank=False)
    stock = models.CharField(max_length=20, blank=False)

    class Meta:
        db_table = 'product'


class List(models.Model):
    lno = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(auto_now=True, null=False)
    pno = models.IntegerField(blank=False)
    uno = models.IntegerField(blank=False)

    class Meta:
        db_table = 'list'
