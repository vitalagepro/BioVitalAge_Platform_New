# Generated by Django 5.1.4 on 2025-01-10 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0021_datiestesireferti_aa_epa_datiestesireferti_o3_index_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datiestesireferti',
            old_name='a_photo',
            new_name='g_gt_m',
        ),
        migrations.RenameField(
            model_name='datiestesireferti',
            old_name='direct_bili',
            new_name='g_gt_w',
        ),
        migrations.RemoveField(
            model_name='datiestesireferti',
            name='g_gt',
        ),
        migrations.RemoveField(
            model_name='datiestesireferti',
            name='got',
        ),
        migrations.RemoveField(
            model_name='datiestesireferti',
            name='gpt',
        ),
        migrations.RemoveField(
            model_name='datiestesireferti',
            name='idirect_bili',
        ),
        migrations.RemoveField(
            model_name='datiestesireferti',
            name='tot_bili',
        ),
    ]
