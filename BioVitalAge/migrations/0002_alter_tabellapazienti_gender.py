# Generated by Django 5.1.4 on 2025-04-10 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabellapazienti',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=20, null=True),
        ),
    ]
