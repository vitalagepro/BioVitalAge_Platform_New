from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import UtentiRegistratiCredenziali,TabellaPazienti, ArchivioReferti, DatiEstesiReferti
from .utils import calculate_biological_age
from django.contrib.sessions.models import Session
from django.db.models import OuterRef, Subquery
from django.db import transaction

# Create your views here.

class LoginRenderingPage(View):
    def get(self, request):
        return render(request, 'includes/login.html')

class HomePageRender(View):

    def get(self, request):
        persone = TabellaPazienti.objects.all().order_by('-id')[:5]
        
        # Ottieni il referto più recente per ogni paziente
        ultimo_referto = ArchivioReferti.objects.filter(paziente=OuterRef('referto__paziente')).order_by('-data_referto')

        # Ottieni i dati estesi associati al referto più recente di ciascun paziente
        datiEstesi = DatiEstesiReferti.objects.filter(referto=Subquery(ultimo_referto.values('id')[:1]))

        context = {
            'persone': persone,
            'datiEstesi': datiEstesi
        }

        return render(request, "includes/homePage.html", context)
    
    def post(self, request):

        emailInput = request.POST['email']
        passwordInput = request.POST['password']

       
        Query = UtentiRegistratiCredenziali.objects.all().values()

        for record in Query:  
            for key, value in record.items():
                if key == 'email':
                    if value == emailInput: 

                        if record['password'] == passwordInput:

                            dottore = UtentiRegistratiCredenziali.objects.get(email=emailInput, password=passwordInput)
                            request.session['dottore_id'] = dottore.id

                            persone = TabellaPazienti.objects.all().order_by('-id')[:5]
        
                            # Ottieni il referto più recente per ogni paziente
                            ultimo_referto = ArchivioReferti.objects.filter(paziente=OuterRef('referto__paziente')).order_by('-data_referto')

                            # Ottieni i dati estesi associati al referto più recente di ciascun paziente
                            datiEstesi = DatiEstesiReferti.objects.filter(referto=Subquery(ultimo_referto.values('id')[:1]))

                            context = {
                                'persone': persone,
                                'datiEstesi': datiEstesi
                            }

                            return render(request, "includes/homePage.html", context)
                        
                        else:
                            return render(request, 'includes/login.html', {'error' : 'Password errata' })
                        
                    else:
                        return render(request, 'includes/login.html', {'error' : 'Email inserita non valida o non registrata' })


def safe_float(data, key, default=0.0):
    try:
        return float(data.get(key, default))
    except (ValueError, TypeError):
        return default


