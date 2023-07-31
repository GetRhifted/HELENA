from .models import Recetas
from rest_framework import viewsets, permissions
from .serializers import RecetasSerializer

class RecetasViewSet(viewsets.ModelViewSet):
    queryset = Recetas.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RecetasSerializer
