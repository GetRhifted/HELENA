from rest_framework import routers
from .api import RecetasViewSet, PrediccionesViewSet
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register('api/Recetas', RecetasViewSet, 'Recetas')
router.register('api/Predicciones', PrediccionesViewSet, 'Predicciones')

urlpatterns = [
    # URL para la vista guardar_recetas
    path('api/guardar_recetas/', views.guardar_recetas, name='guardar_recetas'),
    path('api/guardar_predicciones', views.guardar_predicciones, name='guardar_predicciones'),
]

urlpatterns += router.urls

