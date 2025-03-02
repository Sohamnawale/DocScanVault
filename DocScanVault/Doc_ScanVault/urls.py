from django.urls import path
from Doc_ScanVault import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login',views.login,name = 'login'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('upload', views.upload, name='upload')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)