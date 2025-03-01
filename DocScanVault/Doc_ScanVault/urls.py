from django.urls import path
from Doc_ScanVault import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index')
]