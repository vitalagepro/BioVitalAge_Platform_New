from django.db import models

# Tabella dottori con credenziali
class UtentiRegistratiCredenziali(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=24, null=True)

    def __str__(self):
        return f'{self.nome} {self.cognome}'


# Tabella pazienti associata a ogni dottore
class TabellaPazienti(models.Model):
    dottore = models.ForeignKey(
        UtentiRegistratiCredenziali, 
        on_delete=models.CASCADE, 
        related_name='pazienti',
        null=True
    )
    # Dati personali
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Male'), ('F', 'Female')])
    cap = models.CharField(max_length=5, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True, unique=True)
    chronological_age = models.IntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=3, null=True, blank=True)
    rh_factor = models.CharField(max_length=3, null=True, blank=True)
    pressure = models.CharField(max_length=100, null=True, blank=True)
    heart_rate = models.CharField(max_length=100, null=True, blank=True)
    associate_staff = models.CharField(max_length=100, null=True, blank=True)
    lastVisit = models.DateField(null=True, blank=True)
    upcomingVisit = models.DateField(null=True, blank=True)


    # Dati antropometrici
    height = models.FloatField(help_text="Height in cm", null=True) 
    weight = models.FloatField(help_text="Weight in kg", null=True) 
    bmi = models.FloatField(help_text="Body Mass Index", null=True) 
    bmi_detection_date = models.DateField( null=True)

    # Circonferenza addominale
    girth_value = models.FloatField(help_text="Girth value in cm", null=True)
    girth_notes = models.TextField(blank=True, null=True)
    girth_date = models.DateField( null=True)

    # Alcol
    alcol = models.BooleanField(default=False, null=True)
    alcol_type = models.CharField(max_length=100, blank=True, null=True)
    data_alcol = models.DateField(blank=True, null=True)
    alcol_frequency = models.CharField(max_length=100, blank=True, null=True)

    # Fumo
    smoke = models.BooleanField(default=False, null=True)
    smoke_frequency = models.CharField(max_length=100, blank=True, null=True)
    reduced_intake = models.CharField(max_length=100, blank=True, null=True)

    # Sport
    sport = models.CharField(default=False, max_length=100, null=True)
    sport_livello = models.CharField(max_length=100, blank=True, null=True)
    sport_frequency = models.CharField(max_length=100, blank=True, null=True)

    # Sedentarietà
    attivita_sedentaria = models.CharField(default=False, max_length=100, null=True)
    livello_sedentarieta = models.CharField(max_length=100, blank=True, null=True)
    sedentarieta_nota = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Paziente: {self.name} {self.surname}"  



# Tabella archivio referti associata ai pazienti
class ArchivioReferti(models.Model):
    paziente = models.ForeignKey(
        TabellaPazienti,
        on_delete=models.CASCADE, 
        related_name='referti'
    )
    data_referto = models.DateField(auto_now_add=True)
    data_ora_creazione = models.DateTimeField(auto_now_add=True, null=True)
    descrizione = models.TextField(null=True, blank=True)
    documento = models.FileField(upload_to='referti/', null=True, blank=True)

    def __str__(self):
        print(f"Referto ID: {self.id} - Paziente: {self.paziente.name} {self.paziente.surname}")
        return f"Referto ID: {self.id} - Paziente: {self.paziente.name} {self.paziente.surname}"


