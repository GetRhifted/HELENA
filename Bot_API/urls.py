from rest_framework import routers
from .api import RecetasViewSet
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register('api/Recetas', RecetasViewSet, 'Recetas')

urlpatterns = [
    # URL para la vista guardar_recetas
    path('api/guardar_recetas/', views.guardar_recetas, name='guardar_recetas'),
]

urlpatterns += router.urls

