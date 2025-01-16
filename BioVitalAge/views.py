from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import UtentiRegistratiCredenziali,TabellaPazienti, ArchivioReferti, DatiEstesiReferti
from .utils import calculate_biological_age
from django.contrib.sessions.models import Session
from django.db.models import OuterRef, Subquery
from django.db import transaction
from django.contrib import messages

# Create your views here.


class LoginRenderingPage(View):
    def get(self, request):
        return render(request, 'includes/login.html')




class HomePageRender(View):

    def get(self, request):
        persone = TabellaPazienti.objects.all().order_by('-id')[:5]
        
        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)
        
        # Ottieni il referto più recente per ogni paziente
        ultimo_referto = ArchivioReferti.objects.filter(paziente=OuterRef('referto__paziente')).order_by('-data_referto')

        # Ottieni i dati estesi associati al referto più recente di ciascun paziente
        datiEstesi = DatiEstesiReferti.objects.filter(referto=Subquery(ultimo_referto.values('id')[:1]))

        context = {
            'persone': persone,
            'datiEstesi': datiEstesi,
            'dottore': dottore
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
                                'datiEstesi': datiEstesi,
                                'dottore': dottore
                            }

                            return render(request, "includes/homePage.html", context)
                        
                        else:
                            return render(request, 'includes/login.html', {'error' : 'Password errata' })
                        
                    else:
                        return render(request, 'includes/login.html', {'error' : 'Email inserita non valida o non registrata' })




class StatisticheView(View):
    def get(self, request):

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        context = {
            'dottore' : dottore
        }

        return render(request, "includes/statistiche.html", context)
    



def safe_float(data, key, default=0.0):
    try:
        return float(data.get(key, default))
    except (ValueError, TypeError):
        return default




