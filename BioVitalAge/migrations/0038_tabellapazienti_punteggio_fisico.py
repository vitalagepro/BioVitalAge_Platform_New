# Generated by Django 5.1.5 on 2025-02-10 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0037_tabellapazienti_acqua_tabellapazienti_bmr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabellapazienti',
            name='punteggio_fisico',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
