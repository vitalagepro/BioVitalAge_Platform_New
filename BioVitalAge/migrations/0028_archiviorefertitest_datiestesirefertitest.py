# Generated by Django 5.1.4 on 2025-01-27 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0027_tabellapazienti_associate_staff_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivioRefertiTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_referto', models.DateField(auto_now_add=True)),
                ('data_ora_creazione', models.DateTimeField(auto_now_add=True, null=True)),
                ('punteggio', models.TextField(blank=True, null=True)),
                ('documento', models.FileField(blank=True, null=True, upload_to='referti/')),
                ('paziente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referti_test', to='BioVitalAge.tabellapazienti')),
            ],
        ),
        migrations.CreateModel(
            name='DatiEstesiRefertiTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SiIm', models.IntegerField(blank=True, null=True)),
                ('Lymph', models.FloatField(blank=True, null=True)),
                ('Lymph_el', models.FloatField(blank=True, null=True)),
                ('wbc', models.FloatField(blank=True, null=True)),
                ('Proteins_c', models.FloatField(blank=True, null=True)),
                ('Inter_6', models.FloatField(blank=True, null=True)),
                ('Tnf', models.FloatField(blank=True, null=True)),
                ('Mono', models.FloatField(blank=True, null=True)),
                ('Mono_el', models.FloatField(blank=True, null=True)),
                ('Fss', models.FloatField(blank=True, null=True)),
                ('CirPolp', models.FloatField(blank=True, null=True)),
                ('WHip_ratio', models.FloatField(blank=True, null=True)),
                ('WH_ratio', models.FloatField(blank=True, null=True)),
                ('Glic', models.FloatField(blank=True, null=True)),
                ('Emog', models.FloatField(blank=True, null=True)),
                ('Insu', models.FloatField(blank=True, null=True)),
                ('Pept_c', models.FloatField(blank=True, null=True)),
                ('Col_tot', models.FloatField(blank=True, null=True)),
                ('Col_ldl', models.FloatField(blank=True, null=True)),
                ('Col_hdl', models.FloatField(blank=True, null=True)),
                ('Trigl', models.FloatField(blank=True, null=True)),
                ('albumina', models.FloatField(blank=True, null=True)),
                ('clearance_urea', models.FloatField(blank=True, null=True)),
                ('igf_1', models.FloatField(blank=True, null=True)),
                ('sarc_f', models.IntegerField(blank=True, null=True)),
                ('hgs_test', models.IntegerField(blank=True, null=True)),
                ('sppb', models.IntegerField(blank=True, null=True)),
                ('referto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dati_estesi_test', to='BioVitalAge.archiviorefertitest')),
            ],
        ),
    ]
