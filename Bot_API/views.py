from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RecetasSerializer

@api_view(['POST'])
def guardar_recetas(request):
    if request.method == 'POST':
        # Obtener los datos de las recetas enviados por el scraper
        data = request.data

        # Validar y guardar los datos utilizando el serializador
        serializer = RecetasSerializer(data=data)
        if serializer.is_valid():
            print("Datos válidos:", serializer.validated_data)
            serializer.save()
            return Response({'message': 'Recetas guardadas exitosamente.'}, status=201)
        else:
            print("Errores de validación:", serializer.errors)
            return Response(serializer.errors, status=400)




