from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('analisis_mercado', '0007_alter_ofertaempleo_unique_together_ofertaempleo_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='habilidad',
            name='categoria',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ] 