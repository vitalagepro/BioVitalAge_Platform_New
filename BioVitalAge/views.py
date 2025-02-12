from datetime import date, datetime
from xml.etree.ElementInclude import include
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import *
from .utils import calculate_biological_age, calcola_punteggio_finale
import json
from django.db.models import OuterRef, Subquery
from django.views.decorators.csrf import csrf_exempt
from .models import TabellaPazienti, ArchivioReferti
import os
from django.http import JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator
import traceback
from django.shortcuts import redirect
from django.http import FileResponse

# Create your views here.


class LoginRenderingPage(View):
    def get(self, request):
        response = render(request, 'includes/login.html')
        response.delete_cookie('disclaimer_accepted', path='/')
        return response


class LogOutRender(View):
    def get(self, request):

        if 'dottore_id' in request.session:
            del request.session['dottore_id']

            request.session.flush()

        return render(request, 'includes/login.html')



# View per la homepage
class HomePageRender(View):

    def get(self, request):
        persone = TabellaPazienti.objects.all().order_by('-id')[:5]
        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        # Calcolo di show_disclaimer
        show_disclaimer = not request.COOKIES.get('disclaimer_accepted', False)

        context = {
            'persone': persone,
            'dottore': dottore,
            'show_disclaimer': show_disclaimer  # Passa lo stato del disclaimer
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

                            # Ottieni i 5 pazienti più recenti
                            persone = TabellaPazienti.objects.all().order_by('-id')[:5]
            
                            # Ottieni il referto più recente per ogni paziente
                            ultimo_referto = ArchivioReferti.objects.filter(paziente=OuterRef('referto__paziente')).order_by('-data_referto')

                            # Ottieni i dati estesi associati al referto più recente di ciascun paziente
                            datiEstesi = DatiEstesiReferti.objects.filter(referto=Subquery(ultimo_referto.values('id')[:1]))

                            # Funzione helper per convertire i dati JSON-serializzabili
                            def make_json_serializable(data):
                                if isinstance(data, list):
                                    return [make_json_serializable(item) for item in data]
                                elif isinstance(data, dict):
                                    return {key: make_json_serializable(value) for key, value in data.items()}
                                elif isinstance(data, date):
                                    return data.isoformat()  # Converte le date in stringhe
                                return data

                            # Prepara il contesto e lo salva in sessione
                            context = {
                                'persone': make_json_serializable(list(persone.values())),
                                'datiEstesi': make_json_serializable(list(datiEstesi.values())),
                                'dottore': dottore.id  # Questo è un intero, già JSON-serializzabile
                            }
                            
                            request.session['home_context'] = context

                            # Reindirizza alla homepage
                            response = redirect('HomePage')
                            response.delete_cookie('disclaimer_accepted')
                            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                            response['Pragma'] = 'no-cache'
                            return response

                        else:
                            return render(request, 'includes/login.html', {'error': 'Password errata'})
                        
                    else:
                        return render(request, 'includes/login.html', {'error': 'Email inserita non valida o non registrata'})

# View per accettare il disclaimer
class AcceptDisclaimerView(View):
    def post(self, request):
        # Restituisce una risposta JSON
        response = JsonResponse({"success": True})
        # Imposta un cookie per indicare che il disclaimer è stato accettato
        response.set_cookie('disclaimer_accepted', 'true', max_age=365*24*60*60)  # 1 anno
        return response



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
            try:
                paziente = TabellaPazienti.objects.get(codice_fiscale=codice_fiscale)
                context.update({
                    "paziente": paziente,
                    "id_persona": paziente.id
                })
            except TabellaPazienti.DoesNotExist:
                context.update({"error": "Paziente non trovato."})

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
                    'gamma', 'albumin_dI', 'a_1_dI', 'a_2_dI', 'b_1_dI', 'b_2_dI', 'gamma_dI', 'ag_rap', 'got_m', 'got_w', 'gpt_m', 'gpt_w',
                    'g_gt_m', 'g_gt_w', 'a_photo_m', 'a_photo_w', 'tot_bili', 'direct_bili', 'indirect_bili', 'ves', 'pcr_c', 's_weight',
                    'ph', 'proteins_ex', 'blood_ex', 'ketones', 'uro', 'bilirubin_ex', 'leuc', 'glucose', 'shbg_m', 'shbg_w', 'nt_pro', 'v_b12', 'v_d', 'ves2', 'telotest'
                ]

                # Verifica se almeno un campo opzionale è stato inserito
                if any(data.get(campo) for campo in campi_opzionali):

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

                    exams = []

                    if paziente.gender == 'M':

                        exams = [
                            {'my_acid': my_acid}, {'p_acid': p_acid}, {'st_acid': st_acid}, {'ar_acid': ar_acid},
                            {'beenic_acid': beenic_acid}, {'pal_acid': pal_acid}, {'ol_acid': ol_acid}, {'ner_acid': ner_acid},
                            {'a_linoleic_acid': a_linoleic_acid}, {'eico_acid': eico_acid}, {'doco_acid': doco_acid}, {'lin_acid': lin_acid},
                            {'gamma_lin_acid': gamma_lin_acid}, {'dih_gamma_lin_acid': dih_gamma_lin_acid}, {'arachidonic_acid': arachidonic_acid},
                            {'sa_un_fatty_acid': sa_un_fatty_acid}, {'o3o6_fatty_acid_quotient': o3o6_fatty_acid_quotient}, {'aa_epa': aa_epa},
                            {'o3_index': o3_index}, {'neut_ul': neut_ul}, {'lymph_ul': lymph_ul}, {'mono_ul': mono_ul}, {'eosi_ul': eosi_ul},
                            {'baso_ul': baso_ul}, {'rdwcv': rdwcv}, {'hct_m': hct_m}, {'hgb_m': hgb_m}, {'rbc_m': rbc_m}, {'azotemia': azotemia},
                            {'uric_acid': uric_acid}, {'creatinine_m': creatinine_m}, {'uricemy_m': uricemy_m}, {'cistatine_c': cistatine_c},
                            {'plt': plt}, {'mpv': mpv}, {'plcr': plcr}, {'pct': pct}, {'pdw': pdw}, {'d_dimero': d_dimero}, {'pai_1': pai_1},
                            {'tot_chol': tot_chol}, {'ldl_chol': ldl_chol}, {'hdl_chol_m': hdl_chol_m}, {'trigl': trigl}, {'na': na}, {'k': k},
                            {'mg': mg}, {'ci': ci}, {'ca': ca}, {'p': p}, {'dhea_m': dhea_m}, {'testo_m': testo_m}, {'tsh': tsh}, {'ft3': ft3},
                            {'ft4': ft4}, {'beta_es_m': beta_es_m}, {'prog_m': prog_m}, {'fe': fe}, {'transferrin': transferrin},
                            {'ferritin_m': ferritin_m}, {'glicemy': glicemy}, {'insulin': insulin}, {'homa': homa}, {'ir': ir},
                            {'albuminemia': albuminemia}, {'tot_prot': tot_prot}, {'tot_prot_ele': tot_prot_ele}, {'albumin_ele': albumin_ele},
                            {'a_1': a_1}, {'a_2': a_2}, {'b_1': b_1}, {'b_2': b_2}, {'gamma': gamma}, {'albumin_dI': albumin_dI},
                            {'a_1_dI': a_1_dI}, {'a_2_dI': a_2_dI}, {'b_1_dI': b_1_dI}, {'b_2_dI': b_2_dI}, {'gamma_dI': gamma_dI},
                            {'ag_rap': ag_rap}, {'got_m': got_m}, {'gpt_m': gpt_m}, {'g_gt_m': g_gt_m}, {'a_photo_m': a_photo_m},
                            {'tot_bili': tot_bili}, {'direct_bili': direct_bili}, {'indirect_bili': indirect_bili}, {'ves': ves},
                            {'pcr_c': pcr_c}, {'tnf_a': tnf_a}, {'inter_6': inter_6}, {'inter_10': inter_10}, {'scatolo': scatolo},
                            {'indicano': indicano}, {'s_weight': s_weight}, {'ph': ph}, {'proteins_ex': proteins_ex}, {'blood_ex': blood_ex},
                            {'ketones': ketones}, {'uro': uro}, {'bilirubin_ex': bilirubin_ex}, {'leuc': leuc}, {'glucose': glucose},
                            {'shbg_m': shbg_m}, {'nt_pro': nt_pro}, {'v_b12': v_b12}, {'v_d': v_d}, {'ves2': ves2}, {'telotest': telotest}
                        ]

                    if paziente.gender == 'F':
                        
                        exams = [
                            {'my_acid': my_acid}, {'p_acid': p_acid}, {'st_acid': st_acid}, {'ar_acid': ar_acid},
                            {'beenic_acid': beenic_acid}, {'pal_acid': pal_acid}, {'ol_acid': ol_acid}, {'ner_acid': ner_acid},
                            {'a_linoleic_acid': a_linoleic_acid}, {'eico_acid': eico_acid}, {'doco_acid': doco_acid}, {'lin_acid': lin_acid},
                            {'gamma_lin_acid': gamma_lin_acid}, {'dih_gamma_lin_acid': dih_gamma_lin_acid}, {'arachidonic_acid': arachidonic_acid},
                            {'sa_un_fatty_acid': sa_un_fatty_acid}, {'o3o6_fatty_acid_quotient': o3o6_fatty_acid_quotient}, {'aa_epa': aa_epa},
                            {'o3_index': o3_index}, {'neut_ul': neut_ul}, {'lymph_ul': lymph_ul}, {'mono_ul': mono_ul}, {'eosi_ul': eosi_ul},
                            {'baso_ul': baso_ul}, {'rdwcv': rdwcv}, {'hct_w': hct_w}, {'hgb_w': hgb_w}, {'rbc_w': rbc_w}, {'azotemia': azotemia},
                            {'uric_acid': uric_acid}, {'creatinine_w': creatinine_w}, {'uricemy_w': uricemy_w}, {'cistatine_c': cistatine_c},
                            {'plt': plt}, {'mpv': mpv}, {'plcr': plcr}, {'pct': pct}, {'pdw': pdw}, {'d_dimero': d_dimero}, {'pai_1': pai_1},
                            {'tot_chol': tot_chol}, {'ldl_chol': ldl_chol}, {'hdl_chol_w': hdl_chol_w}, {'trigl': trigl}, {'na': na}, {'k': k},
                            {'mg': mg}, {'ci': ci}, {'ca': ca}, {'p': p}, {'dhea_w': dhea_w}, {'testo_w': testo_w}, {'tsh': tsh}, {'ft3': ft3},
                            {'ft4': ft4}, {'beta_es_w': beta_es_w}, {'prog_w': prog_w}, {'fe': fe}, {'transferrin': transferrin},
                            {'ferritin_w': ferritin_w}, {'glicemy': glicemy}, {'insulin': insulin}, {'homa': homa}, {'ir': ir},
                            {'albuminemia': albuminemia}, {'tot_prot': tot_prot}, {'tot_prot_ele': tot_prot_ele}, {'albumin_ele': albumin_ele},
                            {'a_1': a_1}, {'a_2': a_2}, {'b_1': b_1}, {'b_2': b_2}, {'gamma': gamma}, {'albumin_dI': albumin_dI},
                            {'a_1_dI': a_1_dI}, {'a_2_dI': a_2_dI}, {'b_1_dI': b_1_dI}, {'b_2_dI': b_2_dI}, {'gamma_dI': gamma_dI},
                            {'ag_rap': ag_rap}, {'got_w': got_w}, {'gpt_w': gpt_w}, {'g_gt_w': g_gt_w}, {'a_photo_w': a_photo_w},
                            {'tot_bili': tot_bili}, {'direct_bili': direct_bili}, {'indirect_bili': indirect_bili}, {'ves': ves},
                            {'pcr_c': pcr_c}, {'tnf_a': tnf_a}, {'inter_6': inter_6}, {'inter_10': inter_10}, {'scatolo': scatolo},
                            {'indicano': indicano}, {'s_weight': s_weight}, {'ph': ph}, {'proteins_ex': proteins_ex}, {'blood_ex': blood_ex},
                            {'ketones': ketones}, {'uro': uro}, {'bilirubin_ex': bilirubin_ex}, {'leuc': leuc}, {'glucose': glucose},
                            {'shbg_w': shbg_w}, {'nt_pro': nt_pro}, {'v_b12': v_b12}, {'v_d': v_d}, {'ves2': ves2}, {'telotest': telotest}
                        ]

  
                    # Calcolo dell'età biologica
                    biological_age = calculate_biological_age(
                        chronological_age, d_roms = d_roms, osi = osi, pat = pat, wbc = wbc, basophils = baso_ul,
                        eosinophils = eosi, lymphocytes = lymph, monocytes = mono, neutrophils = neut, rbc = rbc_m, hgb = hgb_m, 
                        hct = hct_m, mcv = mcv, mch = mch, mchc = mchc, rdw = rdwsd, exams = exams, gender=paziente.gender
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
                    'gamma', 'albumin_dI', 'a_1_dI', 'a_2_dI', 'b_1_dI', 'b_2_dI', 'gamma_dI', 'ag_rap', 'got_m', 'got_w', 'gpt_m', 'gpt_w',
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
                        chronological_age = data.get('chronological_age'),
                        province = data.get('province')
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
                        province = data.get('province')
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


                    exams = []

                    if paziente.gender == 'M':

                        exams = [
                            {'my_acid': my_acid}, {'p_acid': p_acid}, {'st_acid': st_acid}, {'ar_acid': ar_acid},
                            {'beenic_acid': beenic_acid}, {'pal_acid': pal_acid}, {'ol_acid': ol_acid}, {'ner_acid': ner_acid},
                            {'a_linoleic_acid': a_linoleic_acid}, {'eico_acid': eico_acid}, {'doco_acid': doco_acid}, {'lin_acid': lin_acid},
                            {'gamma_lin_acid': gamma_lin_acid}, {'dih_gamma_lin_acid': dih_gamma_lin_acid}, {'arachidonic_acid': arachidonic_acid},
                            {'sa_un_fatty_acid': sa_un_fatty_acid}, {'o3o6_fatty_acid_quotient': o3o6_fatty_acid_quotient}, {'aa_epa': aa_epa},
                            {'o3_index': o3_index}, {'neut_ul': neut_ul}, {'lymph_ul': lymph_ul}, {'mono_ul': mono_ul}, {'eosi_ul': eosi_ul},
                            {'baso_ul': baso_ul}, {'rdwcv': rdwcv}, {'hct_m': hct_m}, {'hgb_m': hgb_m}, {'rbc_m': rbc_m}, {'azotemia': azotemia},
                            {'uric_acid': uric_acid}, {'creatinine_m': creatinine_m}, {'uricemy_m': uricemy_m}, {'cistatine_c': cistatine_c},
                            {'plt': plt}, {'mpv': mpv}, {'plcr': plcr}, {'pct': pct}, {'pdw': pdw}, {'d_dimero': d_dimero}, {'pai_1': pai_1},
                            {'tot_chol': tot_chol}, {'ldl_chol': ldl_chol}, {'hdl_chol_m': hdl_chol_m}, {'trigl': trigl}, {'na': na}, {'k': k},
                            {'mg': mg}, {'ci': ci}, {'ca': ca}, {'p': p}, {'dhea_m': dhea_m}, {'testo_m': testo_m}, {'tsh': tsh}, {'ft3': ft3},
                            {'ft4': ft4}, {'beta_es_m': beta_es_m}, {'prog_m': prog_m}, {'fe': fe}, {'transferrin': transferrin},
                            {'ferritin_m': ferritin_m}, {'glicemy': glicemy}, {'insulin': insulin}, {'homa': homa}, {'ir': ir},
                            {'albuminemia': albuminemia}, {'tot_prot': tot_prot}, {'tot_prot_ele': tot_prot_ele}, {'albumin_ele': albumin_ele},
                            {'a_1': a_1}, {'a_2': a_2}, {'b_1': b_1}, {'b_2': b_2}, {'gamma': gamma}, {'albumin_dI': albumin_dI},
                            {'a_1_dI': a_1_dI}, {'a_2_dI': a_2_dI}, {'b_1_dI': b_1_dI}, {'b_2_dI': b_2_dI}, {'gamma_dI': gamma_dI},
                            {'ag_rap': ag_rap}, {'got_m': got_m}, {'gpt_m': gpt_m}, {'g_gt_m': g_gt_m}, {'a_photo_m': a_photo_m},
                            {'tot_bili': tot_bili}, {'direct_bili': direct_bili}, {'indirect_bili': indirect_bili}, {'ves': ves},
                            {'pcr_c': pcr_c}, {'tnf_a': tnf_a}, {'inter_6': inter_6}, {'inter_10': inter_10}, {'scatolo': scatolo},
                            {'indicano': indicano}, {'s_weight': s_weight}, {'ph': ph}, {'proteins_ex': proteins_ex}, {'blood_ex': blood_ex},
                            {'ketones': ketones}, {'uro': uro}, {'bilirubin_ex': bilirubin_ex}, {'leuc': leuc}, {'glucose': glucose},
                            {'shbg_m': shbg_m}, {'nt_pro': nt_pro}, {'v_b12': v_b12}, {'v_d': v_d}, {'ves2': ves2}, {'telotest': telotest}
                        ]

                    if paziente.gender == 'F':
                        
                        exams = [
                            {'my_acid': my_acid}, {'p_acid': p_acid}, {'st_acid': st_acid}, {'ar_acid': ar_acid},
                            {'beenic_acid': beenic_acid}, {'pal_acid': pal_acid}, {'ol_acid': ol_acid}, {'ner_acid': ner_acid},
                            {'a_linoleic_acid': a_linoleic_acid}, {'eico_acid': eico_acid}, {'doco_acid': doco_acid}, {'lin_acid': lin_acid},
                            {'gamma_lin_acid': gamma_lin_acid}, {'dih_gamma_lin_acid': dih_gamma_lin_acid}, {'arachidonic_acid': arachidonic_acid},
                            {'sa_un_fatty_acid': sa_un_fatty_acid}, {'o3o6_fatty_acid_quotient': o3o6_fatty_acid_quotient}, {'aa_epa': aa_epa},
                            {'o3_index': o3_index}, {'neut_ul': neut_ul}, {'lymph_ul': lymph_ul}, {'mono_ul': mono_ul}, {'eosi_ul': eosi_ul},
                            {'baso_ul': baso_ul}, {'rdwcv': rdwcv}, {'hct_w': hct_w}, {'hgb_w': hgb_w}, {'rbc_w': rbc_w}, {'azotemia': azotemia},
                            {'uric_acid': uric_acid}, {'creatinine_w': creatinine_w}, {'uricemy_w': uricemy_w}, {'cistatine_c': cistatine_c},
                            {'plt': plt}, {'mpv': mpv}, {'plcr': plcr}, {'pct': pct}, {'pdw': pdw}, {'d_dimero': d_dimero}, {'pai_1': pai_1},
                            {'tot_chol': tot_chol}, {'ldl_chol': ldl_chol}, {'hdl_chol_w': hdl_chol_w}, {'trigl': trigl}, {'na': na}, {'k': k},
                            {'mg': mg}, {'ci': ci}, {'ca': ca}, {'p': p}, {'dhea_w': dhea_w}, {'testo_w': testo_w}, {'tsh': tsh}, {'ft3': ft3},
                            {'ft4': ft4}, {'beta_es_w': beta_es_w}, {'prog_w': prog_w}, {'fe': fe}, {'transferrin': transferrin},
                            {'ferritin_w': ferritin_w}, {'glicemy': glicemy}, {'insulin': insulin}, {'homa': homa}, {'ir': ir},
                            {'albuminemia': albuminemia}, {'tot_prot': tot_prot}, {'tot_prot_ele': tot_prot_ele}, {'albumin_ele': albumin_ele},
                            {'a_1': a_1}, {'a_2': a_2}, {'b_1': b_1}, {'b_2': b_2}, {'gamma': gamma}, {'albumin_dI': albumin_dI},
                            {'a_1_dI': a_1_dI}, {'a_2_dI': a_2_dI}, {'b_1_dI': b_1_dI}, {'b_2_dI': b_2_dI}, {'gamma_dI': gamma_dI},
                            {'ag_rap': ag_rap}, {'got_w': got_w}, {'gpt_w': gpt_w}, {'g_gt_w': g_gt_w}, {'a_photo_w': a_photo_w},
                            {'tot_bili': tot_bili}, {'direct_bili': direct_bili}, {'indirect_bili': indirect_bili}, {'ves': ves},
                            {'pcr_c': pcr_c}, {'tnf_a': tnf_a}, {'inter_6': inter_6}, {'inter_10': inter_10}, {'scatolo': scatolo},
                            {'indicano': indicano}, {'s_weight': s_weight}, {'ph': ph}, {'proteins_ex': proteins_ex}, {'blood_ex': blood_ex},
                            {'ketones': ketones}, {'uro': uro}, {'bilirubin_ex': bilirubin_ex}, {'leuc': leuc}, {'glucose': glucose},
                            {'shbg_w': shbg_w}, {'nt_pro': nt_pro}, {'v_b12': v_b12}, {'v_d': v_d}, {'ves2': ves2}, {'telotest': telotest}
                        ]

  
                    # Calcolo dell'età biologica
                    biological_age = calculate_biological_age(
                        chronological_age, d_roms = d_roms, osi = osi, pat = pat, wbc = wbc, basophils = baso_ul,
                        eosinophils = eosi, lymphocytes = lymph, monocytes = mono, neutrophils = neut, rbc = rbc_m, hgb = hgb_m, 
                        hct = hct_m, mcv = mcv, mch = mch, mchc = mchc, rdw = rdwsd, exams = exams, gender=paziente.gender
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
            error_message = f"System error: {str(e)}\n{traceback.format_exc()}"
            print(error_message)

            context = {
                "error": "Si è verificato un errore di sistema. Controlla di aver inserito tutti i dati corretti nei campi necessari e riprova.",
                "dettaglio": error_message 
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
        # Ottieni il paziente con l'ID specificato
        persona = get_object_or_404(TabellaPazienti, id=id)

        # Recupera l'ID del referto dalla query string
        referto_id = request.GET.get('referto_id')

        # Recupera il referto specifico se l'ID è passato, altrimenti l'ultimo referto
        if referto_id:
            referto = get_object_or_404(ArchivioReferti, id=referto_id, paziente=persona)
        else:
            referto = ArchivioReferti.objects.filter(paziente=persona).order_by("-data_ora_creazione").first()

        # Ottieni i dati estesi associati al referto selezionato
        dati_estesi = DatiEstesiReferti.objects.filter(referto=referto).first() if referto else None

        # Recupera il dottore dalla sessione
        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        # Preparazione del contesto per il template
        context = {
            'persona': persona,
            'referto': referto,
            'datiEstesi': dati_estesi,
            'dottore': dottore,
        }
        return render(request, "includes/Referto.html", context)



class ScaricaReferto(View):
    def get(self, request, persona_id, visite_id):

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)
        persona = get_object_or_404(TabellaPazienti, id=persona_id)
        visite = ElencoVisitePaziente.objects.all()

        # Logica per generare il PDF
        pdf_url = f"/media/pdf/{persona.surname}_{persona.name}_Prescrizione.pdf"

        #DATI REFERTI ETA' BIOLOGICA
        referti_recenti = persona.referti.all().order_by('-data_referto')
        dati_estesi = DatiEstesiReferti.objects.filter(referto__in=referti_recenti)
        ultimo_referto = referti_recenti.first() if referti_recenti else None
        
        dati_estesi_ultimo_referto = None
        if ultimo_referto:
            dati_estesi_ultimo_referto = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()


        #DATI REFERTI PRESCRIZIONI
        json_path = os.path.join(settings.STATIC_ROOT, "includes", "json", "ArchivioEsami.json")

        if not os.path.exists(json_path):
            return JsonResponse({"error": f"File JSON non trovato: {json_path}"}, status=404)

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        visita = ElencoVisitePaziente.objects.get(id=visite_id)
        codici_esami = EsameVisita.objects.filter(visita_id=visite_id).values_list('codice_esame', flat=True)
        listaCodici_Visita = list(codici_esami)

        elencoPrescrizioni = {}

        for esame in data['Foglio1']:  
            codice_esame = esame.get('CODICE_UNIVOCO_ESAME_PIATTAFORMA')  

            if codice_esame:
                codice_esame = str(codice_esame).strip()  

            if codice_esame in listaCodici_Visita:
                elencoPrescrizioni[codice_esame] = esame


        lista_nomi_esami = [esame.get('DESCRIZIONE_ESAME') for esame in elencoPrescrizioni.values() if esame.get('DESCRIZIONE_ESAME')]

        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            'ultimo_referto': ultimo_referto,
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto,
            'dottore' : dottore,
            'visite': visite,
            'visita': visita,
            'lista_nomi_esami': lista_nomi_esami,
            'pdf_url': pdf_url
        }

        return render(request, "includes/cartellaPaziente.html", context)



class DettagliPrescrizioni(View):
    def get(self, request, persona_id, visite_id):

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)
        persona = get_object_or_404(TabellaPazienti, id=persona_id)
        visite = ElencoVisitePaziente.objects.all()

        #DATI REFERTI ETA' BIOLOGICA
        referti_recenti = persona.referti.all().order_by('-data_referto')
        dati_estesi = DatiEstesiReferti.objects.filter(referto__in=referti_recenti)
        ultimo_referto = referti_recenti.first() if referti_recenti else None
        
        dati_estesi_ultimo_referto = None
        if ultimo_referto:
            dati_estesi_ultimo_referto = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()


        #DATI REFERTI PRESCRIZIONI
        json_path = os.path.join(settings.STATIC_ROOT, "includes", "json", "ArchivioEsami.json")

        if not os.path.exists(json_path):
            return JsonResponse({"error": f"File JSON non trovato: {json_path}"}, status=404)

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        visita = ElencoVisitePaziente.objects.get(id=visite_id)
        codici_esami = EsameVisita.objects.filter(visita_id=visite_id).values_list('codice_esame', flat=True)
        listaCodici_Visita = list(codici_esami)

        elencoPrescrizioni = {}

        for esame in data['Foglio1']:  
            codice_esame = esame.get('CODICE_UNIVOCO_ESAME_PIATTAFORMA')  

            if codice_esame:
                codice_esame = str(codice_esame).strip()  

            if codice_esame in listaCodici_Visita:
                elencoPrescrizioni[codice_esame] = esame

        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            'ultimo_referto': ultimo_referto,
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto,
            'dottore' : dottore,
            'visite': visite,
            'visita': visita,
            'elencoPrescrizioni': elencoPrescrizioni,
        }

        return render(request, "includes/cartellaPaziente.html", context)


