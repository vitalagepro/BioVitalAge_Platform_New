# Generated by Django 5.1.4 on 2025-02-11 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0040_alter_tabellapazienti_alcol_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabellapazienti',
            name='alcol',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
