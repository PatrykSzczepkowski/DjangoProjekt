from django.urls import path

from . import views
from .views import create_car, get_car, update_car, delete_car, car_list, create_owner, get_owner, update_owner, \
    delete_owner, create_vehicle_history, get_vehicle_history, update_vehicle_history, delete_vehicle_history, \
    create_car_image, get_car_image, update_car_image, delete_car_image, pricegt, pricelt, register_user, \
    CustomAuthTokenLogin

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', CustomAuthTokenLogin.as_view()),
    path('register/', register_user, name='register_user'),
    path('car/pricegt/<int:price>/', pricegt, name='pricegt'),
    path('car/pricelt/<int:price>/', pricelt, name='pricelt'),
    path('car/car_list', car_list, name='car_list'),
    path('car/create/', create_car, name='create_car'),
    path('car/<int:pk>/', get_car, name='get_car'),
    path('car/update/<int:pk>/', update_car, name='update_car'),
    path('car/delete/<int:pk>/', delete_car, name='delete_car'),
    path('owner/create/', create_owner, name='create_owner'),
    path('owner/<int:pk>/', get_owner, name='get_owner'),
    path('owner/update/<int:pk>/', update_owner, name='update_owner'),
    path('owner/delete/<int:pk>/', delete_owner, name='delete_owner'),
    path('vehicle_history/create/', create_vehicle_history, name='create_vehicle_history'),
    path('vehicle_history/<int:pk>/', get_vehicle_history, name='get_vehicle_history'),
    path('vehicle_history/update/<int:pk>/', update_vehicle_history, name='update_vehicle_history'),
    path('vehicle_history/delete/<int:pk>/', delete_vehicle_history, name='delete_vehicle_history'),
    path('car_image/create/', create_car_image, name='create_car_image'),
    path('car_image/<int:pk>/', get_car_image, name='get_car_image'),
    path('car_image/update/<int:pk>/', update_car_image, name='update_car_image'),
    path('car_image/delete/<int:pk>/', delete_car_image, name='delete_car_image'),
]