class CalcolatoreRender(View):
    
    def get(self, request):

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        context = {
            'dottore' : dottore
        }

        codice_fiscale = request.GET.get('parametro')

        if codice_fiscale:
            paziente = TabellaPazienti.objects.get(codice_fiscale=codice_fiscale)
            paziente_id = paziente.id

            context = {
                    "paziente": paziente,
                    "id_persona": paziente_id,
            }


            return render(request, 'includes/calcolatore.html', context)
        
        else:
            return render(request, 'includes/calcolatore.html', context)

        
    def post(self, request):
        data = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}
        dottore_id = request.session.get('dottore_id')

        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        try:
            # Controlla se esiste un paziente con lo stesso nome e cognome
            paziente = TabellaPazienti.objects.filter(
                codice_fiscale=data.get('codice_fiscale') 
            ).first()

            if paziente: 
                
                paziente_id = paziente.id

                campi_opzionali=[
                    'd_roms', 'osi', 'pat', 'my_acid', 'p_acid', 'st_acid', 'ar_acid', 'beenic_acid', 'pal_acid', 'ol_acid', 'ner_acid', 'a_linoleic_acid', 'eico_acid',
                    'doco_acid', 'lin_acid', 'gamma_lin_acid', 'dih_gamma_lin_acid', 'arachidonic_acid', 'sa_un_fatty_acid', 'o3o6_fatty_acid_quotient', 'aa_epa', 
                    'o3_index', 'wbc', 'baso', 'eosi', 'lymph', 'mono', 'neut', 'neut_ul', 'lymph_ul', 'mono_ul', 'eosi_ul', 'baso_ul', 'mch', 'mchc', 'mcv', 'rdwsd',
                    'rdwcv', 'hct_m', 'hct_w', 'hgb_m', 'hgb_w', 'rbc_m', 'rbc_w', 'azotemia', 'uric_acid', 'creatinine_m', 'creatinine_w', 'uricemy_m', 'uricemy_w',
                    'cistatine_c', 'plt', 'mpv', 'plcr', 'pct', 'pdw', 'd_dimero', 'pai_1', 'tot_chol', 'ldl_chol', 'hdl_chol_m', 'hdl_chol_w', 'trigl', 'na', 'k', 
                    'mg', 'ci', 'ca', 'p', 'dhea_m', 'dhea_w', 'testo_m', 'testo_w', 'tsh', 'ft3', 'ft4', 'beta_es_m', 'beta_es_w', 'prog_m', 'prog_w', 'fe', 'transferrin',
                    'ferritin_m', 'ferritin_w', 'glicemy', 'insulin', 'homa', 'ir', 'albuminemia', 'tot_prot', 'tot_prot_ele', 'albumin_ele', 'a_1', 'a_2', 'b_1', 'b_2',
                    'gamma', 'albumin_dI', 'a_1_dI', 'a_2_dI', 'b_1_dI', 'b_2_dI', 'gamma_dI', 'ag_rap', 'cm', 'b_2_spike', 'b_2_spike_m1', 'got_m', 'got_w', 'gpt_m', 'gpt_w',
                    'g_gt_m', 'g_gt_w', 'a_photo_m', 'a_photo_w', 'tot_bili', 'direct_bili', 'indirect_bili', 'ves', 'pcr_c', 's_weight',
                    'ph', 'proteins_ex', 'blood_ex', 'ketones', 'uro', 'bilirubin_ex', 'leuc', 'glucose', 'shbg_m', 'shbg_w', 'nt_pro', 'v_b12', 'v_d', 'ves2', 'telotest'
                ]

                # Verifica se almeno un campo opzionale è stato inserito
                if any(data.get(campo) for campo in campi_opzionali):


                    print('sono qui')
                    paziente_query = get_object_or_404(TabellaPazienti, id=paziente.id)

                    # Salva i dati del referto
                    referto = ArchivioReferti(
                        paziente=paziente_query,
                        descrizione=data.get('descrizione'),
                    )
                    referto.save()

                    # Estrai i dati necessari per la tabella DatiEstesiReferti
                    chronological_age = int(data.get('chronological_age'))

                    d_roms = safe_float(data, 'd_roms')
                    osi = safe_float(data, 'osi')
                    pat = safe_float(data, 'pat')

                    my_acid = safe_float(data, 'my_acid')
                    p_acid = safe_float(data, 'p_acid')
                    st_acid = safe_float(data, 'st_acid')
                    ar_acid = safe_float(data, 'ar_acid')
                    beenic_acid = safe_float(data, 'beenic_acid')
                    pal_acid = safe_float(data, 'pal_acid')
                    ol_acid = safe_float(data, 'ol_acid')
                    ner_acid = safe_float(data, 'ner_acid')
                    a_linoleic_acid = safe_float(data, 'a_linoleic_acid')
                    eico_acid = safe_float(data, 'eico_acid')
                    doco_acid = safe_float(data, 'doco_acid')
                    lin_acid = safe_float(data, 'lin_acid')
                    gamma_lin_acid = safe_float(data, 'gamma_lin_acid')
                    dih_gamma_lin_acid = safe_float(data, 'dih_gamma_lin_acid')
                    arachidonic_acid = safe_float(data, 'arachidonic_acid')
                    sa_un_fatty_acid = safe_float(data, 'sa_un_fatty_acid')
                    o3o6_fatty_acid_quotient =  safe_float(data, 'o3o6_fatty_acid_quotient')
                    aa_epa = safe_float(data, 'aa_epa ')
                    o3_index = safe_float(data, 'o3_index')

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

                    mch = safe_float(data, 'mch')
                    mchc = safe_float(data, 'mchc')
                    mcv = safe_float(data, 'mcv')
                    rdwsd = safe_float(data, 'rdwsd')
                    rdwcv = safe_float(data, 'rdwcv')
                    hct_m = safe_float(data, 'hct_m')
                    hct_w = safe_float(data, 'hct_w')
                    hgb_m = safe_float(data, 'hgb_m')
                    hgb_w = safe_float(data, 'hgb_w')
                    rbc_m = safe_float(data, 'rbc_m')
                    rbc_w = safe_float(data, 'rbc_w')

                    azotemia = safe_float(data, 'azotemia')
                    uric_acid = safe_float(data, 'uric_acid')
                    creatinine_m = safe_float(data, 'creatinine_m')
                    creatinine_w = safe_float(data, 'creatinine_w')
                    uricemy_m = safe_float(data, 'uricemy_m')
                    uricemy_w = safe_float(data, 'uricemy_w')
                    cistatine_c = safe_float(data, 'cistatine_c')

                    plt = safe_float(data, 'plt')
                    mpv = safe_float(data, 'mpv')
                    plcr = safe_float(data, 'plcr')
                    pct = safe_float(data, 'pct')
                    pdw = safe_float(data, 'pdw')
                    d_dimero = safe_float(data, 'd_dimero')
                    pai_1 = safe_float(data, 'pai_1')

                    tot_chol = safe_float(data, 'tot_chol')
                    ldl_chol = safe_float(data, 'ldl_chol')
                    hdl_chol_m = safe_float(data, 'hdl_chol_m')
                    hdl_chol_w = safe_float(data, 'hdl_chol_w')
                    trigl = safe_float(data, 'trigl')

                    na = safe_float(data, 'na')
                    k = safe_float(data, 'k')
                    mg = safe_float(data, 'mg')
                    ci = safe_float(data, 'ci')
                    ca = safe_float(data, 'ca')
                    p = safe_float(data, 'p')

                    dhea_m = safe_float(data, 'dhea_m')
                    dhea_w = safe_float(data, 'dhea_w')
                    testo_m = safe_float(data, 'testo_m')
                    testo_w = safe_float(data, 'testo_w')
                    tsh = safe_float(data, 'tsh')
                    ft3 = safe_float(data, 'ft3')
                    ft4 = safe_float(data, 'ft4')
                    beta_es_m = safe_float(data, 'beta_es_m')
                    beta_es_w = safe_float(data, 'beta_es_w')
                    prog_m = safe_float(data, 'prog_m')
                    prog_w = safe_float(data, 'prog_w')

                    fe = safe_float(data, 'fe')
                    transferrin = safe_float(data, 'transferrin')
                    ferritin_m = safe_float(data, 'ferritin_m')
                    ferritin_w = safe_float(data, 'ferritin_w')

                    glicemy = safe_float(data, 'glicemy')
                    insulin = safe_float(data, 'insulin')
                    homa = safe_float(data, 'homa')
                    ir = safe_float(data, 'ir')

                    albuminemia = safe_float(data, 'albuminemia')
                    tot_prot = safe_float(data, 'tot_prot')
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
              
                    got_m = safe_float(data, 'got_m')
                    got_w = safe_float(data, 'got_w')
                    gpt_m = safe_float(data, 'gpt_m')
                    gpt_w = safe_float(data, 'gpt_w')
                    g_gt_m = safe_float(data, 'g_gt_w')
                    g_gt_w = safe_float(data, 'g_gt_w')
                    a_photo_m = safe_float(data, 'a_photo_m')
                    a_photo_w = safe_float(data, 'a_photo_w')
                    tot_bili = safe_float(data, 'tot_bili')
                    direct_bili = safe_float(data, 'direct_bili')
                    indirect_bili = safe_float(data, 'indirect_bili')
                 
                    ves = safe_float(data, 'ves')
                    pcr_c = safe_float(data, 'pcr_c')

                    tnf_a = safe_float(data, 'tnf_a')
                    inter_6 = safe_float(data, 'inter_6')
                    inter_10 = safe_float(data, 'inter_10')

                    scatolo = safe_float(data, 'scatolo')
                    indicano = safe_float(data, 'indicano')

                    s_weight = safe_float(data, 's_weight')
                    ph = safe_float(data, 'ph')
                    proteins_ex = safe_float(data, 'proteins_ex')
                    blood_ex = safe_float(data, 'blood_ex')
                    ketones = safe_float(data, 'ketones')
                    uro = safe_float(data, 'uro')
                    bilirubin_ex = safe_float(data, 'bilirubin_ex')
                    leuc = safe_float(data, 'leuc')
                    glucose = safe_float(data, 'glucose')

                    shbg_m = safe_float(data, 'shbg_m')
                    shbg_w = safe_float(data, 'shbg_w')
                    nt_pro = safe_float(data, 'nt_pro')
                    v_b12 = safe_float(data, 'v_b12')
                    v_d = safe_float(data, 'v_d')
                    ves2 = safe_float(data, 'ves2')

                    telotest = safe_float(data, 'telotest')


                    exams = [
                            my_acid, p_acid, st_acid, ar_acid, beenic_acid, pal_acid, 
                            ol_acid, ner_acid, a_linoleic_acid, eico_acid, doco_acid, 
                            lin_acid, gamma_lin_acid, dih_gamma_lin_acid, arachidonic_acid, 
                            sa_un_fatty_acid, o3o6_fatty_acid_quotient, aa_epa, o3_index,
                            neut_ul, lymph_ul, mono_ul, eosi_ul, baso_ul, rdwcv, hct_w, 
                            hgb_w, rbc_w, azotemia, uric_acid, creatinine_m, creatinine_w, 
                            uricemy_m, uricemy_w, cistatine_c, plt, mpv, plcr, pct, pdw, 
                            d_dimero, pai_1, tot_chol, ldl_chol, hdl_chol_m, hdl_chol_w, 
                            trigl, na, k, mg, ci, ca, p, dhea_m, dhea_w, testo_m, 
                            testo_w, tsh, ft3, ft4, beta_es_m, beta_es_w, prog_m, prog_w, 
                            fe, transferrin, ferritin_m, ferritin_w, glicemy, insulin, homa, 
                            ir, albuminemia, tot_prot, tot_prot_ele, albumin_ele, a_1, a_2, 
                            b_1, b_2, gamma, albumin_dI, a_1_dI, a_2_dI, b_1_dI, b_2_dI, 
                            gamma_dI, ag_rap, cm, b_2_spike, b_2_spike_m1, got_m, got_w, 
                            gpt_m, gpt_w, g_gt_m, g_gt_w, a_photo_m, a_photo_w, tot_bili, 
                            direct_bili, indirect_bili, ves, pcr_c, tnf_a, inter_6, inter_10, 
                            scatolo, indicano, s_weight, ph, proteins_ex, blood_ex, ketones, 
                            uro, bilirubin_ex, leuc, glucose, shbg_m, shbg_w, nt_pro, v_b12, 
                            v_d, ves2, telotest
                        ]


                    # Calcolo dell'età biologica
                    biological_age = calculate_biological_age(
                        chronological_age, d_roms, osi, pat, wbc, baso,
                        eosi, lymph, mono, neut, rbc_m, hgb_m, 
                        hct_m, mcv, mch, mchc, rdwsd, exams
                    )

                    # Salvataggio dei dati
                    dati_estesi = DatiEstesiReferti(
                        referto=referto,

                        d_roms=d_roms,
                        osi=osi,
                        pat=pat,

                        my_acid=my_acid,
                        p_acid=p_acid,
                        st_acid=st_acid,
                        ar_acid=ar_acid,
                        beenic_acid=beenic_acid,
                        pal_acid=pal_acid,
                        ol_acid=ol_acid,
                        ner_acid=ner_acid,
                        a_linoleic_acid=a_linoleic_acid,
                        eico_acid=eico_acid,
                        doco_acid=doco_acid,
                        lin_acid=lin_acid,
                        gamma_lin_acid=gamma_lin_acid,
                        dih_gamma_lin_acid=dih_gamma_lin_acid,
                        arachidonic_acid=arachidonic_acid,
                        sa_un_fatty_acid=sa_un_fatty_acid,
                        o3o6_fatty_acid_quotient = o3o6_fatty_acid_quotient,
                        aa_epa = aa_epa,
                        o3_index = o3_index,

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

                        mch=mch,
                        mchc=mchc,
                        mcv=mcv,
                        rdwsd=rdwsd,
                        rdwcv=rdwcv,
                        hct_m=hct_m,
                        hct_w=hct_w,
                        hgb_m=hgb_m,
                        hgb_w=hgb_w,
                        rbc_m=rbc_m,
                        rbc_w=rbc_w,

                        azotemia=azotemia,
                        uric_acid=uric_acid,
                        creatinine_m=creatinine_m,
                        creatinine_w=creatinine_w,
                        uricemy_m=uricemy_m,
                        uricemy_w=uricemy_w,
                        cistatine_c=cistatine_c,

                        plt=plt,
                        mpv=mpv,
                        plcr=plcr,
                        pct=pct,
                        pdw=pdw,
                        d_dimero=d_dimero,
                        pai_1=pai_1,

                        tot_chol=tot_chol,
                        ldl_chol=ldl_chol,
                        hdl_chol_m=hdl_chol_m,
                        hdl_chol_w=hdl_chol_w,
                        trigl=trigl,

                        na=na,
                        k=k,
                        mg=mg,
                        ci=ci,
                        ca=ca,
                        p=p,

                        dhea_m=dhea_m,
                        dhea_w=dhea_w,
                        testo_m=testo_m,
                        testo_w=testo_w,
                        tsh=tsh,
                        ft3=ft3,
                        ft4=ft4,
                        beta_es_m=beta_es_m,
                        beta_es_w=beta_es_w,
                        prog_m=prog_m,
                        prog_w=prog_w,

                        fe=fe,
                        transferrin=transferrin,
                        ferritin_m=ferritin_m,
                        ferritin_w=ferritin_w,

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
                      
                        got_m=got_m,
                        got_w=got_w,
                        gpt_m=gpt_m,
                        gpt_w=gpt_w,
                        g_gt_m=g_gt_m,
                        g_gt_w = g_gt_w,    
                        a_photo_m=a_photo_m,
                        a_photo_w=a_photo_w,
                        tot_bili=tot_bili,
                        direct_bili=direct_bili,
                        indirect_bili=indirect_bili,
                       
                        ves=ves,
                        pcr_c=pcr_c,

                        tnf_a=tnf_a,
                        inter_6=inter_6,
                        inter_10=inter_10,

                        scatolo=scatolo,
                        indicano=indicano,

                        s_weight=s_weight,
                        ph=ph,
                        proteins_ex=proteins_ex,
                        blood_ex=blood_ex,
                        ketones=ketones,
                        uro=uro,
                        bilirubin_ex=bilirubin_ex,
                        leuc=leuc,
                        glucose=glucose,

                        shbg_m=shbg_m,
                        shbg_w=shbg_w,
                        nt_pro=nt_pro,
                        v_b12=v_b12,
                        v_d=v_d,
                        ves2=ves2,

                        telotest=telotest,

                        biological_age= biological_age,
                    )
                    dati_estesi.save()

                    # Context da mostrare nel template
                    context = {
                        "show_modal": True,
                        "biological_age": biological_age,
                        "data": data,
                        "id_persona": paziente_id,
                        'dottore': dottore
                    }

                    return render(request, "includes/calcolatore.html", context)
                
                else:
                    
                    context = {
                        "show_modal": False,
                        "error": "Operazione non andata a buon fine: 'Un Utente con questo Codice Fiscale è gia presente all'interno del database'. ",
                        "data": data,
                        'dottore': dottore
                    }
                    return render(request, "includes/calcolatore.html", context)

            else:

                campi_opzionali=[
                    'd_roms', 'osi', 'pat', 'my_acid', 'p_acid', 'st_acid', 'ar_acid', 'beenic_acid', 'pal_acid', 'ol_acid', 'ner_acid', 'a_linoleic_acid', 'eico_acid',
                    'doco_acid', 'lin_acid', 'gamma_lin_acid', 'dih_gamma_lin_acid', 'arachidonic_acid', 'sa_un_fatty_acid', 'o3o6_fatty_acid_quotient', 'aa_epa', 
                    'o3_index', 'wbc', 'baso', 'eosi', 'lymph', 'mono', 'neut', 'neut_ul', 'lymph_ul', 'mono_ul', 'eosi_ul', 'baso_ul', 'mch', 'mchc', 'mcv', 'rdwsd',
                    'rdwcv', 'hct_m', 'hct_w', 'hgb_m', 'hgb_w', 'rbc_m', 'rbc_w', 'azotemia', 'uric_acid', 'creatinine_m', 'creatinine_w', 'uricemy_m', 'uricemy_w',
                    'cistatine_c', 'plt', 'mpv', 'plcr', 'pct', 'pdw', 'd_dimero', 'pai_1', 'tot_chol', 'ldl_chol', 'hdl_chol_m', 'hdl_chol_w', 'trigl', 'na', 'k', 
                    'mg', 'ci', 'ca', 'p', 'dhea_m', 'dhea_w', 'testo_m', 'testo_w', 'tsh', 'ft3', 'ft4', 'beta_es_m', 'beta_es_w', 'prog_m', 'prog_w', 'fe', 'transferrin',
                    'ferritin_m', 'ferritin_w', 'glicemy', 'insulin', 'homa', 'ir', 'albuminemia', 'tot_prot', 'tot_prot_ele', 'albumin_ele', 'a_1', 'a_2', 'b_1', 'b_2',
                    'gamma', 'albumin_dI', 'a_1_dI', 'a_2_dI', 'b_1_dI', 'b_2_dI', 'gamma_dI', 'ag_rap', 'cm', 'b_2_spike', 'b_2_spike_m1', 'got_m', 'got_w', 'gpt_m', 'gpt_w',
                    'g_gt_m', 'g_gt_w', 'a_photo_m', 'a_photo_w', 'tot_bili', 'direct_bili', 'indirect_bili', 'ves', 'pcr_c', 's_weight',
                    'ph', 'proteins_ex', 'blood_ex', 'ketones', 'uro', 'bilirubin_ex', 'leuc', 'glucose', 'shbg_m', 'shbg_w', 'nt_pro', 'v_b12', 'v_d', 'ves2', 'telotest'
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
                        codice_fiscale=data.get('codice_fiscale'),
                        chronological_age = data.get('chronological_age')
                    )
                    paziente.save()


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
              
                    paziente = TabellaPazienti.objects.filter(
                        codice_fiscale=data.get('codice_fiscale') 
                    ).first()
    
                    
                    paziente_id = paziente.id

                    # Salva i dati del referto
                    referto = ArchivioReferti(
                        paziente=paziente,
                        descrizione=data.get('descrizione'),
                        documento=request.FILES.get('documento')
                    )
                    referto.save()

                    # Estrai i dati necessari per la tabella DatiEstesiReferti
                    chronological_age = int(data.get('chronological_age'))

                    d_roms = safe_float(data, 'd_roms')
                    osi = safe_float(data, 'osi')
                    pat = safe_float(data, 'pat')

                    my_acid = safe_float(data, 'my_acid')
                    p_acid = safe_float(data, 'p_acid')
                    st_acid = safe_float(data, 'st_acid')
                    ar_acid = safe_float(data, 'ar_acid')
                    beenic_acid = safe_float(data, 'beenic_acid')
                    pal_acid = safe_float(data, 'pal_acid')
                    ol_acid = safe_float(data, 'ol_acid')
                    ner_acid = safe_float(data, 'ner_acid')
                    a_linoleic_acid = safe_float(data, 'a_linoleic_acid')
                    eico_acid = safe_float(data, 'eico_acid')
                    doco_acid = safe_float(data, 'doco_acid')
                    lin_acid = safe_float(data, 'lin_acid')
                    gamma_lin_acid = safe_float(data, 'gamma_lin_acid')
                    dih_gamma_lin_acid = safe_float(data, 'dih_gamma_lin_acid')
                    arachidonic_acid = safe_float(data, 'arachidonic_acid')
                    sa_un_fatty_acid = safe_float(data, 'sa_un_fatty_acid')
                    o3o6_fatty_acid_quotient =  safe_float(data, 'o3o6_fatty_acid_quotient')
                    aa_epa = safe_float(data, 'aa_epa ')
                    o3_index = safe_float(data, 'o3_index')

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

                    mch = safe_float(data, 'mch')
                    mchc = safe_float(data, 'mchc')
                    mcv = safe_float(data, 'mcv')
                    rdwsd = safe_float(data, 'rdwsd')
                    rdwcv = safe_float(data, 'rdwcv')
                    hct_m = safe_float(data, 'hct_m')
                    hct_w = safe_float(data, 'hct_w')
                    hgb_m = safe_float(data, 'hgb_m')
                    hgb_w = safe_float(data, 'hgb_w')
                    rbc_m = safe_float(data, 'rbc_m')
                    rbc_w = safe_float(data, 'rbc_w')

                    azotemia = safe_float(data, 'azotemia')
                    uric_acid = safe_float(data, 'uric_acid')
                    creatinine_m = safe_float(data, 'creatinine_m')
                    creatinine_w = safe_float(data, 'creatinine_w')
                    uricemy_m = safe_float(data, 'uricemy_m')
                    uricemy_w = safe_float(data, 'uricemy_w')
                    cistatine_c = safe_float(data, 'cistatine_c')

                    plt = safe_float(data, 'plt')
                    mpv = safe_float(data, 'mpv')
                    plcr = safe_float(data, 'plcr')
                    pct = safe_float(data, 'pct')
                    pdw = safe_float(data, 'pdw')
                    d_dimero = safe_float(data, 'd_dimero')
                    pai_1 = safe_float(data, 'pai_1')

                    tot_chol = safe_float(data, 'tot_chol')
                    ldl_chol = safe_float(data, 'ldl_chol')
                    hdl_chol_m = safe_float(data, 'hdl_chol_m')
                    hdl_chol_w = safe_float(data, 'hdl_chol_w')
                    trigl = safe_float(data, 'trigl')

                    na = safe_float(data, 'na')
                    k = safe_float(data, 'k')
                    mg = safe_float(data, 'mg')
                    ci = safe_float(data, 'ci')
                    ca = safe_float(data, 'ca')
                    p = safe_float(data, 'p')

                    dhea_m = safe_float(data, 'dhea_m')
                    dhea_w = safe_float(data, 'dhea_w')
                    testo_m = safe_float(data, 'testo_m')
                    testo_w = safe_float(data, 'testo_w')
                    tsh = safe_float(data, 'tsh')
                    ft3 = safe_float(data, 'ft3')
                    ft4 = safe_float(data, 'ft4')
                    beta_es_m = safe_float(data, 'beta_es_m')
                    beta_es_w = safe_float(data, 'beta_es_w')
                    prog_m = safe_float(data, 'prog_m')
                    prog_w = safe_float(data, 'prog_w')

                    fe = safe_float(data, 'fe')
                    transferrin = safe_float(data, 'transferrin')
                    ferritin_m = safe_float(data, 'ferritin_m')
                    ferritin_w = safe_float(data, 'ferritin_w')

                    glicemy = safe_float(data, 'glicemy')
                    insulin = safe_float(data, 'insulin')
                    homa = safe_float(data, 'homa')
                    ir = safe_float(data, 'ir')

                    albuminemia = safe_float(data, 'albuminemia')
                    tot_prot = safe_float(data, 'tot_prot')
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
              
                    got_m = safe_float(data, 'got_m')
                    got_w = safe_float(data, 'got_w')
                    gpt_m = safe_float(data, 'gpt_m')
                    gpt_w = safe_float(data, 'gpt_w')
                    g_gt_m = safe_float(data, 'g_gt_w')
                    g_gt_w = safe_float(data, 'g_gt_w')
                    a_photo_m = safe_float(data, 'a_photo_m')
                    a_photo_w = safe_float(data, 'a_photo_w')
                    tot_bili = safe_float(data, 'tot_bili')
                    direct_bili = safe_float(data, 'direct_bili')
                    indirect_bili = safe_float(data, 'indirect_bili')
                 
                    ves = safe_float(data, 'ves')
                    pcr_c = safe_float(data, 'pcr_c')

                    tnf_a = safe_float(data, 'tnf_a')
                    inter_6 = safe_float(data, 'inter_6')
                    inter_10 = safe_float(data, 'inter_10')

                    scatolo = safe_float(data, 'scatolo')
                    indicano = safe_float(data, 'indicano')

                    s_weight = safe_float(data, 's_weight')
                    ph = safe_float(data, 'ph')
                    proteins_ex = safe_float(data, 'proteins_ex')
                    blood_ex = safe_float(data, 'blood_ex')
                    ketones = safe_float(data, 'ketones')
                    uro = safe_float(data, 'uro')
                    bilirubin_ex = safe_float(data, 'bilirubin_ex')
                    leuc = safe_float(data, 'leuc')
                    glucose = safe_float(data, 'glucose')

                    shbg_m = safe_float(data, 'shbg_m')
                    shbg_w = safe_float(data, 'shbg_w')
                    nt_pro = safe_float(data, 'nt_pro')
                    v_b12 = safe_float(data, 'v_b12')
                    v_d = safe_float(data, 'v_d')
                    ves2 = safe_float(data, 'ves2')

                    telotest = safe_float(data, 'telotest')

                    exams = [
                            my_acid, p_acid, st_acid, ar_acid, beenic_acid, pal_acid, 
                            ol_acid, ner_acid, a_linoleic_acid, eico_acid, doco_acid, 
                            lin_acid, gamma_lin_acid, dih_gamma_lin_acid, arachidonic_acid, 
                            sa_un_fatty_acid, o3o6_fatty_acid_quotient, aa_epa, o3_index,
                            neut_ul, lymph_ul, mono_ul, eosi_ul, baso_ul, rdwcv, hct_w, 
                            hgb_w, rbc_w, azotemia, uric_acid, creatinine_m, creatinine_w, 
                            uricemy_m, uricemy_w, cistatine_c, plt, mpv, plcr, pct, pdw, 
                            d_dimero, pai_1, tot_chol, ldl_chol, hdl_chol_m, hdl_chol_w, 
                            trigl, na, k, mg, ci, ca, p, dhea_m, dhea_w, testo_m, 
                            testo_w, tsh, ft3, ft4, beta_es_m, beta_es_w, prog_m, prog_w, 
                            fe, transferrin, ferritin_m, ferritin_w, glicemy, insulin, homa, 
                            ir, albuminemia, tot_prot, tot_prot_ele, albumin_ele, a_1, a_2, 
                            b_1, b_2, gamma, albumin_dI, a_1_dI, a_2_dI, b_1_dI, b_2_dI, 
                            gamma_dI, ag_rap, cm, b_2_spike, b_2_spike_m1, got_m, got_w, 
                            gpt_m, gpt_w, g_gt_m, g_gt_w, a_photo_m, a_photo_w, tot_bili, 
                            direct_bili, indirect_bili, ves, pcr_c, tnf_a, inter_6, inter_10, 
                            scatolo, indicano, s_weight, ph, proteins_ex, blood_ex, ketones, 
                            uro, bilirubin_ex, leuc, glucose, shbg_m, shbg_w, nt_pro, v_b12, 
                            v_d, ves2, telotest
                        ]

                    # Calcolo dell'età biologica
                    biological_age = calculate_biological_age(
                        chronological_age, d_roms, osi, pat, wbc, baso,
                        eosi, lymph, mono, neut, rbc_m, hgb_m, 
                        hct_m, mcv, mch, mchc, rdwsd, exams
                    )

                    # Salvataggio dei dati
                    dati_estesi = DatiEstesiReferti(
                        referto=referto,

                        d_roms=d_roms,
                        osi=osi,
                        pat=pat,

                        my_acid=my_acid,
                        p_acid=p_acid,
                        st_acid=st_acid,
                        ar_acid=ar_acid,
                        beenic_acid=beenic_acid,
                        pal_acid=pal_acid,
                        ol_acid=ol_acid,
                        ner_acid=ner_acid,
                        a_linoleic_acid=a_linoleic_acid,
                        eico_acid=eico_acid,
                        doco_acid=doco_acid,
                        lin_acid=lin_acid,
                        gamma_lin_acid=gamma_lin_acid,
                        dih_gamma_lin_acid=dih_gamma_lin_acid,
                        arachidonic_acid=arachidonic_acid,
                        sa_un_fatty_acid=sa_un_fatty_acid,
                        o3o6_fatty_acid_quotient = o3o6_fatty_acid_quotient,
                        aa_epa = aa_epa,
                        o3_index = o3_index,

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

                        mch=mch,
                        mchc=mchc,
                        mcv=mcv,
                        rdwsd=rdwsd,
                        rdwcv=rdwcv,
                        hct_m=hct_m,
                        hct_w=hct_w,
                        hgb_m=hgb_m,
                        hgb_w=hgb_w,
                        rbc_m=rbc_m,
                        rbc_w=rbc_w,

                        azotemia=azotemia,
                        uric_acid=uric_acid,
                        creatinine_m=creatinine_m,
                        creatinine_w=creatinine_w,
                        uricemy_m=uricemy_m,
                        uricemy_w=uricemy_w,
                        cistatine_c=cistatine_c,

                        plt=plt,
                        mpv=mpv,
                        plcr=plcr,
                        pct=pct,
                        pdw=pdw,
                        d_dimero=d_dimero,
                        pai_1=pai_1,

                        tot_chol=tot_chol,
                        ldl_chol=ldl_chol,
                        hdl_chol_m=hdl_chol_m,
                        hdl_chol_w=hdl_chol_w,
                        trigl=trigl,

                        na=na,
                        k=k,
                        mg=mg,
                        ci=ci,
                        ca=ca,
                        p=p,

                        dhea_m=dhea_m,
                        dhea_w=dhea_w,
                        testo_m=testo_m,
                        testo_w=testo_w,
                        tsh=tsh,
                        ft3=ft3,
                        ft4=ft4,
                        beta_es_m=beta_es_m,
                        beta_es_w=beta_es_w,
                        prog_m=prog_m,
                        prog_w=prog_w,

                        fe=fe,
                        transferrin=transferrin,
                        ferritin_m=ferritin_m,
                        ferritin_w=ferritin_w,

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
                      
                        got_m=got_m,
                        got_w=got_w,
                        gpt_m=gpt_m,
                        gpt_w=gpt_w,
                        g_gt_m=g_gt_m,
                        g_gt_w = g_gt_w,    
                        a_photo_m=a_photo_m,
                        a_photo_w=a_photo_w,
                        tot_bili=tot_bili,
                        direct_bili=direct_bili,
                        indirect_bili=indirect_bili,
                       
                        ves=ves,
                        pcr_c=pcr_c,

                        tnf_a=tnf_a,
                        inter_6=inter_6,
                        inter_10=inter_10,

                        scatolo=scatolo,
                        indicano=indicano,

                        s_weight=s_weight,
                        ph=ph,
                        proteins_ex=proteins_ex,
                        blood_ex=blood_ex,
                        ketones=ketones,
                        uro=uro,
                        bilirubin_ex=bilirubin_ex,
                        leuc=leuc,
                        glucose=glucose,

                        shbg_m=shbg_m,
                        shbg_w=shbg_w,
                        nt_pro=nt_pro,
                        v_b12=v_b12,
                        v_d=v_d,
                        ves2=ves2,
                        
                        telotest=telotest,

                        biological_age= biological_age,
                    )
                    dati_estesi.save()
                
                # Context da mostrare nel template
                context = {
                    "show_modal": True,
                    "biological_age": biological_age,
                    "data": data,
                    "id_persona": paziente_id,
                    'dottore' : dottore,
                }

                return render(request, "includes/calcolatore.html", context)

        except Exception as e:
    
            context = {
                "error": "system error: " + str(e) + " --- Controlla di aver inserito tutti i dati corretti nei campi necessari e riprova.",
            }
            return render(request, "includes/calcolatore.html", context)




