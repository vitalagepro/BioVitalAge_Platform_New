# Generated by Django 5.1.4 on 2025-02-11 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0041_alter_tabellapazienti_alcol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabellapazienti',
            name='smoke',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
