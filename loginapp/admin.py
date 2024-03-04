"""
loginapp/admin.py
"""

from django.contrib import admin

# Register your models here.
from .models import UserModel, AdminModel
admin.site.register(UserModel)
admin.site.register(AdminModel)