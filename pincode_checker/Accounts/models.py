from django.db import models

# Create your models here.


class UserAddress(models.Model):
    id = models.AutoField(primary_key=True)
    pincode = models.BigIntegerField(unique=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    division = models.CharField(max_length=50)

    def __str__(self):
        return self.pincode


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.ForeignKey(UserAddress, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
