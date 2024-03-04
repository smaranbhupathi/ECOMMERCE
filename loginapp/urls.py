"""
loginapp/urls.py
"""
from django.urls import path
from .views import my_login_page, my_register_page, my_addnewuser_page, my_validatelogin_page, profile, edit_profile
from .views import my_admin_login_page, my_admin_validatelogin_page

urlpatterns = [
    path('', my_login_page),
    path('register/', my_register_page),
    path('addnewuser/', my_addnewuser_page),
    path('validatelogin/', my_validatelogin_page),
    path('admin/', my_admin_login_page),
    path('validateadminlogin/', my_admin_validatelogin_page),
    path('profile/',profile),
    path('profile/edit/',edit_profile )

]