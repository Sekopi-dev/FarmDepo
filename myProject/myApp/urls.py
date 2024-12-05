from . import views 
from django.urls import path, include


from django.urls import path

urlpatterns = [
    path("", views.home, name="index"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('update_user/', views.update_user, name="update_user"),
    path('product/<int:pk>', views.product, name="product"),
    path('myaccount/', views.myaccount, name="myaccount"),
    path('category/<int:category_id>/', views.category, name='category'),
    path('order_detail/<int:order_id>', views.order_detail, name="order_detail"),
    
    path('search', views.search, name="search"),


    

    path('cart/', include('cart.urls')),
]