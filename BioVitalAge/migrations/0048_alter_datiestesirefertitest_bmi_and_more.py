# Generated by Django 5.1.4 on 2025-02-17 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0047_datiestesirefertitest_bmi_datiestesirefertitest_cdp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datiestesirefertitest',
            name='BMI',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datiestesirefertitest',
            name='CDP',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datiestesirefertitest',
            name='WHR',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
