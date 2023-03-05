from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.download_file, name='download-file'),
    path('open/<int:id>/', views.open_file, name='open-file'),
]
