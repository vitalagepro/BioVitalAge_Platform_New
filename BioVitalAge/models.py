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
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Male'), ('F', 'Female')])
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True, unique=True)
    chronological_age = models.IntegerField(null=True, blank=True)


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
    descrizione = models.TextField(null=True, blank=True)
    documento = models.FileField(upload_to='referti/', null=True, blank=True)

    def __str__(self):
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
    fa_saturated = models.FloatField(null=True, blank=True)
    o9o7fatty_acids = models.FloatField(null=True, blank=True)
    o3fatty_acids = models.FloatField(null=True, blank=True)
    o6fatty_acids = models.FloatField(null=True, blank=True)
    s_u_fatty_acids = models.FloatField(null=True, blank=True)
    o6o3_fatty_acids_quotient = models.FloatField(null=True, blank=True)
    aa_epa_quotient = models.FloatField(null=True, blank=True)
    O3_index = models.FloatField(null=True, blank=True)

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
    rbc = models.FloatField(null=True, blank=True)
    hct = models.FloatField(null=True, blank=True)
    hgb = models.FloatField(null=True, blank=True)
    mch = models.FloatField(null=True, blank=True)
    mchc = models.FloatField(null=True, blank=True)
    mcv = models.FloatField(null=True, blank=True)
    rdwsd = models.FloatField(null=True, blank=True)
    rdwcv = models.FloatField(null=True, blank=True)

    # Renal Functionality
    azotemia = models.FloatField(null=True, blank=True)
    creatinine = models.FloatField(null=True, blank=True)
    uric_acid = models.FloatField(null=True, blank=True)

    # Clotting Status
    plt = models.FloatField(null=True, blank=True)
    mpv = models.FloatField(null=True, blank=True)
    plcr = models.FloatField(null=True, blank=True)
    pct = models.FloatField(null=True, blank=True)
    pdw = models.FloatField(null=True, blank=True)

    # Lipid Appearance
    tot_chol = models.FloatField(null=True, blank=True)
    ldl_chol = models.FloatField(null=True, blank=True)
    hdl_chol = models.FloatField(null=True, blank=True)
    trigl = models.FloatField(null=True, blank=True)

    # Minerals
    na = models.FloatField(null=True, blank=True)
    k = models.FloatField(null=True, blank=True)
    mg = models.FloatField(null=True, blank=True)
    ci = models.FloatField(null=True, blank=True)
    ca = models.FloatField(null=True, blank=True)
    p = models.FloatField(null=True, blank=True)

    # Martial Trim
    fe = models.FloatField(null=True, blank=True)
    ferritin = models.FloatField(null=True, blank=True)
    transferrin = models.FloatField(null=True, blank=True)

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
    cm = models.FloatField(null=True, blank=True)
    b_2_spike = models.FloatField(null=True, blank=True)
    b_2_spike_m1 = models.FloatField(null=True, blank=True)

    # Liver Functionality
    got = models.FloatField(null=True, blank=True)
    gpt = models.FloatField(null=True, blank=True)
    g_gt = models.FloatField(null=True, blank=True)
    a_photo = models.FloatField(null=True, blank=True)
    tot_bili = models.FloatField(null=True, blank=True)
    direct_bili = models.FloatField(null=True, blank=True)
    idirect_bili = models.FloatField(null=True, blank=True)

    # Indices of Phlogosis
    ves = models.FloatField(null=True, blank=True)
    pcr_c = models.FloatField(null=True, blank=True)

    # Urinalysis
    s_weight = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    glucose_ex = models.FloatField(null=True, blank=True)
    proteins_ex = models.FloatField(null=True, blank=True)
    blood_ex = models.FloatField(null=True, blank=True)
    ketones = models.FloatField(null=True, blank=True)
    uro = models.FloatField(null=True, blank=True)
    bilirubin_ex = models.FloatField(null=True, blank=True)
    leuc = models.FloatField(null=True, blank=True)

    # Other Exams
    homocysteine = models.FloatField(null=True, blank=True)

    # Biological Age
    biological_age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Dati Estesi Referto ID: {self.referto.id}"
    