class CalcolatoreRender(View):
    def get(self, request):
        return render(request, 'includes/calcolatore.html')


    def post(self, request):
        data = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}
        dottore_id = request.session.get('dottore_id')

        try:
            dottore = UtentiRegistratiCredenziali.objects.get(id=dottore_id)

            # Controlla se esiste un paziente con lo stesso nome e cognome
            paziente = TabellaPazienti.objects.filter(
                name=data.get('name'),
                surname=data.get('surname'),
                codice_fiscale=data.get('codice_fiscale') 
            ).first()

            if paziente: 
                
                campi_opzionali = [
                    # Aggiunti tutti i campi definiti nel modello e HTML
                    'd_roms', 'osi', 'pat', 'fa_saturated', 'o9o7fatty_acids', 'o3fatty_acids', 'o6fatty_acids', 's_u_fatty_acids',
                    'o6o3_fatty_acids_quotient', 'aa_epa_quotient', 'O3_index', 'wbc', 'basophils', 'eosinophils', 'lymphocytes',
                    'monocytes', 'neutrophils', 'neut_ul', 'lymph_ul', 'mono_ul', 'eosi_ul', 'baso_ul', 'rbc', 'hgb', 'hct',
                    'mcv', 'mch', 'mchc', 'rdwsd', 'rdwcv', 'azotemia', 'glucose', 'creatinine', 'ferritin', 'albumin', 'protein',
                    'bilirubin', 'uric_acid', 'plt', 'mpv', 'plcr', 'pct', 'pdw', 'tot_chol', 'ldl_chol', 'hdl_chol', 'trigl',
                    'na', 'k', 'mg', 'ci', 'ca', 'p', 'fe', 'transferrin', 'glicemy', 'insulin', 'homa', 'ir', 'albuminemia',
                    'tot_prot', 'tot_prot_ele', 'albumin_ele', 'a_1', 'a_2', 'b_1', 'b_2', 'gamma', 'albumin_dI', 'a_1_dI',
                    'a_2_dI', 'b_1_dI', 'b_2_dI', 'gamma_dI', 'ag_rap', 'cm', 'b_2_spike', 'b_2_spike_m1', 'got', 'gpt',
                    'g_gt', 'a_photo', 'tot_bili', 'direct_bili', 'idirect_bili', 'ves', 'pcr_c', 's_weight', 'ph', 'glucose_ex',
                    'proteins_ex', 'blood_ex', 'ketones', 'uro', 'bilirubin_ex', 'leuc', 'homocysteine'
                ]

                # Verifica se almeno un campo opzionale è stato inserito
                if any(data.get(campo) for campo in campi_opzionali):

                    paziente_query = get_object_or_404(TabellaPazienti, id=paziente.id)

                    # Salva i dati del referto
                    referto = ArchivioReferti(
                        paziente=paziente_query,
                        descrizione=data.get('descrizione'),
                        documento=request.FILES.get('documento')
                    )
                    referto.save()

                    # Estrai i dati necessari per la tabella DatiEstesiReferti
                    chronological_age = int(data.get('chronological_age'))
                    d_roms = safe_float(data, 'd_roms')
                    osi = safe_float(data, 'osi')
                    pat = safe_float(data, 'pat')

                    # Omega Screening
                    fa_saturated = safe_float(data, 'fa_saturated')
                    o9o7fatty_acids = safe_float(data, 'o9o7fatty_acids')
                    o3fatty_acids = safe_float(data, 'o3fatty_acids')
                    o6fatty_acids = safe_float(data, 'o6fatty_acids')
                    s_u_fatty_acids = safe_float(data, 's_u_fatty_acids')
                    o6o3_fatty_acids_quotient = safe_float(data, 'o6o3_fatty_acids_quotient')
                    aa_epa_quotient = safe_float(data, 'aa_epa_quotient')
                    O3_index = safe_float(data, 'O3_index')

                    # White Blood Cells
                    wbc = safe_float(data, 'wbc')
                    baso = safe_float(data, 'baso')
                    eosi = safe_float(data, 'eosi')
                    lymph = safe_float(data, 'lymph')
                    mono = safe_float(data, 'mono')
                    neut = safe_float(data, 'neut')
                    neut_ul = safe_float(data, 'neut_ul')
                    lymph_ul = safe_float(data, 'lymph_ul')
                    mono_ul = safe_float(data, 'mono_ul')
                    eosi_ul = safe_float(data, 'eosi_ul')
                    baso_ul = safe_float(data, 'baso_ul')

                    # Red Blood Cells
                    rbc = safe_float(data, 'rbc')
                    hgb = safe_float(data, 'hgb')
                    hct = safe_float(data, 'hct')
                    mcv = safe_float(data, 'mcv')
                    mch = safe_float(data, 'mch')
                    mchc = safe_float(data, 'mchc')
                    rdwsd = safe_float(data, 'rdwsd')
                    rdwcv = safe_float(data, 'rdwcv')

                    # Renal Functionality
                    azotemia = safe_float(data, 'azotemia')
                    creatinine = safe_float(data, 'creatinine')
                    uric_acid = safe_float(data, 'uric_acid')


                    # Clotting Status
                    plt = safe_float(data, 'plt')
                    mpv = safe_float(data, 'mpv')
                    plcr  = safe_float(data, 'plcr')
                    pct = safe_float(data, 'pct')
                    pdw = safe_float(data, 'pdw')
            
                
                    # Martial Trim
                    fe = safe_float(data, 'fe')
                    ferritin = safe_float(data, 'ferritin')
                    transferrin = safe_float(data, 'transferrin')

                    # Diabetological Setup
                    glicemy = safe_float(data, 'glicemy')
                    insulin = safe_float(data, 'insulin')
                    homa = safe_float(data, 'homa')
                    ir = safe_float(data, 'ir')

                    # Proteins
                    albuminemia = safe_float(data, 'albuminemia')
                    tot_prot = safe_float(data, 'tot_prot')

                    # Seroprotein Electrophoresis
                    tot_prot_ele = safe_float(data, 'tot_prot_ele')
                    albumin_ele = safe_float(data, 'albumin_ele')
                    a_1 = safe_float(data, 'a_1')
                    a_2 = safe_float(data, 'a_2')
                    b_1 = safe_float(data, 'b_1')
                    b_2 = safe_float(data, 'b_2')
                    gamma = safe_float(data, 'gamma')
                    albumin_dI = safe_float(data, 'albumin_dI')
                    a_1_dI = safe_float(data, 'a_1_dI')
                    a_2_dI = safe_float(data, 'a_2_dI')
                    b_1_dI = safe_float(data, 'b_1_dI')
                    b_2_dI = safe_float(data, 'b_2_dI')
                    gamma_dI = safe_float(data, 'gamma_dI')
                    ag_rap = safe_float(data, 'ag_rap')
                    cm = safe_float(data, 'cm')
                    b_2_spike = safe_float(data, 'b_2_spike')
                    b_2_spike_m1 = safe_float(data, 'b_2_spike_m1')

                    # Liver Functionality
                    got = safe_float(data, 'got')
                    gpt = safe_float(data, 'gpt')
                    g_gt = safe_float(data, 'g_gt')
                    a_photo = safe_float(data, 'a_photo')
                    tot_bili = safe_float(data, 'tot_bili')
                    direct_bili = safe_float(data, 'direct_bili')
                    idirect_bili = safe_float(data, 'idirect_bili')

                    # Indices of Phlogosis
                    ves = safe_float(data, 'ves')
                    pcr_c = safe_float(data, 'pcr_c')

                    # Urinalysis
                    s_weight = safe_float(data, 's_weight')
                    ph = safe_float(data, 'ph')
                    glucose_ex = safe_float(data, 'glucose')
                    proteins_ex = safe_float(data, 'proteins_ex')
                    blood_ex = safe_float(data, 'blood_ex')
                    ketones = safe_float(data, 'ketones')
                    uro = safe_float(data, 'uro')
                    bilirubin_ex = safe_float(data, 'bilirubin_ex')
                    leuc = safe_float(data, 'leuc')

                    # Other Exams
                    homocysteine = safe_float(data, 'homocysteine')

                    # Lipid Appearance
                    tot_chol = safe_float(data, 'tot_chol')
                    ldl_chol = safe_float(data, 'ldl_chol')
                    hdl_chol = safe_float(data, 'hdl_chol')
                    trigl = safe_float(data, 'trigl')

                    # Minerals
                    na = safe_float(data, 'na')
                    k = safe_float(data, 'k')
                    mg = safe_float(data, 'mg')
                    ci = safe_float(data, 'ci')
                    ca = safe_float(data, 'ca')
                    p = safe_float(data, 'p')

                    exams = [glucose_ex, creatinine, ferritin, albumin_ele, proteins_ex, bilirubin_ex, uric_acid]

                    # Calcolo dell'età biologica
                    biological_age = calculate_biological_age(
                        chronological_age, d_roms, osi, pat, wbc, baso,
                        eosi, lymph, mono, neut, rbc, hgb, 
                        hct, mcv, mch, mchc, rdwsd, exams
                    )


                    # Salvataggio dei dati
                    dati_estesi = DatiEstesiReferti(
                        referto=referto,
                        d_roms=d_roms,
                        osi=osi,
                        pat=pat,
                        fa_saturated=fa_saturated,
                        o9o7fatty_acids=o9o7fatty_acids,
                        o3fatty_acids=o3fatty_acids,
                        o6fatty_acids=o6fatty_acids,
                        s_u_fatty_acids=s_u_fatty_acids,
                        o6o3_fatty_acids_quotient=o6o3_fatty_acids_quotient,
                        aa_epa_quotient=aa_epa_quotient,
                        O3_index=O3_index,
                        wbc=wbc,
                        baso=baso,
                        eosi=eosi,
                        lymph=lymph,
                        mono=mono,
                        neut=neut,
                        neut_ul=neut_ul,
                        lymph_ul=lymph_ul,
                        mono_ul=mono_ul,
                        eosi_ul=eosi_ul,
                        baso_ul=baso_ul,
                        rbc=rbc,
                        hct=hct,
                        hgb=hgb,
                        mch=mch,
                        mchc=mchc,
                        mcv=mcv,
                        rdwsd=rdwsd,
                        rdwcv=rdwcv,
                        azotemia=azotemia,
                        creatinine=creatinine,
                        ferritin=ferritin,
                        uric_acid=uric_acid,
                        biological_age=biological_age,
                        
                        # Nuovi campi
                        plt = plt,
                        mpv = mpv,
                        plcr  = plcr,
                        pct = pct,
                        pdw = pdw,
                        fe=fe,
                        transferrin=transferrin,
                        glicemy=glicemy,
                        insulin=insulin,
                        homa=homa,
                        ir=ir,
                        albuminemia=albuminemia,
                        tot_prot=tot_prot,
                        tot_prot_ele=tot_prot_ele,
                        albumin_ele=albumin_ele,
                        a_1=a_1,
                        a_2=a_2,
                        b_1=b_1,
                        b_2=b_2,
                        gamma=gamma,
                        albumin_dI=albumin_dI,
                        a_1_dI=a_1_dI,
                        a_2_dI=a_2_dI,
                        b_1_dI=b_1_dI,
                        b_2_dI=b_2_dI,
                        gamma_dI=gamma_dI,
                        ag_rap=ag_rap,
                        cm=cm,
                        b_2_spike=b_2_spike,
                        b_2_spike_m1=b_2_spike_m1,
                        got=got,
                        gpt=gpt,
                        g_gt=g_gt,
                        a_photo=a_photo,
                        tot_bili=tot_bili,
                        direct_bili=direct_bili,
                        idirect_bili=idirect_bili,
                        ves=ves,
                        pcr_c=pcr_c,
                        s_weight=s_weight,
                        ph=ph,
                        glucose_ex=glucose_ex,
                        proteins_ex=proteins_ex,
                        blood_ex=blood_ex,
                        ketones=ketones,
                        uro=uro,
                        bilirubin_ex=bilirubin_ex,
                        leuc=leuc,
                        homocysteine=homocysteine,
                        tot_chol=tot_chol,
                        ldl_chol=ldl_chol,
                        hdl_chol=hdl_chol,
                        trigl=trigl,
                        na=na,
                        k=k,
                        mg=mg,
                        ci=ci,
                        ca=ca,
                        p=p
                    )
                    dati_estesi.save()


                    print("Dati estesi salvati:", dati_estesi)

                    # Context da mostrare nel template
                    context = {
                        "show_modal": True,
                        "biological_age": biological_age,
                        "data": data,
                    }
                    
                    return render(request, "includes/calcolatore.html", context)
                
                else:
                    print("Nessun campo opzionale compilato. Operazione interrotta.")
                    context = {
                        "show_modal": False,
                        "error": "Nessun dato opzionale inserito. Referto e dati estesi non salvati.",
                        "data": data,
                    }
                    return render(request, "includes/calcolatore.html", context)

            else:
                # Controlla se solo i campi richiesti sono popolati
                campi_obbligatori = ['name', 'surname', 'dob', 'gender', 'place_of_birth', 'codice_fiscale', 'chronological_age']
                campi_opzionali = [
                    # Aggiunti tutti i campi definiti nel modello e HTML
                    'd_roms', 'osi', 'pat', 'fa_saturated', 'o9o7fatty_acids', 'o3fatty_acids', 'o6fatty_acids', 's_u_fatty_acids',
                    'o6o3_fatty_acids_quotient', 'aa_epa_quotient', 'O3_index', 'wbc', 'basophils', 'eosinophils', 'lymphocytes',
                    'monocytes', 'neutrophils', 'neut_ul', 'lymph_ul', 'mono_ul', 'eosi_ul', 'baso_ul', 'rbc', 'hgb', 'hct',
                    'mcv', 'mch', 'mchc', 'rdwsd', 'rdwcv', 'azotemia', 'glucose', 'creatinine', 'ferritin', 'albumin', 'protein',
                    'bilirubin', 'uric_acid', 'plt', 'mpv', 'plcr', 'pct', 'pdw', 'tot_chol', 'ldl_chol', 'hdl_chol', 'trigl',
                    'na', 'k', 'mg', 'ci', 'ca', 'p', 'fe', 'transferrin', 'glicemy', 'insulin', 'homa', 'ir', 'albuminemia',
                    'tot_prot', 'tot_prot_ele', 'albumin_ele', 'a_1', 'a_2', 'b_1', 'b_2', 'gamma', 'albumin_dI', 'a_1_dI',
                    'a_2_dI', 'b_1_dI', 'b_2_dI', 'gamma_dI', 'ag_rap', 'cm', 'b_2_spike', 'b_2_spike_m1', 'got', 'gpt',
                    'g_gt', 'a_photo', 'tot_bili', 'direct_bili', 'idirect_bili', 'ves', 'pcr_c', 's_weight', 'ph', 'glucose_ex',
                    'proteins_ex', 'blood_ex', 'ketones', 'uro', 'bilirubin_ex', 'leuc', 'homocysteine'
                ]

                if all(not data.get(campo) for campo in campi_opzionali):
                    # Salva solo i dati personali e l'età cronologica
                    paziente = TabellaPazienti(
                        dottore=dottore,
                        name=data.get('name'),
                        surname=data.get('surname'),
                        dob=data.get('dob'),
                        gender=data.get('gender'),
                        place_of_birth=data.get('place_of_birth'),
                        codice_fiscale=data.get('codice_fiscale')
                    )
                    paziente.save()
                    print("Paziente creato (solo campi obbligatori):", paziente)

                    dati_estesi = DatiEstesiReferti(
                        chronological_age=chronological_age,  
                    )
                    dati_estesi.save()
                  
                else:
                    # Salva tutti i dati del paziente
                    paziente = TabellaPazienti(
                        dottore= dottore,
                        name= data.get('name'),
                        surname= data.get('surname'),
                        dob= data.get('dob'),
                        gender= data.get('gender'),
                        place_of_birth= data.get('place_of_birth'),
                        codice_fiscale= data.get('codice_fiscale'),
                        chronological_age= data.get('chronological_age'),
                    )
                    paziente.save()
                    print("Paziente creato:", paziente)

                    # Salva i dati del referto
                    referto = ArchivioReferti(
                        paziente=paziente,
                        descrizione=data.get('descrizione'),
                        documento=request.FILES.get('documento')
                    )
                    referto.save()
                    print("Referto salvato:", referto)

                    # Estrai i dati necessari per la tabella DatiEstesiReferti
                    chronological_age = int(data.get('chronological_age'))
                    d_roms = safe_float(data, 'd_roms')
                    osi = safe_float(data, 'osi')
                    pat = safe_float(data, 'pat')

                    # Omega Screening
                    fa_saturated = safe_float(data, 'fa_saturated')
                    o9o7fatty_acids = safe_float(data, 'o9o7fatty_acids')
                    o3fatty_acids = safe_float(data, 'o3fatty_acids')
                    o6fatty_acids = safe_float(data, 'o6fatty_acids')
                    s_u_fatty_acids = safe_float(data, 's_u_fatty_acids')
                    o6o3_fatty_acids_quotient = safe_float(data, 'o6o3_fatty_acids_quotient')
                    aa_epa_quotient = safe_float(data, 'aa_epa_quotient')
                    O3_index = safe_float(data, 'O3_index')

                    # White Blood Cells
                    wbc = safe_float(data, 'wbc')
                    baso = safe_float(data, 'baso')
                    eosi = safe_float(data, 'eosi')
                    lymph = safe_float(data, 'lymph')
                    mono = safe_float(data, 'mono')
                    neut = safe_float(data, 'neut')
                    neut_ul = safe_float(data, 'neut_ul')
                    lymph_ul = safe_float(data, 'lymph_ul')
                    mono_ul = safe_float(data, 'mono_ul')
                    eosi_ul = safe_float(data, 'eosi_ul')
                    baso_ul = safe_float(data, 'baso_ul')

                    # Red Blood Cells
                    rbc = safe_float(data, 'rbc')
                    hgb = safe_float(data, 'hgb')
                    hct = safe_float(data, 'hct')
                    mcv = safe_float(data, 'mcv')
                    mch = safe_float(data, 'mch')
                    mchc = safe_float(data, 'mchc')
                    rdwsd = safe_float(data, 'rdwsd')
                    rdwcv = safe_float(data, 'rdwcv')

                    # Renal Functionality
                    azotemia = safe_float(data, 'azotemia')
                    creatinine = safe_float(data, 'creatinine')
                    uric_acid = safe_float(data, 'uric_acid')

                    # Clotting Status
                    plt = safe_float(data, 'plt')
                    mpv = safe_float(data, 'mpv')
                    plcr  = safe_float(data, 'plcr')
                    pct = safe_float(data, 'pct')
                    pdw = safe_float(data, 'pdw')

                    # Martial Trim
                    fe = safe_float(data, 'fe')
                    ferritin = safe_float(data, 'ferritin')
                    transferrin = safe_float(data, 'transferrin')

                    # Diabetological Setup
                    glicemy = safe_float(data, 'glicemy')
                    insulin = safe_float(data, 'insulin')
                    homa = safe_float(data, 'homa')
                    ir = safe_float(data, 'ir')

                    # Proteins
                    albuminemia = safe_float(data, 'albuminemia')
                    tot_prot = safe_float(data, 'tot_prot')

                    # Seroprotein Electrophoresis
                    tot_prot_ele = safe_float(data, 'tot_prot_ele')
                    albumin_ele = safe_float(data, 'albumin_ele')
                    a_1 = safe_float(data, 'a_1')
                    a_2 = safe_float(data, 'a_2')
                    b_1 = safe_float(data, 'b_1')
                    b_2 = safe_float(data, 'b_2')
                    gamma = safe_float(data, 'gamma')
                    albumin_dI = safe_float(data, 'albumin_dI')
                    a_1_dI = safe_float(data, 'a_1_dI')
                    a_2_dI = safe_float(data, 'a_2_dI')
                    b_1_dI = safe_float(data, 'b_1_dI')
                    b_2_dI = safe_float(data, 'b_2_dI')
                    gamma_dI = safe_float(data, 'gamma_dI')
                    ag_rap = safe_float(data, 'ag_rap')
                    cm = safe_float(data, 'cm')
                    b_2_spike = safe_float(data, 'b_2_spike')
                    b_2_spike_m1 = safe_float(data, 'b_2_spike_m1')

                    # Liver Functionality
                    got = safe_float(data, 'got')
                    gpt = safe_float(data, 'gpt')
                    g_gt = safe_float(data, 'g_gt')
                    a_photo = safe_float(data, 'a_photo')
                    tot_bili = safe_float(data, 'tot_bili')
                    direct_bili = safe_float(data, 'direct_bili')
                    idirect_bili = safe_float(data, 'idirect_bili')

                    # Indices of Phlogosis
                    ves = safe_float(data, 'ves')
                    pcr_c = safe_float(data, 'pcr_c')

                    # Urinalysis
                    s_weight = safe_float(data, 's_weight')
                    ph = safe_float(data, 'ph')
                    glucose_ex = safe_float(data, 'glucose')
                    proteins_ex = safe_float(data, 'proteins_ex')
                    blood_ex = safe_float(data, 'blood_ex')
                    ketones = safe_float(data, 'ketones')
                    uro = safe_float(data, 'uro')
                    bilirubin_ex = safe_float(data, 'bilirubin_ex')
                    leuc = safe_float(data, 'leuc')

                    # Other Exams
                    homocysteine = safe_float(data, 'homocysteine')

                    # Lipid Appearance
                    tot_chol = safe_float(data, 'tot_chol')
                    ldl_chol = safe_float(data, 'ldl_chol')
                    hdl_chol = safe_float(data, 'hdl_chol')
                    trigl = safe_float(data, 'trigl')

                    # Minerals
                    na = safe_float(data, 'na')
                    k = safe_float(data, 'k')
                    mg = safe_float(data, 'mg')
                    ci = safe_float(data, 'ci')
                    ca = safe_float(data, 'ca')
                    p = safe_float(data, 'p')

                    exams = [glucose_ex, creatinine, ferritin, albumin_ele, proteins_ex, bilirubin_ex, uric_acid]

                    # Calcolo dell'età biologica
                    biological_age = calculate_biological_age(
                        chronological_age, d_roms, osi, pat, wbc, baso,
                        eosi, lymph, mono, neut, rbc, hgb, 
                        hct, mcv, mch, mchc, rdwsd, exams
                    )

                    print(referto.id)

                    # Salvataggio dei dati
                    dati_estesi = DatiEstesiReferti(
                        referto=referto,
                        d_roms=d_roms,
                        osi=osi,
                        pat=pat,
                        fa_saturated=fa_saturated,
                        o9o7fatty_acids=o9o7fatty_acids,
                        o3fatty_acids=o3fatty_acids,
                        o6fatty_acids=o6fatty_acids,
                        s_u_fatty_acids=s_u_fatty_acids,
                        o6o3_fatty_acids_quotient=o6o3_fatty_acids_quotient,
                        aa_epa_quotient=aa_epa_quotient,
                        O3_index=O3_index,
                        wbc=wbc,
                        baso=baso,
                        eosi=eosi,
                        lymph=lymph,
                        mono=mono,
                        neut=neut,
                        neut_ul=neut_ul,
                        lymph_ul=lymph_ul,
                        mono_ul=mono_ul,
                        eosi_ul=eosi_ul,
                        baso_ul=baso_ul,
                        rbc=rbc,
                        hct=hct,
                        hgb=hgb,
                        mch=mch,
                        mchc=mchc,
                        mcv=mcv,
                        rdwsd=rdwsd,
                        rdwcv=rdwcv,
                        azotemia=azotemia,
                        creatinine=creatinine,
                        ferritin=ferritin,
                        uric_acid=uric_acid,
                        biological_age=biological_age,
                        
                        # Nuovi campi
                        plt = plt,
                        mpv = mpv,
                        plcr  = plcr,
                        pct = pct,
                        pdw = pdw,
                        fe=fe,
                        transferrin=transferrin,
                        glicemy=glicemy,
                        insulin=insulin,
                        homa=homa,
                        ir=ir,
                        albuminemia=albuminemia,
                        tot_prot=tot_prot,
                        tot_prot_ele=tot_prot_ele,
                        albumin_ele=albumin_ele,
                        a_1=a_1,
                        a_2=a_2,
                        b_1=b_1,
                        b_2=b_2,
                        gamma=gamma,
                        albumin_dI=albumin_dI,
                        a_1_dI=a_1_dI,
                        a_2_dI=a_2_dI,
                        b_1_dI=b_1_dI,
                        b_2_dI=b_2_dI,
                        gamma_dI=gamma_dI,
                        ag_rap=ag_rap,
                        cm=cm,
                        b_2_spike=b_2_spike,
                        b_2_spike_m1=b_2_spike_m1,
                        got=got,
                        gpt=gpt,
                        g_gt=g_gt,
                        a_photo=a_photo,
                        tot_bili=tot_bili,
                        direct_bili=direct_bili,
                        idirect_bili=idirect_bili,
                        ves=ves,
                        pcr_c=pcr_c,
                        s_weight=s_weight,
                        ph=ph,
                        glucose_ex=glucose_ex,
                        proteins_ex=proteins_ex,
                        blood_ex=blood_ex,
                        ketones=ketones,
                        uro=uro,
                        bilirubin_ex=bilirubin_ex,
                        leuc=leuc,
                        homocysteine=homocysteine,
                        tot_chol=tot_chol,
                        ldl_chol=ldl_chol,
                        hdl_chol=hdl_chol,
                        trigl=trigl,
                        na=na,
                        k=k,
                        mg=mg,
                        ci=ci,
                        ca=ca,
                        p=p
                    )
                    dati_estesi.save()

                    print("Dati estesi salvati:", dati_estesi)

                # Context da mostrare nel template
                context = {
                    "show_modal": True,
                    "biological_age": biological_age,
                    "data": data,
                }

                return render(request, "includes/calcolatore.html", context)

        except Exception as e:
            import traceback

            print("Errore incontrato:")
            print(traceback.format_exc())
            context = {
                "error": str(e),
                "data": data,
            }
            return render(request, "includes/calcolatore.html", context)


