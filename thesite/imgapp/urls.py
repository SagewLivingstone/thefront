from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     # path('imglist/', views.image_list, name='image_list'),
     path('image/<int:image_id>/', views.image, name='image'),
     path('day/<int:year>/<int:month>/<int:day>/', views.date, name='day'),
     path('month/<int:year>/<int:month>/', views.month, name='month'),
     path('year/<int:year>', views.year, name='year'),
     path('album/<int:id>', views.album, name='album'),
]