class RisultatiRender(View):
    def get(self, request):
        persone = TabellaPazienti.objects.all()
        
        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)
 
        # Ottieni il referto più recente per ogni paziente
        ultimo_referto = ArchivioReferti.objects.filter(paziente=OuterRef('referto__paziente')).order_by('-data_referto')

        # Ottieni i dati estesi associati al referto più recente di ciascun paziente
        datiEstesi = DatiEstesiReferti.objects.filter(referto=Subquery(ultimo_referto.values('id')[:1]))

        context = {
            'persone': persone,
            'datiEstesi': datiEstesi,
            'dottore' : dottore
        }

        return render(request, "includes/risultati.html", context)




class PersonaDetailView(View):
   
    def get(self, request, id):
        persona = get_object_or_404(TabellaPazienti, id=id)

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        ultimo_referto = ArchivioReferti.objects.filter(paziente=persona).order_by('-data_ora_creazione').first()

        datiEstesi = None
        if ultimo_referto:
            datiEstesi = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()

        context = {
            'persona': persona,
            'ultimo_referto': ultimo_referto,
            'datiEstesi': datiEstesi,
            'dottore' : dottore
        }
        return render(request, "includes/Referto.html", context)




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

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        # Ottieni i dati estesi dell'ultimo referto
        dati_estesi_ultimo_referto = None
        if ultimo_referto:
            dati_estesi_ultimo_referto = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()

        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            'ultimo_referto': ultimo_referto,
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto,
            'dottore' : dottore
        }

        return render(request, "includes/cartellaPaziente.html", context)




