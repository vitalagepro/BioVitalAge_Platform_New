# Generated by Django 5.1.5 on 2025-02-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0030_merge_20250131_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabellapazienti',
            name='heart_rate',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tabellapazienti',
            name='pressure',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
