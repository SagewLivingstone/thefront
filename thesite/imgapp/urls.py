from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('imglist/', views.image_list, name='image_list'),
     path('image/<int:image_id>/', views.image, name='image'),
     path('day/<int:year>/<int:month>/<int:day>/', views.day, name='day'),
]
