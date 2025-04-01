from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Tabella dottori con credenziali
class UtentiRegistratiCredenziali(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=24, null=True)
    cookie = models.CharField(max_length=2, null=True)

    def __str__(self):
        return f'{self.nome} {self.cognome}'


# Tabella pazienti associata a ogni dottore
# tabella DATI PAZIENTI associati al dottore
class TabellaPazienti(models.Model):

    dottore = models.ForeignKey(
        UtentiRegistratiCredenziali, 
        on_delete=models.CASCADE, 
        related_name='pazienti',
        null=True
    )

    codice_fiscale = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['dottore', 'codice_fiscale'], name='unique_paziente_per_dottore')
    ]
        
    # DATI PERSONALI
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Male'), ('F', 'Female')])
    cap = models.CharField(max_length=5, null=True, blank=True)
    residence = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    chronological_age = models.IntegerField(null=True, blank=True)
    heart_rate = models.CharField(max_length=100, null=True, blank=True)
    associate_staff = models.CharField(max_length=100, null=True, blank=True)
    lastVisit = models.DateField(null=True, blank=True)
    upcomingVisit = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    # --- DATI BASE ---
    ## DOMINIO OCCUPAZIONE
    professione = models.CharField(max_length=100, null=True, blank=True)
    pensionato = models.CharField(max_length=100, null=True, blank=True)

    ## DOMINIO DONNA
    menarca = models.CharField(max_length=100, null=True, blank=True)
    ciclo = models.CharField(max_length=100, null=True, blank=True)
    sintomi = models.CharField(max_length=100, null=True, blank=True)
    esordio = models.CharField(max_length=100, null=True, blank=True)
    parto = models.CharField(max_length=100, null=True, blank=True)
    post_parto = models.CharField(max_length=100, null=True, blank=True)
    aborto = models.CharField(max_length=100, null=True, blank=True)
    
    ## DOMINIO STILE DI VITA
    ### Alcol
    alcol = models.CharField(max_length=255, null=True, blank=True)
    alcol_type = models.CharField(max_length=255, null=True, blank=True)
    data_alcol = models.DateField(null=True, blank=True)
    alcol_frequency = models.CharField(max_length=255, null=True, blank=True)

    ### Fumo
    smoke = models.CharField(max_length=255, null=True, blank=True)
    smoke_frequency = models.CharField(max_length=100, blank=True, null=True)
    reduced_intake = models.CharField(max_length=100, blank=True, null=True)

    ### Sport
    sport = models.CharField(default=False, max_length=100, null=True, blank=True)
    sport_livello = models.CharField(max_length=100, blank=True, null=True)
    sport_frequency = models.CharField(max_length=100, blank=True, null=True)

    ### SedentarietÃ 
    attivita_sedentaria = models.CharField(default=False, max_length=100, null=True, blank=True)
    livello_sedentarieta = models.CharField(max_length=100, blank=True, null=True)
    sedentarieta_nota = models.TextField(blank=True, null=True)

    ## DOMINIO ANAMNESI FAMILIARE
    m_cardiache = models.CharField(max_length=100, null=True, blank=True)
    diabete_m = models.CharField(max_length=100, null=True, blank=True)
    obesita = models.CharField(max_length=100, null=True, blank=True)
    epilessia = models.CharField(max_length=100, null=True, blank=True)
    ipertensione = models.CharField(max_length=100, null=True, blank=True)
    m_tiroidee = models.CharField(max_length=100, null=True, blank=True)
    m_polmonari = models.CharField(max_length=100, null=True, blank=True)
    tumori = models.CharField(max_length=100, null=True, blank=True)
    allergie = models.CharField(max_length=100, null=True, blank=True)
    m_psichiatriche = models.CharField(max_length=100, null=True, blank=True)

    patologie = models.CharField(max_length=100, null=True, blank=True)
    p_p_altro = models.CharField(max_length=100, null=True, blank=True)
    t_farmaco = models.CharField(max_length=100, null=True, blank=True)
    t_dosaggio = models.CharField(max_length=100, null=True, blank=True)
    t_durata = models.CharField(max_length=100, null=True, blank=True)

    ## DOMINIO ANAMNESI PATOLOGICA REMOTA
    p_cardiovascolari = models.CharField(max_length=100, null=True, blank=True)
    m_metabolica = models.CharField(max_length=100, null=True, blank=True)
    p_respiratori_cronici = models.CharField(max_length=100, null=True, blank=True)
    m_neurologica = models.CharField(max_length=100, null=True, blank=True)
    m_endocrina = models.CharField(max_length=100, null=True, blank=True)
    m_autoimmune = models.CharField(max_length=100, null=True, blank=True)
    p_epatici = models.CharField(max_length=100, null=True, blank=True)
    m_renale = models.CharField(max_length=100, null=True, blank=True)
    d_gastrointestinali = models.CharField(max_length=100, null=True, blank=True)
    
    ## DOMINIO ESAME OBBIETTIVO
    eloquio = models.CharField(max_length=100, null=True, blank=True)
    s_nutrizionale = models.CharField(max_length=100, null=True, blank=True)
    a_genarale = models.CharField(max_length=100, null=True, blank=True)
    psiche = models.CharField(max_length=100, null=True, blank=True)
    r_ambiente = models.CharField(max_length=100, null=True, blank=True)
    s_emotivo = models.CharField(max_length=100, null=True, blank=True)
    costituzione = models.CharField(max_length=100, null=True, blank=True)
    statura = models.CharField(max_length=100, null=True, blank=True)

    ## DOMINIO INFORMAZIONE DEL SANGUE
    blood_group = models.CharField(max_length=3, null=True, blank=True)
    rh_factor = models.CharField(max_length=3, null=True, blank=True)
    pressure_min = models.CharField(max_length=100, null=True, blank=True)
    pressure_max = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Paziente: {self.name} {self.surname}"

