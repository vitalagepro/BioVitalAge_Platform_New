# Generated by Django 5.1.5 on 2025-01-26 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0025_tabellapazienti_cap_tabellapazienti_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabellapazienti',
            name='blood_group',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
