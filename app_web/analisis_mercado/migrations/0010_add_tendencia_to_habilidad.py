from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('analisis_mercado', '0009_add_demanda_actual_to_habilidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='habilidad',
            name='tendencia',
            field=models.FloatField(default=0.0),
        ),
    ] 