# Nuova tabella per i dati estesi dei referti
class DatiEstesiReferti(models.Model):
    referto = models.OneToOneField(
        ArchivioReferti, 
        on_delete=models.CASCADE, 
        related_name='dati_estesi'
    )

    # Oxidative Stress
    d_roms = models.FloatField(null=True, blank=True)
    osi = models.FloatField(null=True, blank=True)
    pat = models.FloatField(null=True, blank=True)

    # Omega Screening
    my_acid = models.FloatField(null=True, blank=True)  
    p_acid = models.FloatField(null=True, blank=True)  
    st_acid = models.FloatField(null=True, blank=True)  
    ar_acid = models.FloatField(null=True, blank=True)  
    beenic_acid = models.FloatField(null=True, blank=True) 
    pal_acid = models.FloatField(null=True, blank=True) 
    ol_acid = models.FloatField(null=True, blank=True)  
    ner_acid = models.FloatField(null=True, blank=True) 
    a_linoleic_acid = models.FloatField(null=True, blank=True) 
    eico_acid = models.FloatField(null=True, blank=True)  
    doco_acid = models.FloatField(null=True, blank=True)  
    lin_acid = models.FloatField(null=True, blank=True)  
    gamma_lin_acid = models.FloatField(null=True, blank=True)  
    dih_gamma_lin_acid = models.FloatField(null=True, blank=True)  
    arachidonic_acid = models.FloatField(null=True, blank=True)  
    sa_un_fatty_acid = models.FloatField(null=True, blank=True)
    o3o6_fatty_acid_quotient = models.FloatField(null=True, blank=True)  
    aa_epa = models.FloatField(null=True, blank=True)  
    o3_index = models.FloatField(null=True, blank=True)

    # White Blood Cells
    wbc = models.FloatField(null=True, blank=True)
    baso = models.FloatField(null=True, blank=True)
    eosi = models.FloatField(null=True, blank=True)
    lymph = models.FloatField(null=True, blank=True)
    mono = models.FloatField(null=True, blank=True)
    neut = models.FloatField(null=True, blank=True)
    neut_ul = models.FloatField(null=True, blank=True)
    lymph_ul = models.FloatField(null=True, blank=True)
    mono_ul = models.FloatField(null=True, blank=True)
    eosi_ul = models.FloatField(null=True, blank=True)
    baso_ul = models.FloatField(null=True, blank=True)

    # Red Blood Cells
    mch = models.FloatField(null=True, blank=True)
    mchc = models.FloatField(null=True, blank=True)
    mcv = models.FloatField(null=True, blank=True)
    rdwsd = models.FloatField(null=True, blank=True)
    rdwcv = models.FloatField(null=True, blank=True)
    hct_m = models.FloatField(null=True, blank=True)  
    hct_w = models.FloatField(null=True, blank=True) 
    hgb_m = models.FloatField(null=True, blank=True)  
    hgb_w = models.FloatField(null=True, blank=True)  
    rbc_m = models.FloatField(null=True, blank=True)  
    rbc_w = models.FloatField(null=True, blank=True)

    # Renal Functionality
    azotemia = models.FloatField(null=True, blank=True)
    uric_acid = models.FloatField(null=True, blank=True)
    creatinine_m = models.FloatField(null=True, blank=True)  
    creatinine_w = models.FloatField(null=True, blank=True)  
    uricemy_m = models.FloatField(null=True, blank=True)  
    uricemy_w = models.FloatField(null=True, blank=True)  
    cistatine_c = models.FloatField(null=True, blank=True)

    # Clotting Status 
    plt = models.FloatField(null=True, blank=True)
    mpv = models.FloatField(null=True, blank=True)
    plcr = models.FloatField(null=True, blank=True)
    pct = models.FloatField(null=True, blank=True)
    pdw = models.FloatField(null=True, blank=True)
    d_dimero = models.FloatField(null=True, blank=True)
    pai_1 = models.FloatField(null=True, blank=True)

    # Lipid Appearance
    tot_chol = models.FloatField(null=True, blank=True)
    ldl_chol = models.FloatField(null=True, blank=True)
    hdl_chol_m = models.FloatField(null=True, blank=True)  
    hdl_chol_w = models.FloatField(null=True, blank=True)  
    trigl = models.FloatField(null=True, blank=True)

    # Minerals
    na = models.FloatField(null=True, blank=True)
    k = models.FloatField(null=True, blank=True)
    mg = models.FloatField(null=True, blank=True)
    ci = models.FloatField(null=True, blank=True)
    ca = models.FloatField(null=True, blank=True)
    p = models.FloatField(null=True, blank=True)

    # Hormonal Assets
    dhea_m = models.FloatField(null=True, blank=True) 
    dhea_w = models.FloatField(null=True, blank=True)  
    testo_m = models.FloatField(null=True, blank=True) 
    testo_w = models.FloatField(null=True, blank=True)  
    tsh = models.FloatField(null=True, blank=True)  
    ft3 = models.FloatField(null=True, blank=True)  
    ft4 = models.FloatField(null=True, blank=True)  
    beta_es_m = models.FloatField(null=True, blank=True) 
    beta_es_w = models.FloatField(null=True, blank=True)  
    prog_m = models.FloatField(null=True, blank=True)  
    prog_w = models.FloatField(null=True, blank=True)  

    # Martial Trim
    fe = models.FloatField(null=True, blank=True)
    transferrin = models.FloatField(null=True, blank=True)
    ferritin_m = models.FloatField(null=True, blank=True)  
    ferritin_w = models.FloatField(null=True, blank=True)  

    # Diabetological Setup
    glicemy = models.FloatField(null=True, blank=True)
    insulin = models.FloatField(null=True, blank=True)
    homa = models.FloatField(null=True, blank=True)
    ir = models.FloatField(null=True, blank=True)

    # Proteins
    albuminemia = models.FloatField(null=True, blank=True)
    tot_prot = models.FloatField(null=True, blank=True)
    tot_prot_ele = models.FloatField(null=True, blank=True)
    albumin_ele = models.FloatField(null=True, blank=True)
    a_1 = models.FloatField(null=True, blank=True)
    a_2 = models.FloatField(null=True, blank=True)
    b_1 = models.FloatField(null=True, blank=True)
    b_2 = models.FloatField(null=True, blank=True)
    gamma = models.FloatField(null=True, blank=True)
    albumin_dI = models.FloatField(null=True, blank=True)
    a_1_dI = models.FloatField(null=True, blank=True)
    a_2_dI = models.FloatField(null=True, blank=True)
    b_1_dI = models.FloatField(null=True, blank=True)
    b_2_dI = models.FloatField(null=True, blank=True)
    gamma_dI = models.FloatField(null=True, blank=True)
    ag_rap = models.FloatField(null=True, blank=True)
    
    # Liver Functionality
    got_m = models.FloatField(null=True, blank=True)  
    got_w = models.FloatField(null=True, blank=True)  
    gpt_m = models.FloatField(null=True, blank=True)  
    gpt_w = models.FloatField(null=True, blank=True)  
    g_gt_m = models.FloatField(null=True, blank=True)
    g_gt_w = models.FloatField(null=True, blank=True)  
    a_photo_m = models.FloatField(null=True, blank=True)  
    a_photo_w = models.FloatField(null=True, blank=True)
    tot_bili = models.FloatField(null=True, blank=True)  
    direct_bili = models.FloatField(null=True, blank=True)  
    indirect_bili = models.FloatField(null=True, blank=True)

    # Indices of Phlogosis
    ves = models.FloatField(null=True, blank=True)
    pcr_c = models.FloatField(null=True, blank=True)

    #Advance/sasp inflammation
    tnf_a = models.FloatField(null=True, blank=True)  
    inter_6 = models.FloatField(null=True, blank=True)  
    inter_10 = models.FloatField(null=True, blank=True)  

    # Disbiosi Test
    scatolo = models.FloatField(null=True, blank=True) 
    indicano = models.FloatField(null=True, blank=True)  

    # Urinalysis
    s_weight = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    proteins_ex = models.FloatField(null=True, blank=True)
    blood_ex = models.FloatField(null=True, blank=True)
    ketones = models.FloatField(null=True, blank=True)
    uro = models.FloatField(null=True, blank=True)
    bilirubin_ex = models.FloatField(null=True, blank=True)
    leuc = models.FloatField(null=True, blank=True)
    glucose = models.FloatField(null=True, blank=True)  
    
    # Other Exams
    shbg_m = models.FloatField(null=True, blank=True)  
    shbg_w = models.FloatField(null=True, blank=True)  
    nt_pro = models.FloatField(null=True, blank=True)  
    v_b12 = models.FloatField(null=True, blank=True)  
    v_d = models.FloatField(null=True, blank=True)  
    ves2 = models.FloatField(null=True, blank=True) 

    # Telomere Length
    telotest = models.FloatField(null=True, blank=True)  

    # Biological Age
    biological_age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Dati Estesi Referto ID: {self.referto.id}"
    


