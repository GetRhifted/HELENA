from .models import Recetas, Predicciones
from rest_framework import viewsets, permissions
from .serializers import RecetasSerializer, PrediccionesSerializer

class RecetasViewSet(viewsets.ModelViewSet):
    queryset = Recetas.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RecetasSerializer

class PrediccionesViewSet(viewsets.ModelViewSet):
    queryset = Predicciones.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PrediccionesSerializer
