# Generated by Django 5.1.4 on 2025-04-02 09:36

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivioReferti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_referto', models.DateField(auto_now_add=True)),
                ('data_ora_creazione', models.DateTimeField(auto_now_add=True, null=True)),
                ('descrizione', models.TextField(blank=True, null=True)),
                ('documento', models.FileField(blank=True, null=True, upload_to='referti/')),
            ],
        ),
        migrations.CreateModel(
            name='ArchivioRefertiTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_referto', models.DateField(auto_now_add=True)),
                ('data_ora_creazione', models.DateTimeField(auto_now_add=True, null=True)),
                ('punteggio', models.TextField(blank=True, null=True)),
                ('documento', models.FileField(blank=True, null=True, upload_to='referti/')),
            ],
        ),
        migrations.CreateModel(
            name='ElencoVisitePaziente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_visita', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TabellaPazienti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codice_fiscale', models.CharField(blank=True, max_length=16, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('surname', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('cap', models.CharField(blank=True, max_length=5, null=True)),
                ('residence', models.CharField(blank=True, max_length=100, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('chronological_age', models.IntegerField(blank=True, null=True)),
                ('heart_rate', models.CharField(blank=True, max_length=100, null=True)),
                ('associate_staff', models.CharField(blank=True, max_length=100, null=True)),
                ('lastVisit', models.DateField(blank=True, null=True)),
                ('upcomingVisit', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('professione', models.CharField(blank=True, max_length=100, null=True)),
                ('pensionato', models.CharField(blank=True, max_length=100, null=True)),
                ('menarca', models.CharField(blank=True, max_length=100, null=True)),
                ('ciclo', models.CharField(blank=True, max_length=100, null=True)),
                ('sintomi', models.CharField(blank=True, max_length=100, null=True)),
                ('esordio', models.CharField(blank=True, max_length=100, null=True)),
                ('parto', models.CharField(blank=True, max_length=100, null=True)),
                ('post_parto', models.CharField(blank=True, max_length=100, null=True)),
                ('aborto', models.CharField(blank=True, max_length=100, null=True)),
                ('alcol', models.CharField(blank=True, max_length=255, null=True)),
                ('alcol_type', models.CharField(blank=True, max_length=255, null=True)),
                ('data_alcol', models.DateField(blank=True, null=True)),
                ('alcol_frequency', models.CharField(blank=True, max_length=255, null=True)),
                ('smoke', models.CharField(blank=True, max_length=255, null=True)),
                ('smoke_frequency', models.CharField(blank=True, max_length=100, null=True)),
                ('reduced_intake', models.CharField(blank=True, max_length=100, null=True)),
                ('sport', models.CharField(blank=True, default=False, max_length=100, null=True)),
                ('sport_livello', models.CharField(blank=True, max_length=100, null=True)),
                ('sport_frequency', models.CharField(blank=True, max_length=100, null=True)),
                ('attivita_sedentaria', models.CharField(blank=True, default=False, max_length=100, null=True)),
                ('livello_sedentarieta', models.CharField(blank=True, max_length=100, null=True)),
                ('sedentarieta_nota', models.TextField(blank=True, null=True)),
                ('m_cardiache', models.CharField(blank=True, max_length=100, null=True)),
                ('diabete_m', models.CharField(blank=True, max_length=100, null=True)),
                ('obesita', models.CharField(blank=True, max_length=100, null=True)),
                ('epilessia', models.CharField(blank=True, max_length=100, null=True)),
                ('ipertensione', models.CharField(blank=True, max_length=100, null=True)),
                ('m_tiroidee', models.CharField(blank=True, max_length=100, null=True)),
                ('m_polmonari', models.CharField(blank=True, max_length=100, null=True)),
                ('tumori', models.CharField(blank=True, max_length=100, null=True)),
                ('allergie', models.CharField(blank=True, max_length=100, null=True)),
                ('m_psichiatriche', models.CharField(blank=True, max_length=100, null=True)),
                ('patologie', models.CharField(blank=True, max_length=100, null=True)),
                ('p_p_altro', models.CharField(blank=True, max_length=100, null=True)),
                ('t_farmaco', models.CharField(blank=True, max_length=100, null=True)),
                ('t_dosaggio', models.CharField(blank=True, max_length=100, null=True)),
                ('t_durata', models.CharField(blank=True, max_length=100, null=True)),
                ('p_cardiovascolari', models.CharField(blank=True, max_length=100, null=True)),
                ('m_metabolica', models.CharField(blank=True, max_length=100, null=True)),
                ('p_respiratori_cronici', models.CharField(blank=True, max_length=100, null=True)),
                ('m_neurologica', models.CharField(blank=True, max_length=100, null=True)),
                ('m_endocrina', models.CharField(blank=True, max_length=100, null=True)),
                ('m_autoimmune', models.CharField(blank=True, max_length=100, null=True)),
                ('p_epatici', models.CharField(blank=True, max_length=100, null=True)),
                ('m_renale', models.CharField(blank=True, max_length=100, null=True)),
                ('d_gastrointestinali', models.CharField(blank=True, max_length=100, null=True)),
                ('eloquio', models.CharField(blank=True, max_length=100, null=True)),
                ('s_nutrizionale', models.CharField(blank=True, max_length=100, null=True)),
                ('a_genarale', models.CharField(blank=True, max_length=100, null=True)),
                ('psiche', models.CharField(blank=True, max_length=100, null=True)),
                ('r_ambiente', models.CharField(blank=True, max_length=100, null=True)),
                ('s_emotivo', models.CharField(blank=True, max_length=100, null=True)),
                ('costituzione', models.CharField(blank=True, max_length=100, null=True)),
                ('statura', models.CharField(blank=True, max_length=100, null=True)),
                ('blood_group', models.CharField(blank=True, max_length=3, null=True)),
                ('rh_factor', models.CharField(blank=True, max_length=3, null=True)),
                ('pressure_min', models.CharField(blank=True, max_length=100, null=True)),
                ('pressure_max', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UtentiRegistratiCredenziali',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cognome', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=24, null=True)),
                ('cookie', models.CharField(max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DatiEstesiReferti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_roms', models.FloatField(blank=True, null=True)),
                ('osi', models.FloatField(blank=True, null=True)),
                ('pat', models.FloatField(blank=True, null=True)),
                ('my_acid', models.FloatField(blank=True, null=True)),
                ('p_acid', models.FloatField(blank=True, null=True)),
                ('st_acid', models.FloatField(blank=True, null=True)),
                ('ar_acid', models.FloatField(blank=True, null=True)),
                ('beenic_acid', models.FloatField(blank=True, null=True)),
                ('pal_acid', models.FloatField(blank=True, null=True)),
                ('ol_acid', models.FloatField(blank=True, null=True)),
                ('ner_acid', models.FloatField(blank=True, null=True)),
                ('a_linoleic_acid', models.FloatField(blank=True, null=True)),
                ('eico_acid', models.FloatField(blank=True, null=True)),
                ('doco_acid', models.FloatField(blank=True, null=True)),
                ('lin_acid', models.FloatField(blank=True, null=True)),
                ('gamma_lin_acid', models.FloatField(blank=True, null=True)),
                ('dih_gamma_lin_acid', models.FloatField(blank=True, null=True)),
                ('arachidonic_acid', models.FloatField(blank=True, null=True)),
                ('sa_un_fatty_acid', models.FloatField(blank=True, null=True)),
                ('o3o6_fatty_acid_quotient', models.FloatField(blank=True, null=True)),
                ('aa_epa', models.FloatField(blank=True, null=True)),
                ('o3_index', models.FloatField(blank=True, null=True)),
                ('wbc', models.FloatField(blank=True, null=True)),
                ('baso', models.FloatField(blank=True, null=True)),
                ('eosi', models.FloatField(blank=True, null=True)),
                ('lymph', models.FloatField(blank=True, null=True)),
                ('mono', models.FloatField(blank=True, null=True)),
                ('neut', models.FloatField(blank=True, null=True)),
                ('neut_ul', models.FloatField(blank=True, null=True)),
                ('lymph_ul', models.FloatField(blank=True, null=True)),
                ('mono_ul', models.FloatField(blank=True, null=True)),
                ('eosi_ul', models.FloatField(blank=True, null=True)),
                ('baso_ul', models.FloatField(blank=True, null=True)),
                ('mch', models.FloatField(blank=True, null=True)),
                ('mchc', models.FloatField(blank=True, null=True)),
                ('mcv', models.FloatField(blank=True, null=True)),
                ('rdwsd', models.FloatField(blank=True, null=True)),
                ('rdwcv', models.FloatField(blank=True, null=True)),
                ('hct_m', models.FloatField(blank=True, null=True)),
                ('hct_w', models.FloatField(blank=True, null=True)),
                ('hgb_m', models.FloatField(blank=True, null=True)),
                ('hgb_w', models.FloatField(blank=True, null=True)),
                ('rbc_m', models.FloatField(blank=True, null=True)),
                ('rbc_w', models.FloatField(blank=True, null=True)),
                ('azotemia', models.FloatField(blank=True, null=True)),
                ('uric_acid', models.FloatField(blank=True, null=True)),
                ('creatinine_m', models.FloatField(blank=True, null=True)),
                ('creatinine_w', models.FloatField(blank=True, null=True)),
                ('uricemy_m', models.FloatField(blank=True, null=True)),
                ('uricemy_w', models.FloatField(blank=True, null=True)),
                ('cistatine_c', models.FloatField(blank=True, null=True)),
                ('plt', models.FloatField(blank=True, null=True)),
                ('mpv', models.FloatField(blank=True, null=True)),
                ('plcr', models.FloatField(blank=True, null=True)),
                ('pct', models.FloatField(blank=True, null=True)),
                ('pdw', models.FloatField(blank=True, null=True)),
                ('d_dimero', models.FloatField(blank=True, null=True)),
                ('pai_1', models.FloatField(blank=True, null=True)),
                ('tot_chol', models.FloatField(blank=True, null=True)),
                ('ldl_chol', models.FloatField(blank=True, null=True)),
                ('hdl_chol_m', models.FloatField(blank=True, null=True)),
                ('hdl_chol_w', models.FloatField(blank=True, null=True)),
                ('trigl', models.FloatField(blank=True, null=True)),
                ('na', models.FloatField(blank=True, null=True)),
                ('k', models.FloatField(blank=True, null=True)),
                ('mg', models.FloatField(blank=True, null=True)),
                ('ci', models.FloatField(blank=True, null=True)),
                ('ca', models.FloatField(blank=True, null=True)),
                ('p', models.FloatField(blank=True, null=True)),
                ('dhea_m', models.FloatField(blank=True, null=True)),
                ('dhea_w', models.FloatField(blank=True, null=True)),
                ('testo_m', models.FloatField(blank=True, null=True)),
                ('testo_w', models.FloatField(blank=True, null=True)),
                ('tsh', models.FloatField(blank=True, null=True)),
                ('ft3', models.FloatField(blank=True, null=True)),
                ('ft4', models.FloatField(blank=True, null=True)),
                ('beta_es_m', models.FloatField(blank=True, null=True)),
                ('beta_es_w', models.FloatField(blank=True, null=True)),
                ('prog_m', models.FloatField(blank=True, null=True)),
                ('prog_w', models.FloatField(blank=True, null=True)),
                ('fe', models.FloatField(blank=True, null=True)),
                ('transferrin', models.FloatField(blank=True, null=True)),
                ('ferritin_m', models.FloatField(blank=True, null=True)),
                ('ferritin_w', models.FloatField(blank=True, null=True)),
                ('glicemy', models.FloatField(blank=True, null=True)),
                ('insulin', models.FloatField(blank=True, null=True)),
                ('homa', models.FloatField(blank=True, null=True)),
                ('ir', models.FloatField(blank=True, null=True)),
                ('albuminemia', models.FloatField(blank=True, null=True)),
                ('tot_prot', models.FloatField(blank=True, null=True)),
                ('tot_prot_ele', models.FloatField(blank=True, null=True)),
                ('albumin_ele', models.FloatField(blank=True, null=True)),
                ('a_1', models.FloatField(blank=True, null=True)),
                ('a_2', models.FloatField(blank=True, null=True)),
                ('b_1', models.FloatField(blank=True, null=True)),
                ('b_2', models.FloatField(blank=True, null=True)),
                ('gamma', models.FloatField(blank=True, null=True)),
                ('albumin_dI', models.FloatField(blank=True, null=True)),
                ('a_1_dI', models.FloatField(blank=True, null=True)),
                ('a_2_dI', models.FloatField(blank=True, null=True)),
                ('b_1_dI', models.FloatField(blank=True, null=True)),
                ('b_2_dI', models.FloatField(blank=True, null=True)),
                ('gamma_dI', models.FloatField(blank=True, null=True)),
                ('ag_rap', models.FloatField(blank=True, null=True)),
                ('got_m', models.FloatField(blank=True, null=True)),
                ('got_w', models.FloatField(blank=True, null=True)),
                ('gpt_m', models.FloatField(blank=True, null=True)),
                ('gpt_w', models.FloatField(blank=True, null=True)),
                ('g_gt_m', models.FloatField(blank=True, null=True)),
                ('g_gt_w', models.FloatField(blank=True, null=True)),
                ('a_photo_m', models.FloatField(blank=True, null=True)),
                ('a_photo_w', models.FloatField(blank=True, null=True)),
                ('tot_bili', models.FloatField(blank=True, null=True)),
                ('direct_bili', models.FloatField(blank=True, null=True)),
                ('indirect_bili', models.FloatField(blank=True, null=True)),
                ('ves', models.FloatField(blank=True, null=True)),
                ('pcr_c', models.FloatField(blank=True, null=True)),
                ('tnf_a', models.FloatField(blank=True, null=True)),
                ('inter_6', models.FloatField(blank=True, null=True)),
                ('inter_10', models.FloatField(blank=True, null=True)),
                ('scatolo', models.FloatField(blank=True, null=True)),
                ('indicano', models.FloatField(blank=True, null=True)),
                ('s_weight', models.FloatField(blank=True, null=True)),
                ('ph', models.FloatField(blank=True, null=True)),
                ('proteins_ex', models.FloatField(blank=True, null=True)),
                ('blood_ex', models.FloatField(blank=True, null=True)),
                ('ketones', models.FloatField(blank=True, null=True)),
                ('uro', models.FloatField(blank=True, null=True)),
                ('bilirubin_ex', models.FloatField(blank=True, null=True)),
                ('leuc', models.FloatField(blank=True, null=True)),
                ('glucose', models.FloatField(blank=True, null=True)),
                ('shbg_m', models.FloatField(blank=True, null=True)),
                ('shbg_w', models.FloatField(blank=True, null=True)),
                ('nt_pro', models.FloatField(blank=True, null=True)),
                ('v_b12', models.FloatField(blank=True, null=True)),
                ('v_d', models.FloatField(blank=True, null=True)),
                ('ves2', models.FloatField(blank=True, null=True)),
                ('telotest', models.FloatField(blank=True, null=True)),
                ('biological_age', models.IntegerField(blank=True, null=True)),
                ('referto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dati_estesi', to='BioVitalAge.archivioreferti')),
            ],
        ),
        migrations.CreateModel(
            name='DatiEstesiRefertiTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MMSE', models.IntegerField(blank=True, null=True)),
                ('GDS', models.IntegerField(blank=True, null=True)),
                ('LOC', models.IntegerField(blank=True, null=True)),
                ('Vista', models.IntegerField(blank=True, null=True)),
                ('Udito', models.IntegerField(blank=True, null=True)),
                ('HGS', models.TextField(blank=True, null=True)),
                ('PFT', models.IntegerField(blank=True, null=True)),
                ('ISQ', models.IntegerField(blank=True, null=True)),
                ('BMI', models.FloatField(blank=True, null=True)),
                ('CDP', models.FloatField(blank=True, null=True)),
                ('WHR', models.FloatField(blank=True, null=True)),
                ('WHR_Ratio', models.TextField(blank=True, null=True)),
                ('CST', models.FloatField(blank=True, null=True)),
                ('GS', models.FloatField(blank=True, null=True)),
                ('PPT', models.IntegerField(blank=True, null=True)),
                ('SARC_F', models.IntegerField(blank=True, null=True)),
                ('FSS', models.IntegerField(blank=True, null=True)),
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
                ('Inter_6', models.FloatField(blank=True, null=True)),
                ('Tnf', models.FloatField(blank=True, null=True)),
                ('Mono', models.FloatField(blank=True, null=True)),
                ('Mono_el', models.FloatField(blank=True, null=True)),
                ('Proteins_c', models.FloatField(blank=True, null=True)),
                ('wbc', models.FloatField(blank=True, null=True)),
                ('Lymph', models.FloatField(blank=True, null=True)),
                ('Lymph_el', models.FloatField(blank=True, null=True)),
                ('referto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dati_estesi_test', to='BioVitalAge.archiviorefertitest')),
            ],
        ),
        migrations.CreateModel(
            name='EsameVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codice_esame', models.CharField(max_length=50)),
                ('visita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='esami', to='BioVitalAge.elencovisitepaziente')),
            ],
        ),
        migrations.CreateModel(
            name='Resilienza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hrv', models.FloatField(blank=True, null=True)),
                ('cortisolo', models.FloatField(blank=True, null=True)),
                ('ros', models.FloatField(blank=True, null=True)),
                ('osi', models.FloatField(blank=True, null=True)),
                ('droms', models.FloatField(blank=True, null=True)),
                ('pcr', models.FloatField(blank=True, null=True)),
                ('nlr', models.FloatField(blank=True, null=True)),
                ('homa', models.FloatField(blank=True, null=True)),
                ('ir', models.FloatField(blank=True, null=True)),
                ('omega_3', models.FloatField(blank=True, null=True)),
                ('vo2max', models.FloatField(blank=True, null=True)),
                ('risultato', models.FloatField(blank=True, null=True)),
                ('paziente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resilienza', to='BioVitalAge.tabellapazienti')),
            ],
        ),
        migrations.AddField(
            model_name='elencovisitepaziente',
            name='paziente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visite', to='BioVitalAge.tabellapazienti'),
        ),
        migrations.AddField(
            model_name='archiviorefertitest',
            name='paziente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referti_test', to='BioVitalAge.tabellapazienti'),
        ),
        migrations.AddField(
            model_name='archivioreferti',
            name='paziente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referti', to='BioVitalAge.tabellapazienti'),
        ),
        migrations.AddField(
            model_name='tabellapazienti',
            name='dottore',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pazienti', to='BioVitalAge.utentiregistraticredenziali'),
        ),
        migrations.CreateModel(
            name='RefertiEtaMetabolica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_referto', models.DateTimeField(default=django.utils.timezone.now)),
                ('bmi', models.CharField(blank=True, max_length=100, null=True)),
                ('grasso', models.CharField(blank=True, max_length=100, null=True)),
                ('acqua', models.CharField(blank=True, max_length=100, null=True)),
                ('massa_muscolare', models.CharField(blank=True, max_length=100, null=True)),
                ('bmr', models.CharField(blank=True, max_length=100, null=True)),
                ('whr', models.CharField(blank=True, max_length=100, null=True)),
                ('whtr', models.CharField(blank=True, max_length=100, null=True)),
                ('glicemia', models.CharField(blank=True, max_length=100, null=True)),
                ('ogtt', models.CharField(blank=True, max_length=100, null=True)),
                ('emoglobina_g', models.CharField(blank=True, max_length=100, null=True)),
                ('insulina_d', models.CharField(blank=True, max_length=100, null=True)),
                ('curva_i', models.CharField(blank=True, max_length=100, null=True)),
                ('homa_ir', models.CharField(blank=True, max_length=100, null=True)),
                ('tyg', models.CharField(blank=True, max_length=100, null=True)),
                ('c_tot', models.CharField(blank=True, max_length=100, null=True)),
                ('hdl', models.CharField(blank=True, max_length=100, null=True)),
                ('ldl', models.CharField(blank=True, max_length=100, null=True)),
                ('trigliceridi', models.CharField(blank=True, max_length=100, null=True)),
                ('ast', models.CharField(blank=True, max_length=100, null=True)),
                ('alt', models.CharField(blank=True, max_length=100, null=True)),
                ('ggt', models.CharField(blank=True, max_length=100, null=True)),
                ('bili_t', models.CharField(blank=True, max_length=100, null=True)),
                ('pcr', models.CharField(blank=True, max_length=100, null=True)),
                ('hgs', models.CharField(blank=True, max_length=100, null=True)),
                ('sii', models.CharField(blank=True, max_length=100, null=True)),
                ('c_plasmatico', models.CharField(blank=True, max_length=100, null=True)),
                ('massa_ossea', models.CharField(blank=True, max_length=100, null=True)),
                ('eta_metabolica', models.CharField(blank=True, max_length=100, null=True)),
                ('grasso_viscerale', models.CharField(blank=True, max_length=100, null=True)),
                ('p_fisico', models.CharField(blank=True, max_length=100, null=True)),
                ('storico_punteggi', models.JSONField(blank=True, default=list)),
                ('height', models.CharField(blank=True, max_length=255, null=True)),
                ('weight', models.CharField(blank=True, max_length=255, null=True)),
                ('bmi_detection_date', models.DateField(blank=True, null=True)),
                ('girth_value', models.CharField(blank=True, max_length=255, null=True)),
                ('girth_notes', models.TextField(blank=True, null=True)),
                ('girth_date', models.DateField(blank=True, null=True)),
                ('paziente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referti_eta_metabolica', to='BioVitalAge.tabellapazienti')),
                ('dottore', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referti_eta_metabolica', to='BioVitalAge.utentiregistraticredenziali')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cognome_paziente', models.CharField(blank=True, max_length=255, null=True)),
                ('nome_paziente', models.CharField(blank=True, max_length=255, null=True)),
                ('tipologia_visita', models.CharField(blank=True, choices=[('Fisioterapia Sportiva', 'Fisioterapia Sportiva'), ('Fisioterapia e Riabilitazione', 'Fisioterapia e Riabilitazione'), ('Fisioestetica', 'Fisioestetica')], max_length=100, null=True)),
                ('data', models.DateField(default=datetime.datetime.now)),
                ('giorno', models.CharField(blank=True, max_length=255, null=True)),
                ('orario', models.TimeField()),
                ('durata', models.CharField(blank=True, max_length=255, null=True)),
                ('voce_prezzario', models.CharField(blank=True, max_length=255, null=True)),
                ('numero_studio', models.CharField(blank=True, choices=[('Studio 1', 'Studio 1'), ('Studio 2', 'Studio 2'), ('Studio 3', 'Studio 3')], max_length=100, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('confermato', models.BooleanField(default=False)),
                ('dottore', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BioVitalAge.utentiregistraticredenziali')),
            ],
        ),
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
        migrations.AddConstraint(
            model_name='tabellapazienti',
            constraint=models.UniqueConstraint(fields=('dottore', 'codice_fiscale'), name='unique_paziente_per_dottore'),
        ),
    ]
