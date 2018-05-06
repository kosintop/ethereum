from django.db import models


class Vendor(models.Model):
    name = models.TextField()
    contract_address = models.TextField(max_length=128)


class Reward(models.Model):
    name = models.TextField()
    point = models.IntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    tel = models.TextField()
    wallet_address = models.TextField(max_length=128)

