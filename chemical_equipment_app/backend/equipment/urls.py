from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'datasets', views.DatasetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('summary/<int:dataset_id>/', views.get_summary, name='get_summary'),
    path('history/', views.get_history, name='get_history'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
]