from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import UtentiRegistratiCredenziali,TabellaPazienti, ArchivioReferti, DatiEstesiReferti
from .utils import calculate_biological_age
from django.contrib.sessions.models import Session
from django.db.models import OuterRef, Subquery

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

def get_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def get_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
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
                print("Paziente trovato:", paziente)
            else:
                # Salva i dati del paziente (solo informazioni personali)
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
                print("Paziente creato:", paziente)

            # Salva i dati del referto
            referto = ArchivioReferti(
                paziente=paziente,
                descrizione=data.get('descrizione'),
                documento=request.FILES.get('documento')  # Carica eventuale file referto se necessario
            )
            referto.save()
            print("Referto salvato:", referto)

            # Estrai i dati necessari per la tabella DatiEstesiReferti
            chronological_age = get_int(data.get('chronological_age'), default=0)
            d_roms = get_float(data.get('d_roms'), default=0.0)
            osi = get_float(data.get('osi'), default=0.0)
            pat = get_float(data.get('pat'), default=0.0)
            wbc = get_float(data.get('wbc'), default=0.0)
            basophils = get_float(data.get('basophils'), default=0.0)
            eosinophils = get_float(data.get('eosinophils'), default=0.0)
            lymphocytes = get_float(data.get('lymphocytes'), default=0.0)
            monocytes = get_float(data.get('monocytes'), default=0.0)
            neutrophils = get_float(data.get('neutrophils'), default=0.0)
            rbc = get_float(data.get('rbc'), default=0.0)
            hgb = get_float(data.get('hgb'), default=0.0)
            hct = get_float(data.get('hct'), default=0.0)
            mcv = get_float(data.get('mcv'), default=0.0)
            mch = get_float(data.get('mch'), default=0.0)
            mchc = get_float(data.get('mchc'), default=0.0)
            rdw = get_float(data.get('rdw'), default=0.0)

            
            glucose = get_float(data.get('glucose'), default=0.0)
            creatinine = get_float(data.get('creatinine'), default=0.0)
            ferritin = get_float(data.get('ferritin'), default=0.0)
            albumin = get_float(data.get('albumin'), default=0.0)
            protein = get_float(data.get('protein'), default=0.0)
            bilirubin = get_float(data.get('bilirubin'), default=0.0)
            uric_acid = get_float(data.get('uric_acid'), default=0.0)

            exams = [glucose, creatinine, ferritin, albumin, protein, bilirubin, uric_acid]

            # Calcolo dell'età biologica
            biological_age = calculate_biological_age(
                chronological_age, d_roms, osi, pat, wbc, basophils,
                eosinophils, lymphocytes, monocytes, neutrophils, rbc, hgb, 
                hct, mcv, mch, mchc, rdw, exams
            )

            # Salva i dati estesi del referto
            dati_estesi = DatiEstesiReferti(
                referto=referto,
                chronological_age=chronological_age,
                d_roms=d_roms,
                osi=osi,
                pat=pat,
                glucose=glucose,
                creatinine=creatinine,
                ferritin=ferritin,
                albumin=albumin,
                protein=protein,
                bilirubin=bilirubin,
                uric_acid=uric_acid,
                biological_age=biological_age
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


