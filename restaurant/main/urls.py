from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users_list, name='users_list'),
    path('dishes/', views.dishes_list, name='dishes_list'),
    path('orders/', views.orders_list, name='orders_list'),
    
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('dishes/<int:dish_id>/', views.dish_detail, name='dish_detail'),
]