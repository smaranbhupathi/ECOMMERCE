from django.urls import path
from . import views
from .views import allOrders, address


urlpatterns = [
    path("", views.index, name="ShopHome"),
    # path("login/", views.login, name="Login"),
    # path("logout/", views.logout, name="Logout"),
    # path("register/", views.register, name="Register"),
    # path("addUser/", views.addUser, name="addUser"),
    # path("addAdmin/", views.addAdmin, name="addAdmin"),
    # path("validateUser/", views.validateUser, name='validateUser'),
    # path("validateAdmin/", views.validateAdmin, name='validateAdmin'),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("orders/", views.orders, name="orders"),
    path('add_rating/<int:order_id>/<str:product_key>/', views.add_rating, name='add_rating'),
    path('add_comment/<int:order_id>/<str:product_key>/', views.add_comment, name='add_comment'),
    path('search-recommendations/', views.search_recommendations, name='search_recommendations'),
    path('logout/', views.my_logout_page, name="Logout"),
    path('profile/address/add/', views.add_address, name='add_address'),
    path('profile/address/delete/<int:address_id>/', views.delete, name='delete_address'),
    path('profile/address/', address, name='address'),
    path('adminpage/', views.adminpage, name="Admin"),
    path('adminpage/allOrders/', allOrders, name='all_orders'),
    path('adminpage/addProduct/', views.addProductPage, name='all_product'),
    path('adminpage/updateStatus/', views.updateStatusPage, name='updatedstatuspage'),
    path('adminpage/addProduct/addProducttoDB', views.addtoDB, name='addproducttodb'),
    path('adminpage/updatecurrentStatus/', views.updatecurrentStatus, name='updateStatus'),

]
