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

    # Risultati dei test sui globuli bianchi
    wbc = models.FloatField(null=True, blank=True)
    baso = models.FloatField(null=True, blank=True)
    eosi = models.IntegerField(null=True, blank=True)
    lymph = models.FloatField(null=True, blank=True)
    mono = models.FloatField(null=True, blank=True)
    neut = models.FloatField(null=True, blank=True)

    # Risultati dei test sui globuli rossi
    rbc = models.FloatField(null=True, blank=True)
    hct = models.FloatField(null=True, blank=True)
    hgb = models.FloatField(null=True, blank=True)
    mch = models.FloatField(null=True, blank=True)
    mchc = models.FloatField(null=True, blank=True)
    mcv = models.FloatField(null=True, blank=True)

    # Altri marker chiave
    glucose = models.FloatField(null=True, blank=True)
    azotemia = models.FloatField(null=True, blank=True)
    creatinine = models.FloatField(null=True, blank=True)
    ferritin = models.FloatField(null=True, blank=True)
    albumin = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    bilirubin = models.FloatField(null=True, blank=True)
    uric_acid = models.FloatField(null=True, blank=True)

    biological_age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Dati Estesi Referto ID: {self.referto.id}"
    

    
    #obri_index = models.FloatField(null=True, blank=True)
    #aa_epa = models.FloatField(null=True, blank=True)
    #aa_dha = models.FloatField(null=True, blank=True)
    #homa_test = models.FloatField(null=True, blank=True)
    #cardiovascular_risk = models.FloatField(null=True, blank=True)
    