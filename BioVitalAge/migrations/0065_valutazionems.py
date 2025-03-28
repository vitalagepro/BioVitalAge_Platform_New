# Generated by Django 5.1.4 on 2025-03-26 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioVitalAge', '0064_resilienza'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValutazioneMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequenza_a_f', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo_a_f', models.CharField(blank=True, max_length=100, null=True)),
                ('stile_vita', models.CharField(blank=True, max_length=100, null=True)),
                ('terapie_inf', models.CharField(blank=True, max_length=255, null=True)),
                ('diagnosi_t', models.CharField(blank=True, max_length=255, null=True)),
                ('sintomi_t', models.TextField(blank=True, null=True)),
                ('palpazione', models.CharField(blank=True, max_length=255, null=True)),
                ('osservazione', models.CharField(blank=True, max_length=255, null=True)),
                ('m_attiva', models.CharField(blank=True, max_length=255, null=True)),
                ('m_passiva', models.CharField(blank=True, max_length=255, null=True)),
                ('dolorabilità', models.CharField(blank=True, max_length=255, null=True)),
                ('scala_v_a', models.CharField(blank=True, max_length=50, null=True)),
                ('mo_attivo', models.CharField(blank=True, max_length=255, null=True)),
                ('mo_a_limitazioni', models.CharField(blank=True, max_length=255, null=True)),
                ('mo_passivo', models.CharField(blank=True, max_length=255, null=True)),
                ('mo_p_limitazioni', models.CharField(blank=True, max_length=255, null=True)),
                ('comparazioni_m', models.TextField(blank=True, null=True)),
                ('circ_polp', models.CharField(blank=True, max_length=50, null=True)),
                ('tono_m', models.CharField(blank=True, max_length=50, null=True)),
                ('scala_ashworth', models.CharField(blank=True, max_length=100, null=True)),
                ('v_frontale', models.CharField(blank=True, max_length=255, null=True)),
                ('v_laterale', models.CharField(blank=True, max_length=255, null=True)),
                ('p_testa', models.CharField(blank=True, max_length=100, null=True)),
                ('spalle', models.CharField(blank=True, max_length=100, null=True)),
                ('ombelico', models.CharField(blank=True, max_length=100, null=True)),
                ('a_inferiori', models.CharField(blank=True, max_length=100, null=True)),
                ('piedi', models.CharField(blank=True, max_length=100, null=True)),
                ('colonna_v', models.CharField(blank=True, max_length=100, null=True)),
                ('curvatura_c', models.CharField(blank=True, max_length=100, null=True)),
                ('curvatura_d', models.CharField(blank=True, max_length=100, null=True)),
                ('curvatura_l', models.CharField(blank=True, max_length=100, null=True)),
                ('posizione_b', models.CharField(blank=True, max_length=100, null=True)),
                ('equilibrio_s', models.CharField(blank=True, max_length=100, null=True)),
                ('equilibrio_d', models.CharField(blank=True, max_length=100, null=True)),
                ('p_dolenti', models.CharField(blank=True, max_length=255, null=True)),
                ('gravita_disfunzione_posturale', models.CharField(blank=True, max_length=100, null=True)),
                ('rischio_infortuni', models.CharField(blank=True, max_length=100, null=True)),
                ('suggerimenti', models.CharField(blank=True, max_length=255, null=True)),
                ('considerazioni_finali', models.CharField(blank=True, max_length=255, null=True)),
                ('paziente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valutazioneMS', to='BioVitalAge.tabellapazienti')),
            ],
        ),
    ]
