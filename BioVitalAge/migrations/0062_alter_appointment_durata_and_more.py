# Generated by Django 5.1.4 on 2025-03-12 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0061_alter_appointment_tipologia_visita'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='durata',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='voce_prezzario',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