# tabella REFERTI ETA' METABOLICA
class RefertiEtaMetabolica(models.Model):
    dottore = models.ForeignKey(
        UtentiRegistratiCredenziali,
        on_delete=models.CASCADE,
        related_name='referti_eta_metabolica', 
        null=True
    )

    paziente = models.ForeignKey(
        TabellaPazienti,
        on_delete=models.CASCADE,
        related_name='referti_eta_metabolica'
    )

    data_referto = models.DateTimeField(default=timezone.now)

    # --- DOMINI CLINICI ---
    # COMPOSIZIONE CORPOREA
    bmi = models.CharField(max_length=100, null=True, blank=True) 
    grasso = models.CharField(max_length=100, null=True, blank=True)
    acqua = models.CharField(max_length=100, null=True, blank=True)
    massa_muscolare = models.CharField(max_length=100, null=True, blank=True)
    bmr = models.CharField(max_length=100, null=True, blank=True)
    whr = models.CharField(max_length=100, null=True, blank=True)
    whtr = models.CharField(max_length=100, null=True, blank=True)

    # GLICEMICO
    glicemia = models.CharField(max_length=100, null=True, blank=True)
    ogtt = models.CharField(max_length=100, null=True, blank=True)
    emoglobina_g = models.CharField(max_length=100, null=True, blank=True)
    insulina_d = models.CharField(max_length=100, null=True, blank=True)
    curva_i = models.CharField(max_length=100, null=True, blank=True)
    homa_ir = models.CharField(max_length=100, null=True, blank=True)
    tyg = models.CharField(max_length=100, null=True, blank=True)

    # LIPIDICO
    c_tot = models.CharField(max_length=100, null=True, blank=True)
    hdl = models.CharField(max_length=100, null=True, blank=True)
    ldl = models.CharField(max_length=100, null=True, blank=True)
    trigliceridi = models.CharField(max_length=100, null=True, blank=True)

    # METABOLICO EPATICO
    ast = models.CharField(max_length=100, null=True, blank=True)
    alt = models.CharField(max_length=100, null=True, blank=True)
    ggt = models.CharField(max_length=100, null=True, blank=True)
    bili_t = models.CharField(max_length=100, null=True, blank=True)

    # INFIAMMAZIONE
    pcr = models.CharField(max_length=100, null=True, blank=True)
    hgs = models.CharField(max_length=100, null=True, blank=True)
    sii = models.CharField(max_length=100, null=True, blank=True)

    # STRESS
    c_plasmatico = models.CharField(max_length=100, null=True, blank=True)

    # ALTRI DATI
    massa_ossea = models.CharField(max_length=100, null=True, blank=True)
    eta_metabolica = models.CharField(max_length=100, null=True, blank=True)
    grasso_viscerale = models.CharField(max_length=100, null=True, blank=True)
    punteggio_fisico = models.CharField(max_length=100, null=True, blank=True)
    storico_punteggi = models.JSONField(default=list, blank=True)

    # DATI ANTROPOMETRICI
    height = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    bmi_detection_date = models.DateField(null=True, blank=True)

    # CIRCONFERENZA ADDOMINALE
    girth_value = models.CharField(max_length=255, null=True, blank=True)
    girth_notes = models.TextField(blank=True, null=True)
    girth_date = models.DateField(null=True, blank=True)

    def aggiungi_punteggio(self, nuovo_punteggio):
        self.storico_punteggi.append({
            "punteggio": nuovo_punteggio,
            "data": timezone.now().isoformat()
        })
        self.punteggio_fisico = nuovo_punteggio
        self.save(update_fields=["punteggio_fisico", "storico_punteggi"])

    def __str__(self):
        return f"Referto {self.id} - {self.paziente.name} {self.paziente.surname} - {self.data_referto.date()}"


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

    #DOMINIO COGNITIVO
    MMSE = models.IntegerField(null=True, blank=True)

    #DOMINIO PSICOLOGICO
    GDS = models.IntegerField(null=True, blank=True)
    LOC = models.IntegerField(null=True, blank=True)

    #DOMINIO SENSORIALE
    Vista = models.IntegerField(null=True, blank=True)
    Udito = models.IntegerField(null=True, blank=True)

    #DOMINIO DELLA VITALITA'
    HGS = models.TextField(null=True, blank=True)
    PFT = models.IntegerField(null=True, blank=True)

    #SISTEMA IMMUNITARIO
    ISQ = models.IntegerField(null=True, blank=True)
    BMI = models.FloatField(null=True, blank=True)
    CDP = models.FloatField(null=True, blank=True)
    WHR = models.FloatField(null=True, blank=True)
    WHR_Ratio = models.TextField(null=True, blank=True)

    #DOMINIO DELLA LOCOMOZIONE
    CST = models.FloatField(null=True, blank=True)
    GS = models.FloatField(null=True, blank=True)
    PPT = models.IntegerField(null=True, blank=True)
    SARC_F = models.IntegerField(null=True, blank=True)
    FSS = models.IntegerField(null=True, blank=True)

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

    #BIOMARCATORI CIRCOLANTI DELL'INFIAMMAZIONE
    Inter_6 = models.FloatField(null=True, blank=True)
    Tnf = models.FloatField(null=True, blank=True)
    Mono = models.FloatField(null=True, blank=True)
    Mono_el = models.FloatField(null=True, blank=True)
    Proteins_c = models.FloatField(null=True, blank=True)
    wbc = models.FloatField(null=True, blank=True)
    Lymph = models.FloatField(null=True, blank=True)
    Lymph_el = models.FloatField(null=True, blank=True)
      
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

