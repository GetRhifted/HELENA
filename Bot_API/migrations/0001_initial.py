# Generated by Django 4.2.3 on 2023-07-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recetas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha', models.DateTimeField()),
                ('Titulo', models.CharField(max_length=100)),
                ('Autor', models.CharField(max_length=100)),
                ('Ingredientes', models.TextField()),
                ('Preparacion', models.TextField()),
            ],
        ),
    ]