class DatiBaseView(View):

    def get(self, request, id):
        persona = get_object_or_404(TabellaPazienti, id=id)

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        context = {
            'persona': persona,
            'dottore' : dottore
        }
        return render(request, "includes/dati_base.html", context)
    
    def post(self,request, id): 

        persona = get_object_or_404(TabellaPazienti, id=id)

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        context = {
            'persona': persona,
            'dottore' : dottore
        }

        return render(request, "includes/dati_base.html", context)


    
class InserisciPazienteView(View):

    def get(self, request):

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        context = {
            'dottore' : dottore
        }

        return render(request, "includes/InserisciPaziente.html", context)
    

    def post(self, request):
        dottore = request.user.utentiregistraticredenziali if hasattr(request.user, 'utentiregistraticredenziali') else None
        codice_fiscale = request.POST.get('codice_fiscale')

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)


        paziente_esistente = TabellaPazienti.objects.filter(codice_fiscale=codice_fiscale).first()

        def parse_date(date_str):
            return date_str if date_str else None

        if paziente_esistente:

            paziente_esistente.height = request.POST.get('height')
            paziente_esistente.weight = request.POST.get('weight')
            paziente_esistente.bmi = request.POST.get('bmi')
            paziente_esistente.bmi_detection_date = parse_date(request.POST.get('bmi_detection_date'))


            paziente_esistente.girth_value = request.POST.get('girth_value')
            paziente_esistente.girth_notes = request.POST.get('girth_notes')
            paziente_esistente.girth_date = parse_date(request.POST.get('girth_date'))

    
            paziente_esistente.alcol = request.POST.get('alcol') 
            paziente_esistente.alcol_type = request.POST.get('alcol_type')
            paziente_esistente.data_alcol = parse_date(request.POST.get('data_alcol'))
            paziente_esistente.alcol_frequency = request.POST.get('alcol_frequency')

    
            paziente_esistente.smoke = request.POST.get('smoke') 
            paziente_esistente.smoke_frequency = request.POST.get('smoke_frequency')
            paziente_esistente.reduced_intake = request.POST.get('reduced_intake')

            paziente_esistente.sport = request.POST.get('sport') 
            paziente_esistente.sport_livello = request.POST.get('sport_livello')
            paziente_esistente.sport_frequency = request.POST.get('sport_frequency')

            paziente_esistente.attivita_sedentaria = request.POST.get('attivita_sedentaria')
            paziente_esistente.livello_sedentarieta = request.POST.get('livello_sedentarieta')
            paziente_esistente.sedentarieta_nota = request.POST.get('sedentarieta_nota')
           

            paziente_esistente.save()
            success = "I dati del paziente sono stati aggiornati con successo!"
    
        else:
            # Creazione di un nuovo paziente con la stessa gestione per le date
            TabellaPazienti.objects.create(
                dottore=dottore,
                name=request.POST.get('name'),
                surname=request.POST.get('surname'),
                dob=parse_date(request.POST.get('dob')),
                gender=request.POST.get('gender'),
                place_of_birth=request.POST.get('place_of_birth'),
                codice_fiscale=codice_fiscale,
                chronological_age=request.POST.get('chronological_age'),

                # Dati antropometrici
                height=request.POST.get('height'),
                weight=request.POST.get('weight'),
                bmi=request.POST.get('bmi'),
                bmi_detection_date=parse_date(request.POST.get('bmi_detection_date')),

                # Circonferenza addominale
                girth_value=request.POST.get('girth_value'),
                girth_notes=request.POST.get('girth_notes'),
                girth_date=parse_date(request.POST.get('girth_date')),

                # Alcol
                alcol=request.POST.get('alcol') == 'on',
                alcol_type=request.POST.get('alcol_type'),
                data_alcol=parse_date(request.POST.get('data_alcol')),
                alcol_frequency=request.POST.get('alcol_frequency'),

                # Fumo
                smoke=request.POST.get('smoke') == 'on',
                smoke_frequency=request.POST.get('smoke_frequency'),
                reduced_intake=request.POST.get('reduced_intake'),

                # Sport
                sport=request.POST.get('sport') == 'on',
                sport_livello=request.POST.get('sport_livello'),
                sport_frequency=request.POST.get('sport_frequency'),

                # Sedentarietà
                attivita_sedentaria=request.POST.get('attivita_sedentaria') == 'on',
                livello_sedentarieta=request.POST.get('livello_sedentarieta'),
                sedentarieta_nota=request.POST.get('sedentarieta_nota'),
            )
            
            success = "Nuovo paziente salvato con successo!"

        context = {
            "success": success, 
            'dottore' : dottore
        }

        return render(request, "includes/InserisciPaziente.html", context)



class ComposizioneView(View):

    def get(self, request, id):

        persona = get_object_or_404(TabellaPazienti, id=id)

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        context = {
            'persona': persona,
            'dottore' : dottore
        }

        return render(request, "includes/composizione.html", context)
    