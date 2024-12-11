from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import UtentiRegistratiCredenziali,TabellaPazienti
from .utils import calculate_biological_age

# Create your views here.

class LoginRenderingPage(View):
    def get(self, request):
        return render(request, 'includes/login.html')

class HomePageRender(View):

    def get(self, request):
        persone = TabellaPazienti.objects.all()
        return render(request, "includes/homePage.html", {"persone": persone})
    
    def post(self, request):

        emailInput = request.POST['email']
        passwordInput = request.POST['password']

        Query = UtentiRegistratiCredenziali.objects.all().values()

        for record in Query:  
            for key, value in record.items():
                if key == 'email':
                    if value == emailInput: 

                        if record['password'] == passwordInput:
                            return render(request, 'includes/homePage.html')
                        
                        else:
                            return render(request, 'includes/login.html', {'error' : 'Password errata' })
                        
                    else:
                        return render(request, 'includes/login.html', {'error' : 'Email inserita non valida o non registrata' })
                    
class CalcolatoreRender(View):
    def get(self, request):
        return render(request, 'includes/calcolatore.html')


    def post(self, request):
        data = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}
        
        try:
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
            data['biological_age'] = biological_age

            # Salva i dati nel database
            paziente = TabellaPazienti(
                name=data.get('name'),
                surname=data.get('surname'),
                dob=data.get('dob'),
                gender=data.get('gender'),
                place_of_birth=data.get('place_of_birth'),
                codice_fiscale=data.get('codice_fiscale'),
                chronological_age=chronological_age,
                obri_index=obri_index,
                d_roms=d_roms,
                aa_epa=aa_epa,
                aa_dha=aa_dha,
                homa_test=homa_test,
                cardiovascular_risk=cardiovascular_risk,
                osi=osi,
                pat=pat,
                wbc=float(data.get('wbc', 0)),
                baso=float(data.get('baso', 0)),
                eosi=int(data.get('eosi', 0)),
                lymph=float(data.get('lymph', 0)),
                mono=float(data.get('mono', 0)),
                neut=float(data.get('neut', 0)),
                rbc=float(data.get('rbc', 0)),
                hct=float(data.get('hct', 0)),
                hgb=float(data.get('hgb', 0)),
                mch=float(data.get('mch', 0)),
                mchc=float(data.get('mchc', 0)),
                mcv=float(data.get('mcv', 0)),
                glucose=glucose,
                creatinine=creatinine,
                ferritin=ferritin,
                albumin=albumin,
                protein=protein,
                bilirubin=bilirubin,
                uric_acid=uric_acid,
                biological_age=biological_age
            )
            paziente.save()

            context = {
                "show_modal": True,
                "biological_age": biological_age,
                "data": data,
            }
            return render(request, "includes/calcolatore.html", context)


        except Exception as e:
            context = {
                "error": str(e),
                "data": data,
            }
            return render(request, "includes/calcolatore.html", context)



class RisultatiRender(View):
    def get(self, request):
        persone = TabellaPazienti.objects.all()
        return render(request, "includes/risultati.html", {"persone": persone})


 
class PersonaDetailView(View):
    def get(self, request, id):
        persona = get_object_or_404(TabellaPazienti, id=id)
        return render(request, "includes/persona_detail.html", {"persona": persona})


class CartellaPazienteView(View):
    def get(self, request, id):
        persona = get_object_or_404(TabellaPazienti, id=id)
        return render(request, "includes/cartellaPaziente.html", {"persona": persona})




