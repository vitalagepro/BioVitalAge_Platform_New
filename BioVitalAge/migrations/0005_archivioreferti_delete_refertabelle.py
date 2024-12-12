# Generated by Django 5.0.3 on 2024-12-12 08:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0004_tabellapazienti'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivioReferti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_referto', models.DateField()),
                ('descrizione', models.TextField(blank=True, null=True)),
                ('documento', models.FileField(blank=True, null=True, upload_to='referti/')),
                ('paziente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referti', to='BioVitalAge.tabellapazienti')),
            ],
        ),
        migrations.DeleteModel(
            name='ReferTabelle',
        ),
    ]
