# Generated by Django 5.1.4 on 2025-04-04 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utentiregistraticredenziali',
            name='google_access_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='utentiregistraticredenziali',
            name='google_refresh_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='utentiregistraticredenziali',
            name='google_token_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