class RisultatiRender(View):
    def get(self, request):
        persone = TabellaPazienti.objects.all()
        
        # Ottieni il referto più recente per ogni paziente
        ultimo_referto = ArchivioReferti.objects.filter(paziente=OuterRef('referto__paziente')).order_by('-data_referto')

        # Ottieni i dati estesi associati al referto più recente di ciascun paziente
        datiEstesi = DatiEstesiReferti.objects.filter(referto=Subquery(ultimo_referto.values('id')[:1]))

        context = {
            'persone': persone,
            'datiEstesi': datiEstesi
        }

        return render(request, "includes/risultati.html", context)

class PersonaDetailView(View):
   
    def get(self, request, id):
        # Ottieni il paziente con l'ID specificato
        persona = get_object_or_404(TabellaPazienti, id=id)

        # Ottieni l'ultimo referto del paziente
        ultimo_referto = ArchivioReferti.objects.filter(paziente=persona).order_by('-data_referto').first()

        # Ottieni i dati estesi associati all'ultimo referto (se esiste)
        datiEstesi = None
        if ultimo_referto:
            datiEstesi = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()

        context = {
            'persona': persona,
            'ultimo_referto': ultimo_referto,
            'datiEstesi': datiEstesi
        }
        return render(request, "includes/persona_detail.html", context)

