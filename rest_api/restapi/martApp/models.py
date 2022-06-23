from django.db import models

# Create your models here.
class MartMap(models.Model):
    row   = models.CharField(max_length=2)
    col  = models.CharField(max_length=2)
    type  = models.CharField(max_length=10) # way, stand
    junction   = models.BooleanField(default=0) # 0==False
    class Meta:
        db_table = "MartMap"
        constraints = [
            models.UniqueConstraint(
                fields=["row","col"],
                name="unique MartMap",
            )
        ]
# Create your models here.
class Location(models.Model):
    loc   = models.CharField(max_length=4, primary_key=True)
    minx  = models.FloatField()
    maxx  = models.FloatField()
    miny = models.FloatField()
    maxy = models.FloatField()














































