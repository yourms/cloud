from django.db import models

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