# Generated by Django 5.1.4 on 2025-03-05 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0055_appointment_giorno'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabellapazienti',
            name='residence',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