class CartellaPazienteView(View):

    def get(self, request, id):
        # Ottieni il paziente con l'ID specificato
        persona = get_object_or_404(TabellaPazienti, id=id)

        # Ottieni i 5 referti più recenti del paziente
        referti_recenti = persona.referti.all().order_by('-data_referto')[:5]

        # Ottieni i dati estesi associati a questi referti
        dati_estesi = DatiEstesiReferti.objects.filter(referto__in=referti_recenti)

        # Ottieni l'ultimo referto (il più recente)
        ultimo_referto = referti_recenti.first() if referti_recenti else None

       
        # Ottieni i dati estesi dell'ultimo referto
        dati_estesi_ultimo_referto = None
        if ultimo_referto:
            dati_estesi_ultimo_referto = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()

        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            'ultimo_referto': ultimo_referto,
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto
        }

        return render(request, "includes/cartellaPaziente.html", context)

class DatiBaseView(View):
    def get(self, request, id):
        persona = get_object_or_404(TabellaPazienti, id=id)
        context = {
            'persona': persona,
        }
        return render(request, "includes/dati_base.html", context)


class InserisciPazienteView(View):

    def get(self, request):
        return render(request, "includes/InserisciPaziente.html")
    
    def post(self, request):

        persona = get_object_or_404(TabellaPazienti, id=id)
        referti_recenti = persona.referti.all().order_by('-data_referto')[:5]
        dati_estesi = DatiEstesiReferti.objects.filter(referto__in=referti_recenti)
        ultimo_referto = referti_recenti.first() if referti_recenti else None

        dati_estesi_ultimo_referto = None
        if ultimo_referto:
            dati_estesi_ultimo_referto = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()

        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            'ultimo_referto': ultimo_referto,
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto
        }
         
        return render(request, "includes/cartellaPaziente.html", context)


class StatisticheView(View):

    def get(self, request):
        return render(request, "includes/statistiche.html")
    