class CartellaPazienteView(View):

    def get(self, request, id):
        
        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)
        persona = get_object_or_404(TabellaPazienti, id=id)

        
        #DATI REFERTI ETA' BIOLOGICA
        referti_recenti = persona.referti.all().order_by('-data_referto')
        dati_estesi = DatiEstesiReferti.objects.filter(referto__in=referti_recenti)
        ultimo_referto = referti_recenti.first() if referti_recenti else None
        
        dati_estesi_ultimo_referto = None
        if ultimo_referto:
            dati_estesi_ultimo_referto = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()


        visite = ElencoVisitePaziente.objects.all()

        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            'ultimo_referto': ultimo_referto,
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto,
            'dottore' : dottore,
            'visite': visite,
            #'elencoPrescrizioni': elencoPrescrizioni,
        }

        return render(request, "includes/cartellaPaziente.html", context)

class ElencoRefertiView(View):
    def get(self, request, id):
        
        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)
        persona = get_object_or_404(TabellaPazienti, id=id)
        
        #DATI REFERTI ETA' BIOLOGICA
        referti_recenti = persona.referti.all().order_by('-data_referto')
        dati_estesi = DatiEstesiReferti.objects.filter(referto__in=referti_recenti)
        
        dati_estesi_ultimo_referto = None

        visite = ElencoVisitePaziente.objects.all()

        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto,
            'dottore' : dottore,
            'visite': visite,
            #'elencoPrescrizioni': elencoPrescrizioni,
        }

        return render(request, "includes/elencoReferti.html", context)


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
    
    def post(self, request, id):
            persona = get_object_or_404(TabellaPazienti, id=id)

            # Aggiornamento dei dati ricevuti dal form
            # Identifica il form che ha inviato i dati
            form_id = request.POST.get('form_id')

            # Gestione dei dati in base al form_id
            if form_id == 'datiBaseForm3':
                # Aggiorna i dati relativi alla terza tabella
                alcol_value = request.POST.get('alcol')
                persona.alcol = request.POST.get('alcol')
                persona.alcol_type = request.POST.get('alcol_type')
                persona.data_alcol = request.POST.get('data_alcol') or None
                persona.alcol_frequency = request.POST.get('alcol_frequency')

            elif form_id == 'datiBaseForm4':
                # Aggiorna i dati relativi alla quarta tabella
                persona.smoke = request.POST.get('smoke')
                persona.smoke_frequency = request.POST.get('smoke_frequency')
                persona.reduced_intake = request.POST.get('reduced_intake')

            elif form_id == 'datiBaseForm5':
                # Aggiorna i dati relativi alla quinta tabella
                persona.sport = request.POST.get('sport')
                persona.sport_livello = request.POST.get('sport_livello')
                persona.sport_frequency = request.POST.get('sport_frequency')

            # Salva le modifiche solo se c'è un form valido
            if form_id:
                persona.save()
                print(f"Modifiche salvate per {form_id}")
            else:
                print("Errore: form_id non ricevuto o non valido")

            return redirect('dati_base', id=persona.id)


