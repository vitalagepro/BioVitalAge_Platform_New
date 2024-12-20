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
                    'd_roms', 'osi', 'pat', 'fa_saturated', 'o9o7fatty_acids', 'o3fatty_acids', 'o6fatty_acids', 's_u_fatty_acids',
                    'o6o3_fatty_acids_quotient', 'aa_epa_quotient', 'O3_index', 'wbc', 'basophils', 'eosinophils', 'lymphocytes',
                    'monocytes', 'neutrophils', 'rbc', 'hgb', 'hct', 'mcv', 'mch', 'mchc', 'rdw', 'glucose', 'creatinine',
                    'ferritin', 'albumin', 'protein', 'bilirubin', 'uric_acid'
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

                    fa_saturated = safe_float(data, 'fa_saturated')
                    o9o7fatty_acids = safe_float(data, 'o9o7fatty_acids')
                    o3fatty_acids = safe_float(data, 'o3fatty_acids')
                    o6fatty_acids = safe_float(data, 'o6fatty_acids')
                    s_u_fatty_acids = safe_float(data, 's_u_fatty_acids')
                    o6o3_fatty_acids_quotient = safe_float(data, 'o6o3_fatty_acids_quotient')
                    aa_epa_quotient = safe_float(data, 'aa_epa_quotient')
                    O3_index = safe_float(data, 'O3_index')

                    wbc = safe_float(data, 'wbc')
                    baso = safe_float(data, 'basophils')
                    eosi = safe_float(data, 'eosinophils')
                    lymph = safe_float(data, 'lymphocytes')
                    mono = safe_float(data, 'monocytes')
                    neut = safe_float(data, 'neutrophils')
                    rbc = safe_float(data, 'rbc')
                    hgb = safe_float(data, 'hgb')
                    hct = safe_float(data, 'hct')
                    mcv = safe_float(data, 'mcv')
                    mch = safe_float(data, 'mch')
                    mchc = safe_float(data, 'mchc')
                    rdw = safe_float(data, 'rdw')

                    azotemia = safe_float(data, 'azotemia')
                    glucose = safe_float(data, 'glucose')
                    creatinine = safe_float(data, 'creatinine')
                    ferritin = safe_float(data, 'ferritin')
                    albumin = safe_float(data, 'albumin')
                    protein = safe_float(data, 'protein')
                    bilirubin = safe_float(data, 'bilirubin')
                    uric_acid = safe_float(data, 'uric_acid')


                    exams = [glucose, creatinine, ferritin, albumin, protein, bilirubin, uric_acid]

                    # Calcolo dell'età biologica
                    biological_age = calculate_biological_age(
                        chronological_age, d_roms, osi, pat, wbc, baso,
                        eosi, lymph, mono, neut, rbc, hgb, 
                        hct, mcv, mch, mchc, rdw, exams
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
                        rbc=rbc,
                        hct=hct,
                        hgb=hgb,
                        mch=mch,
                        mchc=mchc,
                        mcv=mcv,
                        glucose=glucose,
                        azotemia=azotemia,
                        creatinine=creatinine,
                        ferritin=ferritin,
                        albumin=albumin,
                        protein=protein,
                        bilirubin=bilirubin,
                        uric_acid=uric_acid,
                        biological_age=biological_age,
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
                    'd_roms', 'osi', 'pat', 'fa_saturated', 'o9o7fatty_acids', 'o3fatty_acids', 'o6fatty_acids', 's_u_fatty_acids',
                    'o6o3_fatty_acids_quotient', 'aa_epa_quotient', 'O3_index', 'wbc', 'basophils', 'eosinophils', 'lymphocytes',
                    'monocytes', 'neutrophils', 'rbc', 'hgb', 'hct', 'mcv', 'mch', 'mchc', 'rdw', 'glucose', 'creatinine',
                    'ferritin', 'albumin', 'protein', 'bilirubin', 'uric_acid'
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

                    fa_saturated = safe_float(data, 'fa_saturated')
                    o9o7fatty_acids = safe_float(data, 'o9o7fatty_acids')
                    o3fatty_acids = safe_float(data, 'o3fatty_acids')
                    o6fatty_acids = safe_float(data, 'o6fatty_acids')
                    s_u_fatty_acids = safe_float(data, 's_u_fatty_acids')
                    o6o3_fatty_acids_quotient = safe_float(data, 'o6o3_fatty_acids_quotient')
                    aa_epa_quotient = safe_float(data, 'aa_epa_quotient')
                    O3_index = safe_float(data, 'O3_index')

                    wbc = safe_float(data, 'wbc')
                    baso = safe_float(data, 'basophils')
                    eosi = safe_float(data, 'eosinophils')
                    lymph = safe_float(data, 'lymphocytes')
                    mono = safe_float(data, 'monocytes')
                    neut = safe_float(data, 'neutrophils')
                    rbc = safe_float(data, 'rbc')
                    hgb = safe_float(data, 'hgb')
                    hct = safe_float(data, 'hct')
                    mcv = safe_float(data, 'mcv')
                    mch = safe_float(data, 'mch')
                    mchc = safe_float(data, 'mchc')
                    rdw = safe_float(data, 'rdw')

                    azotemia = safe_float(data, 'azotemia')
                    glucose = safe_float(data, 'glucose')
                    creatinine = safe_float(data, 'creatinine')
                    ferritin = safe_float(data, 'ferritin')
                    albumin = safe_float(data, 'albumin')
                    protein = safe_float(data, 'protein')
                    bilirubin = safe_float(data, 'bilirubin')
                    uric_acid = safe_float(data, 'uric_acid')

                    exams = [glucose, creatinine, ferritin, albumin, protein, bilirubin, uric_acid]

                    # Calcolo dell'età biologica
                    biological_age = calculate_biological_age(
                        chronological_age, d_roms, osi, pat, wbc, baso,
                        eosi, lymph, mono, neut, rbc, hgb, 
                        hct, mcv, mch, mchc, rdw, exams
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
                        rbc=rbc,
                        hct=hct,
                        hgb=hgb,
                        mch=mch,
                        mchc=mchc,
                        mcv=mcv,
                        glucose=glucose,
                        azotemia=azotemia,
                        creatinine=creatinine,
                        ferritin=ferritin,
                        albumin=albumin,
                        protein=protein,
                        bilirubin=bilirubin,
                        uric_acid=uric_acid,
                        biological_age=biological_age,
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



