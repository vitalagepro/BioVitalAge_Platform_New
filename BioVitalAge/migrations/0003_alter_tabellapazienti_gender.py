# Generated by Django 5.1.4 on 2025-04-10 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0002_alter_tabellapazienti_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabellapazienti',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=200, null=True),
        ),
    ]