# Blood Group view
@method_decorator(csrf_exempt, name='dispatch')
class UpdateBloodDataView(View):

    def post(self, request, id):
        try:
            # Estrai i dati dalla richiesta JSON
            data = json.loads(request.body)
            blood_group = data.get("blood_group", "N/A")
            rh_factor = data.get("rh_factor", "N/A")
            pressure_min = data.get("pressure_min", "Inserisci i valori")
            pressure_max = data.get("pressure_max", "Inserisci i valori")
            heart_rate = data.get("heart_rate", "Inserisci i valori")

            # Recupera il paziente corrispondente
            persona = get_object_or_404(TabellaPazienti, id=id)

            # Aggiorna i dati
            persona.blood_group = blood_group
            persona.rh_factor = rh_factor
            persona.pressure_min = pressure_min
            persona.pressure_max = pressure_max
            persona.heart_rate = heart_rate
            persona.save()

            return JsonResponse({"status": "success", "message": "Dati aggiornati correttamente"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Formato JSON non valido"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

class InserisciPazienteView(View):

    def get(self, request):

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        context = {
            'dottore' : dottore
        }

        return render(request, "includes/InserisciPaziente.html", context)
    

    def post(self, request):
        try:
            success = None  # ✅ Inizializziamo success per evitare l'errore
            dottore = request.user.utentiregistraticredenziali if hasattr(request.user, 'utentiregistraticredenziali') else None
            codice_fiscale = request.POST.get('codice_fiscale')

            dottore_id = request.session.get('dottore_id')
            dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

            paziente_esistente = TabellaPazienti.objects.filter(codice_fiscale=codice_fiscale).first()

            def parse_date(date_str):
                return date_str if date_str else None

            context = {'dottore': dottore}

            if paziente_esistente:
                campi_opzionali = [
                    'province', 'cap', 'email', 'phone', 'associate_staff', 'height', 'weight', 'bmi', 'bmi_detection_date',
                    'girth_value', 'girth_notes', 'girth_date',
                    'alcol', 'alcol_type', 'data_alcol', 'alcol_frequency',
                    'smoke', 'smoke_frequency', 'reduced_intake',
                    'sport', 'sport_livello', 'sport_frequency',
                    'attivita_sedentaria', 'livello_sedentarieta', 'sedentarieta_nota', 'blood_group'
                ]

                if any(request.POST.get(campo) for campo in campi_opzionali):
                    paziente_esistente.email = request.POST.get('email')
                    paziente_esistente.phone = request.POST.get('phone')
                    paziente_esistente.cap = request.POST.get('cap')
                    paziente_esistente.province = request.POST.get('province')
                    paziente_esistente.associate_staff = request.POST.get('associate_staff')
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
                    paziente_esistente.blood_group = request.POST.get('blood_group')

                    paziente_esistente.save()
                    success = "I dati del paziente sono stati aggiornati con successo!"
                else:
                    errore = "Operazione non andata a buon fine: 'Un Utente con questo Codice Fiscale è gia presente all'interno del database'."
                    context['errore'] = errore
            
            else:
                # ✅ Creazione nuovo paziente
                TabellaPazienti.objects.create(
                    dottore=dottore,
                    name=request.POST.get('name'),
                    surname=request.POST.get('surname'),
                    email=request.POST.get('email'),
                    phone=request.POST.get('phone'),
                    dob=parse_date(request.POST.get('dob')),
                    gender=request.POST.get('gender'),
                    cap=request.POST.get('cap'),
                    province=request.POST.get('province'),
                    place_of_birth=request.POST.get('place_of_birth'),
                    codice_fiscale=codice_fiscale,
                    chronological_age=request.POST.get('chronological_age'),
                    blood_group=request.POST.get('blood_group'),
                    associate_staff=request.POST.get('associate_staff'),
                    height=request.POST.get('height'),
                    weight=request.POST.get('weight'),
                    bmi=request.POST.get('bmi'),
                    bmi_detection_date=parse_date(request.POST.get('bmi_detection_date')),
                    girth_value=request.POST.get('girth_value'),
                    girth_notes=request.POST.get('girth_notes'),
                    girth_date=parse_date(request.POST.get('girth_date')),
                    alcol=request.POST.get('alcol') == 'on',
                    alcol_type=request.POST.get('alcol_type'),
                    data_alcol=parse_date(request.POST.get('data_alcol')),
                    alcol_frequency=request.POST.get('alcol_frequency'),
                    smoke=request.POST.get('smoke') == 'on',
                    smoke_frequency=request.POST.get('smoke_frequency'),
                    reduced_intake=request.POST.get('reduced_intake'),
                    sport=request.POST.get('sport') == 'on',
                    sport_livello=request.POST.get('sport_livello'),
                    sport_frequency=request.POST.get('sport_frequency'),
                    attivita_sedentaria=request.POST.get('attivita_sedentaria') == 'on',
                    livello_sedentarieta=request.POST.get('livello_sedentarieta'),
                    sedentarieta_nota=request.POST.get('sedentarieta_nota'),
                )
                success = "Nuovo paziente salvato con successo!"

            # ✅ Aggiorna il contesto con success solo se ha un valore
            if success:
                context["success"] = success

            return render(request, "includes/InserisciPaziente.html", context)

        except Exception as e:
            context["errore"] = f"system error: {str(e)} --- Controlla di aver inserito tutti i dati corretti nei campi necessari e riprova."
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


def dettaglio_paziente(request, id):
    try:
        paziente = TabellaPazienti.objects.get(id=id)
    except TabellaPazienti.DoesNotExist:
        return redirect('pagina_errore')  # Gestione dell'errore se il paziente non esiste

    # Aggiungi valori di default se email o telefono non sono disponibili
    email = getattr(paziente, 'email', "Not provided")
    phone = getattr(paziente, 'phone', "Not provided")

    context = {
        'persona': paziente,
        'email': email,
        'phone': phone,
    }
    return render(request, 'nome_del_tuo_template.html', context)



@csrf_exempt  # Rimuovilo in produzione se non necessario
def update_persona_contact(request, id):
    if request.method == "POST":
        try:
            # Estrai il corpo della richiesta
            data = json.loads(request.body)
            email = data.get("email")
            phone = data.get("phone")
            associate_staff = data.get("associate_staff")
            lastVisit = data.get("lastVisit")
            upcomingVisit = data.get("upcomingVisit")
            blood_group = data.get("blood_group")

            # Recupera il modello e aggiorna i dati
            from .models import TabellaPazienti  # Sostituisci con il tuo modello
            persona = TabellaPazienti.objects.get(id=id)
            persona.email = email
            persona.phone = phone
            persona.associate_staff = associate_staff
            persona.lastVisit = lastVisit
            persona.upcomingVisit = upcomingVisit
            persona.blood_group = blood_group
            persona.save()  # Salva le modifiche nel database

            # print(f"Persona {id} aggiornata con email: {email}, telefono: {phone}, associate_staff: {associate_staff}, lastVisit: {lastVisit}, upcomingVisit: {upcomingVisit}, blood_group: {blood_group}")

            return JsonResponse({"success": True})
        except TabellaPazienti.DoesNotExist:
            return JsonResponse({"success": False, "error": "Persona non trovata"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON non valido"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "error": "Metodo non valido"})


# Funzione per aggiornare i dati di una persona in composizione corpo
@csrf_exempt
def update_persona_composizione(request, id):
    try:
        persona = TabellaPazienti.objects.get(id=id)
    except TabellaPazienti.DoesNotExist:
        return JsonResponse({"success": False, "error": "Persona non trovata"}, status=404)

    if request.method == "GET":
        # ✅ Manteniamo tutti i dati della persona
        data = {
            "success": True,
            "personaComposizione": {
                "height": persona.height,
                "weight": persona.weight,
                "bmi": persona.bmi,
                "bmi_detection_date": persona.bmi_detection_date,
                "girth_value": persona.girth_value,
                "girth_notes": persona.girth_notes,
                "girth_date": persona.girth_date,
                "sport_frequency": persona.sport_frequency,
                "livello_sedentarieta": persona.livello_sedentarieta,
                "grasso": persona.grasso,
                "acqua": persona.acqua,
                "massa_ossea": persona.massa_ossea,
                "massa_muscolare": persona.massa_muscolare,
                "bmr": persona.bmr,
                "eta_metabolica": persona.eta_metabolica,
                "grasso_viscerale": persona.grasso_viscerale,
                "whr": persona.whr,
                "whtr": persona.whtr,
                "punteggio_fisico": persona.punteggio_fisico,
                "storico_punteggi": persona.storico_punteggi or [],  # ✅ Restituiamo anche lo storico
            },
        }
        return JsonResponse(data)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            campi_da_aggiornare = []

            # ✅ Controllo per il reset dello storico punteggi
            if data.get("reset_storico_punteggi", False):
                persona.storico_punteggi = []  # ✅ Resetta lo storico
                persona.punteggio_fisico = None  # ✅ Reset del punteggio attuale
                persona.save(update_fields=["storico_punteggi", "punteggio_fisico"])
                return JsonResponse({"success": True})

            # ✅ Aggiorna tutti gli altri campi se presenti
            for field in [
                "height", "weight", "bmi", "bmi_detection_date",
                "girth_value", "girth_notes", "girth_date", "sport_frequency",
                "livello_sedentarieta", "grasso", "acqua", "massa_ossea",
                "massa_muscolare", "bmr", "eta_metabolica", "grasso_viscerale",
                "whr", "whtr"
            ]:
                if field in data:
                    setattr(persona, field, data[field])
                    campi_da_aggiornare.append(field)

            # ✅ Gestione del punteggio fisico
            if "punteggio_fisico" in data:
                try:
                    nuovo_punteggio = int(data["punteggio_fisico"])  # ✅ Conversione a int
                except ValueError:
                    return JsonResponse({"success": False, "error": "Punteggio non valido"}, status=400)

                if not (1 <= nuovo_punteggio <= 9):
                    return JsonResponse({"success": False, "error": "Punteggio fuori range"}, status=400)

                # ✅ Se il punteggio è cambiato, aggiorniamo lo storico
                if persona.punteggio_fisico != nuovo_punteggio:
                    if not isinstance(persona.storico_punteggi, list):
                        persona.storico_punteggi = []  # ✅ Inizializza se non esiste

                    # ✅ Aggiunge il nuovo punteggio con data
                    persona.storico_punteggi.append({
                        "punteggio": nuovo_punteggio,
                        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })

                    # ✅ Aggiorniamo il punteggio attuale
                    persona.punteggio_fisico = nuovo_punteggio
                    campi_da_aggiornare.append("punteggio_fisico")
                    campi_da_aggiornare.append("storico_punteggi")

            # ✅ Salva solo i campi aggiornati
            if campi_da_aggiornare:
                persona.save(update_fields=campi_da_aggiornare)

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON non valido"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    else:
        return JsonResponse({"success": False, "error": "Metodo non valido"}, status=405)




class EtaVitaleView(View):

    def get(self, request, id):

        persona = get_object_or_404(TabellaPazienti, id=id)
  
        referti_test_recenti = persona.referti_test.all().order_by('-data_ora_creazione')

        print('Referto recente: ', referti_test_recenti)
      
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=request.session.get('dottore_id'))

        context = {
            'persona': persona,
            'referti_test_recenti': referti_test_recenti,
            'dottore': dottore
        }

        return render(request, "includes/EtaVitale.html", context)
    
    def post(self):
        return
    


class TestEtaVitaleView(View):

    def get(self,request, id):
           
        persona = get_object_or_404(TabellaPazienti, id=id)

        ultimo_referto = persona.referti.order_by('-data_referto').first()
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=request.session.get('dottore_id'))
        referti_test_recenti = persona.referti_test.all().order_by('-data_ora_creazione')

        dati_estesi = None
        if ultimo_referto:
            dati_estesi = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()
        
        context = {
            'persona': persona,
            'dati_estesi': dati_estesi,
            'dottore' : dottore,
            'referti_test_recenti': referti_test_recenti
        }

        return render(request, "includes/testVitale.html", context)
 
    def post(self, request, id):
        persona = get_object_or_404(TabellaPazienti, id=id)
        data = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}
        referti_test_recenti = persona.referti_test.all().order_by('-data_ora_creazione')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=request.session.get('dottore_id'))

        SiIm_Somma = (
            int(data.get('SiIm_1', 0)) +
            int(data.get('SiIm_2', 0)) +
            int(data.get('SiIm_3', 0)) +
            int(data.get('SiIm_4', 0)) +
            int(data.get('SiIm_5', 0)) +
            int(data.get('SiIm_6', 0)) +
            int(data.get('SiIm_7', 0))
        )

        Fss_Somma = (
            int(data.get('fss_1', 0)) +
            int(data.get('fss_2', 0)) +
            int(data.get('fss_3', 0)) +
            int(data.get('fss_4', 0)) +
            int(data.get('fss_5', 0)) +
            int(data.get('fss_6', 0)) +
            int(data.get('fss_7', 0)) +
            int(data.get('fss_8', 0))
        )
          
        Sarc_f_Somma = (
            int(data.get('Sarc_f_1', 0)) +
            int(data.get('Sarc_f_2', 0)) +
            int(data.get('Sarc_f_3', 0)) +
            int(data.get('Sarc_f_4', 0)) +
            int(data.get('Sarc_f_5', 0)) 
        )

        biomarcatori = {
            "lymph": safe_float(data, 'Lymph'), 
            "wbc": safe_float(data, 'wbc'),
            "pcr": safe_float(data, 'Proteins_c'),
            "il6": safe_float(data, 'Inter_6'),
            "tnf": safe_float(data, 'Tnf')
        }

        antropometria = {
            "polpaccio": safe_float(data, 'CirPolp'),
            "waist_hip_ratio": safe_float(data, 'WHip_ratio')
        }

        performance_fisica = int(data.get('SPPB', 0))

        punteggioFinale = calcola_punteggio_finale(SiIm_Somma, Fss_Somma,Sarc_f_Somma, biomarcatori, antropometria, performance_fisica )

        print(punteggioFinale)

        referto = ArchivioRefertiTest(
            paziente = persona,
            punteggio = punteggioFinale,
            #documento = request.FILES.get('documento')
        )
        referto.save()


        datiEstesi = DatiEstesiRefertiTest(
            referto = referto,

            SiIm = SiIm_Somma,
            Lymph = safe_float(data, 'Lymph'),
            Lymph_el = safe_float(data, 'Lymph_el'),
            wbc = safe_float(data, 'wbc'),
            Proteins_c = safe_float(data, 'Proteins_c'),

            #BIOMARCATORI CIRCOLANTI DELL'INFIAMMAZIONE
            Inter_6 = safe_float(data, 'Inter_6'),
            Tnf = safe_float(data, 'Tnf'),
            Mono = safe_float(data, 'Mono'),
            Mono_el = safe_float(data, 'Mono_el'),

            #ENERGIA E MTABOLISMO
            Fss = Fss_Somma,
            CirPolp = safe_float(data, 'CirPolp'),
            WHip_ratio = safe_float(data, 'WHip_ratio'),
            WH_ratio = safe_float(data, 'WH_ratio'),

            #BIOMARCATORI CIRCOLANTI DEL METABOLISMO
            Glic = safe_float(data, 'Glic'),
            Emog = safe_float(data, 'Emog'),
            Insu = safe_float(data, 'Insu'),
            Pept_c = safe_float(data, 'Pept_c'),
            Col_tot = safe_float(data, 'Col_tot'),
            Col_ldl = safe_float(data, 'Col_ldl'),
            Col_hdl = safe_float(data, 'Col_hdl'),
            Trigl = safe_float(data, 'Trigl'),
            albumina = safe_float(data, 'albumina'),
            clearance_urea = safe_float(data, 'clearance_urea'),
            igf_1 = safe_float(data, 'ifg_1'),
            
            # Funzione Neuromuscolare
            sarc_f = Sarc_f_Somma,
            hgs_test = data.get('HGS_test'),
            
            # Performance Fisica
            sppb = data.get('SPPB')
        )
        datiEstesi.save()



        context = {
            'persona': persona,
            'modal' : True,
            'Referto': referto,
            'referti_test_recenti': referti_test_recenti,
            'dottore': dottore
        }

        return render(request, "includes/EtaVitale.html", context)


