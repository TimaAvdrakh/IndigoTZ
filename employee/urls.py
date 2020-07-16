# from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('load/',views.load_data, name='load'),
    path('list/',views.list_data, name='list'),
    path('list/<to_sort>', views.sorted_data, name='sorted'),
    path('delete/<rank>', views.delete_view, name='delete'),
    path('add',views.add_view, name='add'),
    path('download', views.download_data, name='download')

]