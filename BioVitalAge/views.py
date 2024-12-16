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
            chronological_age = int(data.get('chronological_age'))
            obri_index = float(data.get('obri_index'))
            d_roms = float(data.get('d_roms'))
            aa_epa = float(data.get('aa_epa'))
            aa_dha = float(data.get('aa_dha'))
            homa_test = float(data.get('homa_test'))
            cardiovascular_risk = float(data.get('cardiovascular_risk'))
            osi = float(data.get('osi'))
            pat = float(data.get('pat'))

            glucose = float(data.get('glucose'))
            creatinine = float(data.get('creatinine'))
            ferritin = float(data.get('ferritin'))
            albumin = float(data.get('albumin'))
            protein = float(data.get('protein'))
            bilirubin = float(data.get('bilirubin'))
            uric_acid = float(data.get('uric_acid'))

            exams = [glucose, creatinine, ferritin, albumin, protein, bilirubin, uric_acid]

            # Calcolo dell'età biologica
            biological_age = calculate_biological_age(
                chronological_age, obri_index, d_roms, aa_epa, aa_dha,
                homa_test, cardiovascular_risk, osi, pat, exams
            )

            # Salva i dati estesi del referto
            dati_estesi = DatiEstesiReferti(
                referto=referto,
                chronological_age=chronological_age,
                obri_index=obri_index,
                d_roms=d_roms,
                aa_epa=aa_epa,
                aa_dha=aa_dha,
                homa_test=homa_test,
                cardiovascular_risk=cardiovascular_risk,
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



