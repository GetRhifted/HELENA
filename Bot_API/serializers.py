from rest_framework import serializers
from .models import Recetas

class RecetasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recetas
        fields = ('Fecha', 'Titulo', 'Autor', 'Ingredientes', 'Preparacion', 'url')
        