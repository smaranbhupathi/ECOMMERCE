"""
loginapp/models.py
"""
from django.db import models

# Create your models here.

class UserModel(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=10)
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'Users_table'

class AdminModel(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=10)
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'Admin_table'