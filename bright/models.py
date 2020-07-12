from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Usertoken(models.Model):
    name = models.CharField(max_length=200, null=True)
    access_token = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Itemtoken(models.Model):
    access_token = models.CharField(max_length=200, null=True)
    item_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.item_id

class Availablebanks(models.Model):
    bank = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    def __str__(self):
        return self.bank