class RefertoQuizView(View):
    def get(self, request, persona_id, referto_id):

        persona = get_object_or_404(TabellaPazienti, id=persona_id)

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        referto = get_object_or_404(ArchivioRefertiTest, id=referto_id)

        ultimo_referto = persona.referti.order_by('-data_referto')
        
        datiEstesi = None
        if referto:
            datiEstesi = DatiEstesiRefertiTest.objects.filter(referto=referto).first()

        context = {
            'persona': persona,
            'ultimo_referto': referto,
            'datiEstesi': datiEstesi,
            'dottore' : dottore,
            'referto' : ultimo_referto
        }

        return render(request, "includes/RefertoQuiz.html", context)


# Referto View
def referti_view(request, referto_id):
    referto = ArchivioReferti.objects.get(id=referto_id)
    return render(request, 'includes/Referto.html', {'data_referto': referto.data_referto})



#PRESCRIZIONI VIEW
class PrescrizioniView(View):

    def get(self, request, persona_id):

        persona = get_object_or_404(TabellaPazienti, id=persona_id)

        dottore_id = request.session.get('dottore_id')
        dottore = get_object_or_404(UtentiRegistratiCredenziali, id=dottore_id)

        context = {
            'persona': persona,
            'dottore': dottore,
        }

        return render(request, "includes/prescrizioni.html", context)


    def post(self, request, persona_id):

        persona = get_object_or_404(TabellaPazienti, id=persona_id)
        
        listaCodici = request.POST.get('codici_esami')
        data_list = json.loads(listaCodici)
        numeri = [x for x in data_list if x.isdigit()]

        nuova_visita = ElencoVisitePaziente.objects.create(
            paziente = persona,
        )

        for i in range(0, len(numeri)):
            EsameVisita.objects.create(
                visita=nuova_visita,
                codice_esame=numeri[i],
            )

        return redirect('cartella_paziente', persona_id)
 


