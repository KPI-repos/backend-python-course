from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # User URLs
    path('users/', views.users_list, name='users_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/update/', views.user_update, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    
    # Dish URLs
    path('dishes/', views.dishes_list, name='dishes_list'),
    path('dishes/create/', views.dish_create, name='dish_create'),
    path('dishes/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('dishes/<int:dish_id>/update/', views.dish_update, name='dish_update'),
    path('dishes/<int:dish_id>/delete/', views.dish_delete, name='dish_delete'),
    
    # Order URLs
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/update/', views.order_update, name='order_update'),
    path('orders/<int:order_id>/delete/', views.order_delete, name='order_delete'),
]