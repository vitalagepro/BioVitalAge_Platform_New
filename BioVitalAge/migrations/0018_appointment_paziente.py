# Generated by Django 5.1.4 on 2025-05-08 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0017_visite'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='paziente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BioVitalAge.tabellapazienti'),
        ),
    ]
