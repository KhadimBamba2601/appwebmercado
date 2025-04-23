from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('analisis_mercado', '0008_add_categoria_to_habilidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='habilidad',
            name='demanda_actual',
            field=models.IntegerField(default=0),
        ),
    ] 