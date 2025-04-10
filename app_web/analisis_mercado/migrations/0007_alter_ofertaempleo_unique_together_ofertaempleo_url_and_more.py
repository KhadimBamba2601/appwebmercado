# Generated by Django 5.1.6 on 2025-04-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analisis_mercado', '0006_alter_ofertaempleo_salario'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ofertaempleo',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='ofertaempleo',
            name='url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='habilidad',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ofertaempleo',
            name='empresa',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='ofertaempleo',
            name='fuente',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ofertaempleo',
            name='salario',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ofertaempleo',
            name='tipo_trabajo',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='ofertaempleo',
            name='ubicacion',
            field=models.CharField(max_length=200),
        ),
    ]
