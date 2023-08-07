from django.db import models

class Recetas(models.Model):
    Fecha = models.DateTimeField()
    Titulo = models.CharField(max_length=200)
    Autor = models.CharField(max_length=100)
    Ingredientes = models.TextField()
    Preparacion = models.TextField()
    url = models.URLField(null=True, blank=True)

class Predicciones(models.Model):
    Titulo = models.CharField(max_length=200)
    Prediccion = models.TextField()
    url = models.URLField(null=True, blank=True)