# Tabella archivio referti Quiz associata ai pazienti
class ArchivioRefertiTest(models.Model):
    paziente = models.ForeignKey(
        TabellaPazienti, 
        on_delete=models.CASCADE, 
        related_name='referti_test'
    )
    data_referto = models.DateField(auto_now_add=True)
    data_ora_creazione = models.DateTimeField(auto_now_add=True, null=True)
    punteggio = models.TextField(null=True, blank=True)
    documento = models.FileField(upload_to='referti/', null=True, blank=True)

    def __str__(self):
        return f"Referto ID: {self.id} - Paziente: {self.paziente.name} {self.paziente.surname}"


# Nuova tabella per i dati estesi dei referti
class DatiEstesiRefertiTest(models.Model):
    referto = models.OneToOneField(
        ArchivioRefertiTest, 
        on_delete=models.CASCADE, 
        related_name='dati_estesi_test'
    )

    SiIm = models.IntegerField(null=True, blank=True)
    Lymph = models.FloatField(null=True, blank=True)
    Lymph_el = models.FloatField(null=True, blank=True)
    wbc = models.FloatField(null=True, blank=True)
    Proteins_c = models.FloatField(null=True, blank=True)

    #BIOMARCATORI CIRCOLANTI DELL'INFIAMMAZIONE
    Inter_6 = models.FloatField(null=True, blank=True)
    Tnf = models.FloatField(null=True, blank=True)
    Mono = models.FloatField(null=True, blank=True)
    Mono_el = models.FloatField(null=True, blank=True)

    #ENERGIA E MTABOLISMO
    Fss = models.FloatField(null=True, blank=True)
    CirPolp = models.FloatField(null=True, blank=True)
    WHip_ratio = models.FloatField(null=True, blank=True)
    WH_ratio = models.FloatField(null=True, blank=True)

    #BIOMARCATORI CIRCOLANTI DEL METABOLISMO
    Glic = models.FloatField(null=True, blank=True)
    Emog = models.FloatField(null=True, blank=True)
    Insu = models.FloatField(null=True, blank=True)
    Pept_c = models.FloatField(null=True, blank=True)
    Col_tot = models.FloatField(null=True, blank=True)
    Col_ldl = models.FloatField(null=True, blank=True)
    Col_hdl = models.FloatField(null=True, blank=True)
    Trigl = models.FloatField(null=True, blank=True)
    albumina = models.FloatField(null=True, blank=True)
    clearance_urea = models.FloatField(null=True, blank=True)
    igf_1 = models.FloatField(null=True, blank=True)
    
    # Funzione Neuromuscolare
    sarc_f = models.IntegerField(null=True, blank=True)
    hgs_test = models.IntegerField(null=True, blank=True)
    
    # Performance Fisica
    sppb = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"Dati Estesi Referto ID: {self.referto.id}"
    




# ELENCO VISITE
class ElencoVisitePaziente(models.Model):
    paziente = models.ForeignKey(
        TabellaPazienti, 
        on_delete=models.CASCADE, 
        related_name='visite'
    )
    data_visita = models.DateField(auto_now_add=True)
    #medico = models.CharField(max_length=100) 
    #motivo_visita = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Visita di - {self.data_visita}"


class EsameVisita(models.Model):
    visita = models.ForeignKey(
        ElencoVisitePaziente, 
        on_delete=models.CASCADE, 
        related_name='esami'
    )
    codice_esame = models.CharField(max_length=50)
    #descrizione = models.CharField(max_length=255)
    #metodica = models.CharField(max_length=100, blank=True, null=True)
    #risultato = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f" Visita {self.visita.id}"
