# Generated by Django 5.1.4 on 2025-02-07 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0032_merge_20250206_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElencoVisitePaziente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_visita', models.DateField()),
                ('paziente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visite', to='BioVitalAge.tabellapazienti')),
            ],
        ),
        migrations.CreateModel(
            name='EsameVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codice_esame', models.CharField(max_length=50)),
                ('descrizione', models.CharField(max_length=255)),
                ('metodica', models.CharField(blank=True, max_length=100, null=True)),
                ('visita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='esami', to='BioVitalAge.elencovisitepaziente')),
            ],
        ),
        migrations.DeleteModel(
            name='PrescrizioniUtenti',
        ),
    ]
