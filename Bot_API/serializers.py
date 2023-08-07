from rest_framework import serializers
from .models import Recetas, Predicciones

class RecetasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recetas
        fields = ('Fecha', 'Titulo', 'Autor', 'Ingredientes', 'Preparacion', 'url')

class PrediccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predicciones
        fields = ('Titulo', 'Prediccion', 'url')
        