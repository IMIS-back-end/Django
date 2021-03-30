from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)    # Varchar(32)
    password = models.CharField(max_length=32)


class Publisher(models.Model):
    name = models.CharField(max_length=32)


class Book(models.Model):
    name = models.CharField(max_length=32)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)    # Foreign key connected with publisher


"""

on_delete:
        models.CASCADE Delete the connected values with the parent entity
        models.PROTECT Save the connected values when deleting the parent entity
        models.SETDEFAULT set the value to default when deleting the parent entity
        models.SET_NULL Set the value to NULL after deleting the parent entity 

"""