# ELENCO ESAMI
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

# TABELLA APPUNTAMENTI
class Appointment(models.Model):
    dottore = models.ForeignKey(UtentiRegistratiCredenziali, on_delete=models.CASCADE, null=True, blank=True)
    cognome_paziente = models.CharField(max_length=255, blank=True, null=True)
    nome_paziente = models.CharField(max_length=255, blank=True, null=True)
    tipologia_visita = models.CharField(max_length=100, choices=[('Fisioterapia Sportiva', 'Fisioterapia Sportiva'), ('Fisioterapia e Riabilitazione', 'Fisioterapia e Riabilitazione'), ('Fisioestetica', 'Fisioestetica')], blank=True, null=True)
    data = models.DateField(default=datetime.now)
    giorno = models.CharField(max_length=255, blank=True, null=True)
    orario = models.TimeField()
    durata = models.CharField(max_length=255, blank=True, null=True)
    voce_prezzario = models.CharField(max_length=255, blank=True, null=True)
    numero_studio = models.CharField(max_length=100, choices=[('Studio 1', 'Studio 1'), ('Studio 2', 'Studio 2'), ('Studio 3', 'Studio 3')], blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    confermato = models.BooleanField(default=False)  # Campo per segnare la conferma
    
    def __str__(self):
        return f"{self.nome_paziente} - {self.orario}"
    





#TABELLA CAPACITA' RESILIENZA
class Resilienza(models.Model):
    paziente = models.ForeignKey(
        TabellaPazienti,
        on_delete=models.CASCADE,
        related_name='resilienza'
    )
 
    hrv = models.FloatField(null=True, blank=True)
    cortisolo = models.FloatField(null=True, blank=True)
    ros = models.FloatField(null=True, blank=True)
    osi = models.FloatField(null=True, blank=True)
    droms = models.FloatField(null=True, blank=True)
    pcr = models.FloatField(null=True, blank=True)
    nlr = models.FloatField(null=True, blank=True)
    homa = models.FloatField(null=True, blank=True)
    ir = models.FloatField(null=True, blank=True)
    omega_3 = models.FloatField(null=True, blank=True)
    vo2max = models.FloatField(null=True, blank=True)

    risultato = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Referto - {self.paziente.name} {self.paziente.surname}"



class ValutazioneMS(models.Model):
    paziente = models.ForeignKey(
        TabellaPazienti,
        on_delete=models.CASCADE,
        related_name='valutazioneMS'
    )   

     # Attività fisica
    frequenza_a_f = models.CharField(max_length=50, blank=True, null=True)
    tipo_a_f = models.CharField(max_length=100, blank=True, null=True)
    stile_vita = models.CharField(max_length=100, blank=True, null=True)

    # Anamnesi muscolo-scheletrica
    terapie_inf = models.CharField(max_length=255, blank=True, null=True)
    diagnosi_t = models.CharField(max_length=255, blank=True, null=True)
    sintomi_t = models.TextField(blank=True, null=True)

    # Esame Generale
    palpazione = models.CharField(max_length=255, blank=True, null=True)
    osservazione = models.CharField(max_length=255, blank=True, null=True)
    m_attiva = models.CharField(max_length=255, blank=True, null=True)
    m_passiva = models.CharField(max_length=255, blank=True, null=True)
    dolorabilità = models.CharField(max_length=255, blank=True, null=True)
    scala_v_a = models.CharField(max_length=50, blank=True, null=True)

    # Esame muscolo-scheletrico
    mo_attivo = models.CharField(max_length=255, blank=True, null=True)
    mo_a_limitazioni = models.CharField(max_length=255, blank=True, null=True)
    mo_passivo = models.CharField(max_length=255, blank=True, null=True)
    mo_p_limitazioni = models.CharField(max_length=255, blank=True, null=True)
    comparazioni_m = models.TextField(blank=True, null=True)
    circ_polp = models.CharField(max_length=50, blank=True, null=True)
    tono_m = models.CharField(max_length=50, blank=True, null=True)
    scala_ashworth = models.CharField(max_length=100, blank=True, null=True)

    # Esame posturale
    v_frontale = models.CharField(max_length=255, blank=True, null=True)
    v_laterale = models.CharField(max_length=255, blank=True, null=True)
    p_testa = models.CharField(max_length=100, blank=True, null=True)
    spalle = models.CharField(max_length=100, blank=True, null=True)
    ombelico = models.CharField(max_length=100, blank=True, null=True)
    a_inferiori = models.CharField(max_length=100, blank=True, null=True)
    piedi = models.CharField(max_length=100, blank=True, null=True)
    colonna_v = models.CharField(max_length=100, blank=True, null=True)
    curvatura_c = models.CharField(max_length=100, blank=True, null=True)
    curvatura_d = models.CharField(max_length=100, blank=True, null=True)
    curvatura_l = models.CharField(max_length=100, blank=True, null=True)
    posizione_b = models.CharField(max_length=100, blank=True, null=True)
    equilibrio_s = models.CharField(max_length=100, blank=True, null=True)
    equilibrio_d = models.CharField(max_length=100, blank=True, null=True)
    p_dolenti = models.CharField(max_length=255, blank=True, null=True)

    # Valutazione complessiva funzionale
    gravita_disfunzione_posturale = models.CharField(max_length=100, blank=True, null=True)
    rischio_infortuni = models.CharField(max_length=100, blank=True, null=True)
    suggerimenti = models.CharField(max_length=255, blank=True, null=True)
    considerazioni_finali = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Referto - {self.paziente.name} {self.paziente.surname}"

