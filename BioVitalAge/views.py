# --- IMPORTS STANDARD ---
import requests # type: ignore
import calendar
import json
import os
import traceback
import logging
import uuid

from datetime import datetime, timedelta
from collections import defaultdict

# --- IMPORTS DI DJANGO ---
from django.core.cache import cache # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.http import JsonResponse # type: ignore
from django.views import View # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.conf import settings # type: ignore
from django.utils import timezone as dj_timezone # type: ignore
from django.utils.decorators import method_decorator # type: ignore
from django.utils.timezone import now, localtime # type: ignore
from django.utils.dateparse import parse_date # type: ignore
from django.db.models import OuterRef, Subquery, Count, Q, Avg, Min, Max # type: ignore
from django.db.models.functions import ExtractMonth # type: ignore
from django.contrib.auth.hashers import check_password # type: ignore
from django.db.models import OuterRef # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin # type: ignore
from django.contrib.auth import update_session_auth_hash # type: ignore


# --- IMPORTS PERSONALI (APP) ---
from .utils import *
from BioVitalAge.funzioni_python.calcolo_capacita_vitale import *
from BioVitalAge.funzioni_python.calcolo_eta_biologica import *
from BioVitalAge.funzioni_python.calcoloMetabolica import *
from .models import *
from BioVitalAge.error_handlers import catch_exceptions


logger = logging.getLogger(__name__)

#----------------------------------------
# ----  SEZIONE LOGIN / HOME PAGE   -----
#----------------------------------------

# VIEW LOGIN
@method_decorator(catch_exceptions, name='dispatch')
class LoginRenderingPage(View):

    def get(self, request):
        response = render(request, 'includes/login.html')
        response.delete_cookie('disclaimer_accepted', path='/')
        return response

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password) 

        if user:
            login(request, user)
            return redirect('HomePage')
        
        return render(request, 'includes/login.html', {
            'error': 'Email o password non valide'
        })

# VIEW LOGOUT
@method_decorator(catch_exceptions, name='dispatch')
class LogOutRender(View):

    def get(self, request):
        logout(request)
        return redirect('login')

# VIEW HOME PAGE
@method_decorator(catch_exceptions, name='dispatch')
class HomePageRender(LoginRequiredMixin,View):

    login_url = 'loginPage'

    def get(self, request):
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persone = TabellaPazienti.objects.all().order_by('-id')[:5]
        today = timezone.now().date()
        total_biological_age_count = DatiEstesiReferti.objects.aggregate(total=Count('biological_age'))['total']
        total_pazienti = TabellaPazienti.objects.count() 

        # Calcola il minimo e il massimo dell'età cronologica
        min_age = TabellaPazienti.objects.aggregate(min_age=Min('chronological_age'))['min_age']
        max_age = TabellaPazienti.objects.aggregate(max_age=Max('chronological_age'))['max_age']
        avg_age = TabellaPazienti.objects.aggregate(avg_age=Avg('chronological_age'))['avg_age']

        # Ottieni solo gli appuntamenti futuri
        appuntamenti = Appointment.objects.filter(dottore=dottore, data__gte=today).order_by('data')[:4]
        # Calcola il totale "biological_age" solo per i referti associati ai pazienti di questo dottore
        total_biological_age_count = DatiEstesiReferti.objects.filter(referto__paziente__dottore=dottore).aggregate(total=Count('biological_age'))['total']
        total_pazienti = TabellaPazienti.objects.filter(dottore=dottore).count()

        # Calcola min, max e media dell'età cronologica solo per i pazienti del dottore
        agg_age = TabellaPazienti.objects.filter(dottore=dottore).aggregate(
            min_age=Min('chronological_age'),
            max_age=Max('chronological_age'),
            avg_age=Avg('chronological_age')
        )
        min_age = agg_age['min_age']
        max_age = agg_age['max_age']
        avg_age = agg_age['avg_age']
        persone = TabellaPazienti.objects.filter(dottore=dottore).order_by('-id')[:5]
                
        # --- Calcolo per il report "Totale Pazienti" ---
        today = dj_timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_last_week = start_of_week - timedelta(days=7)
        end_of_last_week = start_of_week - timedelta(days=1)

        # Conta i pazienti creati nella settimana corrente e in quella precedente
        current_week_patients = TabellaPazienti.objects.filter(
            dottore=dottore, created_at__gte=start_of_week
        ).count()
        last_week_patients = TabellaPazienti.objects.filter(
            dottore=dottore, created_at__gte=start_of_last_week, created_at__lte=end_of_last_week
        ).count()

        # Calcola la differenza e la percentuale
        difference = current_week_patients - last_week_patients
        if last_week_patients > 0:
            percentage_increase = (difference / last_week_patients) * 100
        else:
            percentage_increase = 100 if current_week_patients > 0 else 0

         # --- Calcolo per il report "Totale Prescrizioni" ---

        # Utilizza il campo data_referto per filtrare i referti
        current_week_referti = ArchivioReferti.objects.filter(data_referto__gte=start_of_week).count()
        last_week_referti = ArchivioReferti.objects.filter(data_referto__gte=start_of_last_week,
                                                           data_referto__lte=end_of_last_week).count()
        
        difference_referti = current_week_referti - last_week_referti
        abs_difference_referti = abs(difference_referti)

        # Calcola la percentuale come valore assoluto
        if last_week_referti > 0:
            percentage_increase_referti = abs(difference_referti) / last_week_referti * 100
        else:
            percentage_increase_referti = 100 if current_week_referti > 0 else 0

        # Calcola la percentuale media delle età cronologiche
        if min_age is not None and max_age is not None and max_age != min_age:
            relative_position = (avg_age - min_age) / (max_age - min_age)  # valore fra 0 e 1
            media_percentage = relative_position * 100
        else:
            media_percentage = 0

        if dottore.cookie == "SI":
                context = {
                    'persone': persone,
                    'total_pazienti': total_pazienti,
                    'total_biological_age': total_biological_age_count,
                    'appuntamenti': appuntamenti,
                    'current_week_patients': current_week_patients,
                    'last_week_patients': last_week_patients,
                    'difference': difference,
                    'percentage_increase': percentage_increase,
                    'current_week_referti': current_week_referti,
                    'last_week_referti': last_week_referti,
                    'difference_referti': difference_referti,
                    'percentage_increase_referti': percentage_increase_referti,
                    'abs_difference_referti': abs_difference_referti,
                    'min_age': min_age,
                    'max_age': max_age,
                    'media_percentage': media_percentage,
                    'dottore': dottore,
                    'emails': get_gmail_emails_for_user(request.user),
                }
        else:
                context = {
                    'persone': persone,
                    'total_pazienti': total_pazienti,
                    'total_biological_age': total_biological_age_count,
                    'appuntamenti': appuntamenti,
                    'current_week_patients': current_week_patients,
                    'last_week_patients': last_week_patients,
                    'difference': difference,
                    'percentage_increase': percentage_increase,
                    'current_week_referti': current_week_referti,
                    'last_week_referti': last_week_referti,
                    'difference_referti': difference_referti,
                    'percentage_increase_referti': percentage_increase_referti,
                    'abs_difference_referti': abs_difference_referti,
                    'min_age': min_age,
                    'max_age': max_age,
                    'media_percentage': media_percentage,
                    'dottore': dottore,
                    'emails': get_gmail_emails_for_user(request.user),
                    'show_disclaimer': True
                }

        try:
            social_auth = UserSocialAuth.objects.get(user__email=dottore.email, provider="google-oauth2")
            emails = get_gmail_emails_for_user(social_auth.user)
        except UserSocialAuth.DoesNotExist:
            print("⚠️ Account Google non collegato per:", dottore.email)
            emails = []

        context["emails"] = emails  # ← questo è il campo letto nel template da: <script id="emails-data">
        return render(request, "home_page/homePage.html", context)

# VIEW PER LA SEZIONE STATISTICHE
@method_decorator(catch_exceptions, name='dispatch')
class StatisticheView(LoginRequiredMixin,View):

    def get(self, request):

        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        context = {
            'dottore' : dottore,
            'emails': get_gmail_emails_for_user(request.user)
        }
        
        try:
            social_auth = UserSocialAuth.objects.get(user__email=dottore.email, provider="google-oauth2")
            emails = get_gmail_emails_for_user(social_auth.user)
        except UserSocialAuth.DoesNotExist:
            print("⚠️ Account Google non collegato per:", dottore.email)
            emails = []

        context["emails"] = emails
        return render(request, "home_page/statistiche.html", context)
    
# VIEW PER LE NOTIFICHE MEDICAL NEWS
class MedicalNewsNotificationsView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            # Controlla se i dati sono già in cache
            cached_news = cache.get('medical_news')
            if cached_news:
                return JsonResponse({"success": True, "news": cached_news})
            
            api_key = "80734c3bf8e34cf58beedc44db417a73"
            url = f"https://newsapi.org/v2/everything?q=medicina&language=it&apiKey={api_key}"
            response = requests.get(url)
            data = response.json()
            news = []
            # Controlla se lo status della risposta è "ok"
            if data.get("status") == "ok":
                # Usa la chiave "articles" per ottenere gli articoli
                articles = data.get("articles", [])
                for article in articles[:2]:
                    title = article.get("title", "Notizia medica")
                    description = article.get("description", "")
                    # Usa "publishedAt" per la data e prendi solo la parte della data
                    published_at = article.get("publishedAt", "")[:10]
                    # Usa "url" per ottenere il link
                    link = article.get("url", "#")
                    news.append({
                        "id": str(uuid.uuid4()),
                        "title": title,
                        "description": description,
                        "published_at": published_at,
                        "link": link,
                        "type": "info",
                        "origin": "medical"
                    })
                # Salva in cache per 30 minuti (1800 secondi)
                cache.set('medical_news', news, 1800)
            return JsonResponse({"success": True, "news": news})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

# VIEW PER LE NOTIFICHE
class AppointmentNotificationsView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        try:
            # non serve più guardare request.session['dottore_id']
            dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

            # fuso orario, oggi/domani...
            now_local = timezone.localtime(timezone.now())
            today = now_local.date()
            tomorrow = today + timedelta(days=1)

            notifications = []
            # Appuntamenti di oggi per il dottore loggato
            todays_appts = Appointment.objects.filter(data=today, dottore=dottore)
            for appt in todays_appts:
                appt_time = appt.orario.strftime('%H:%M') if appt.orario else ""
                message = f"Oggi alle {appt_time} hai un appuntamento con {appt.nome_paziente} {appt.cognome_paziente}"
                notifications.append({"message": message, "type": "info"})
            
            # Appuntamenti di domani per il dottore loggato
            tomorrows_appts = Appointment.objects.filter(data=tomorrow, dottore=dottore)
            count_tomorrow = tomorrows_appts.count()
            if count_tomorrow > 0:
                message = f"Domani hai {count_tomorrow} appuntamenti in programma, vai nella sezione appuntamenti per visionarli."
                notifications.append({"message": message, "type": "warning"})
            
            return JsonResponse({"success": True, "notifications": notifications})
        
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
        
# VIEW PER LA SEZIONE PROFILO
def save(self, *args, **kwargs):
    if self.password and not self.password.startswith('pbkdf2_sha256$'):
        self.password = make_password(self.password)
    super().save(*args, **kwargs)

@method_decorator(catch_exceptions, name='dispatch')
class ProfileView(LoginRequiredMixin, View):

    login_url = 'loginPage'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        is_gmail_connected = UserSocialAuth.objects.filter(
            user__email=dottore.email, provider='google-oauth2'
        ).exists()

        return render(request, 'includes/profile.html', {
            'dottore': dottore,
            'gmail_linked': is_gmail_connected,
        })

    def post(self, request, *args, **kwargs):
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        action = request.POST.get("action")

        if action == "update_profile":
            nome     = request.POST.get('name')
            email    = request.POST.get('email')
            password = request.POST.get('password')

            # 1) aggiorno il modello UtentiRegistratiCredenziali
            if nome:
                dottore.nome = nome
            if email:
                dottore.email = email
            if password:
                # salvo hashata nel tuo modello
                dottore.password = make_password(password)
            dottore.save()

            # 2) aggiorno il Django User
            user = request.user
            if email:
                user.email = email
                user.username = email
            if password:
                user.set_password(password)
            user.save()

            # 3) mantengo la sessione attiva se cambio password
            if password:
                update_session_auth_hash(request, user)

            messages.success(request, "Profilo e password aggiornati con successo.")
            return redirect("profile")

        elif action == "update_gmail":
            check_value = request.POST.get('check') == "SI"
            dottore.cookie = "SI" if check_value else ""
            dottore.save(update_fields=['cookie'])

            if not check_value:
                try:
                    social_account = UserSocialAuth.objects.get(
                        user__email=dottore.email, provider="google-oauth2"
                    )
                    social_account.delete()
                    messages.success(request, "Account Gmail disconnesso con successo.")
                except UserSocialAuth.DoesNotExist:
                    messages.info(request, "Nessun account Gmail collegato.")
            else:
                # rimando al flusso di Google OAuth
                return redirect("/auth/login/google-oauth2/?prompt=consent&access_type=offline")

            return redirect("profile")

        # se niente action valida
        messages.error(request, "Azione non riconosciuta.")
        return redirect("profile")




#----------------------------------------
#--------- SEZIONE APPUNTAMENTI ---------
#----------------------------------------

# VIEWS APPUNTAMENTI
@method_decorator(catch_exceptions, name='dispatch')
class AppuntamentiView(LoginRequiredMixin,View):
    def get(self, request):
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persone = TabellaPazienti.objects.filter(dottore=dottore).order_by('-id')
        appuntamenti = Appointment.objects.filter(dottore=dottore).order_by('-id')


        # Ottieni le opzioni definite nei choices
        tipologia_appuntamenti = [choice[0] for choice in Appointment._meta.get_field('tipologia_visita').choices]
        numero_studio = [choice[0] for choice in Appointment._meta.get_field('numero_studio').choices]
        voce_prezzario = Appointment._meta.get_field('voce_prezzario').choices

        context = {
            'dottore': dottore,
            'persone': persone,
            'appuntamenti': appuntamenti,
            'tipologia_appuntamenti': tipologia_appuntamenti,
            'voce_prezzario': voce_prezzario,
            'numero_studio': numero_studio,
        }

        return render(request, 'includes/Appuntamenti.html', context)
    
# VIEWS PER IL SALVATAGGIO DELL'APPUNTAMENTO
@method_decorator(catch_exceptions, name='dispatch')
class AppuntamentiSalvaView(LoginRequiredMixin,View):
    def post(self, request):
        if request.method == "POST":
            try:
                body_raw = request.body.decode('utf-8')
                dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
                data = json.loads(body_raw)

                # Recuperiamo i dati, facendo attenzione ai valori mancanti
                giorno = data.get("giorno", "").strip()
                data_appointment = data.get("data", "").strip()
                time_appointment = data.get("orario", "").strip()
                voce_prezzario = data.get("voce_prezzario", "").strip()
                durata = data.get("durata", "").strip()

                if not time_appointment:
                    print("❌ ERRORE: Il campo 'orario' è mancante o vuoto!")

                # Creazione dell'appuntamento
                Appointment.objects.create(
                    tipologia_visita=data.get("tipologia_visita"),
                    nome_paziente=data.get("nome_paziente"),
                    cognome_paziente=data.get("cognome_paziente"),
                    numero_studio=data.get("numero_studio"),
                    note=data.get("note"),
                    giorno=giorno,
                    data=data_appointment,
                    orario=time_appointment,
                    voce_prezzario=voce_prezzario,
                    durata=durata,
                    dottore=dottore
                )

                return JsonResponse({"success": True, "message": "Appuntamento salvato correttamente!", 'clear_form': True})

            except json.JSONDecodeError as e:
                print(f"❌ ERRORE JSON: {str(e)}")
                return JsonResponse({"success": False, "error": "Formato JSON non valido"}, status=400)
            except Exception as e:
                print(f"❌ ERRORE GENERICO: {str(e)}")
                return JsonResponse({"success": False, "error": str(e)}, status=500)

        return JsonResponse({"success": False, "error": "Metodo non consentito"}, status=405)

# VIEWS SINGLE APPOINTMENT
@method_decorator(catch_exceptions, name='dispatch')
class GetSingleAppointmentView(LoginRequiredMixin,View):
    def get(self, request, appointment_id):
        """Recupera i dettagli di un singolo appuntamento"""
        try:
            dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
            appointment = get_object_or_404(Appointment, id=appointment_id, dottore=dottore)

            response_data = {
                "success": True,
                "id": appointment.id,
                "nome_paziente": appointment.nome_paziente,
                "cognome_paziente": appointment.cognome_paziente,
                "giorno": appointment.giorno,
                "data": appointment.data.strftime("%Y-%m-%d"),
                "numero_studio": appointment.numero_studio or "",  # Se è null, assegna ""
                "note": appointment.note or "",  # Se è null, assegna ""
                "voce_prezzario": appointment.voce_prezzario or "",  # Se è null, assegna ""
                "tipologia_visita": appointment.tipologia_visita or "",  # Se è null, assegna ""
                "orario": str(appointment.orario)[:5],  # Formattato in HH:mm
                "durata": appointment.durata or "",  # Se è null, assegna ""
            }

            return JsonResponse(response_data)
        except Appointment.DoesNotExist:
            return JsonResponse({"success": False, "error": "Appuntamento non trovato"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

# VIEWS GET ALL APPOINTMENTS
@method_decorator(catch_exceptions, name='dispatch')
class AppuntamentiGetView(LoginRequiredMixin,View):
    def get(self, request):
        """Recupera gli appuntamenti futuri o di oggi"""
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        
        # 📌 1. Ottenere la data di oggi senza ore/minuti/secondi
        today = now().date()

        # 📌 2. Eliminare gli appuntamenti con data precedente a oggi
        deleted_count= 0

        # 📌 3. Recuperare solo gli appuntamenti futuri o di oggi
        future_appointments = Appointment.objects.filter(
            data__gte=today,
            dottore=dottore
        )

        # 📌 4. Costruire il dizionario degli appuntamenti organizzati per data
        appointments_by_date = {}
        for appointment in future_appointments:
            date_str = appointment.data.strftime("%Y-%m-%d")  # Formattazione YYYY-MM-DD
            if date_str not in appointments_by_date:
                appointments_by_date[date_str] = []
            appointments_by_date[date_str].append({
                "id": appointment.id,
                "nome_paziente": appointment.nome_paziente,
                "cognome_paziente": appointment.cognome_paziente,
                "giorno": appointment.giorno,
                "data": appointment.data,
                "numero_studio": appointment.numero_studio,
                "note": appointment.note,
                "voce_prezzario": appointment.voce_prezzario,
                "tipologia_visita": appointment.tipologia_visita,
                "orario": appointment.orario,
            })

        return JsonResponse({"success": True, "deleted": deleted_count, "appointments": appointments_by_date})

# VIEWS UPDATE APPOINTMENT
@method_decorator(catch_exceptions, name='dispatch')
class UpdateAppointmentView(LoginRequiredMixin,View):
    def patch(self, request, appointment_id):
        try:
            data = json.loads(request.body)
            appointment = Appointment.objects.get(id=appointment_id)
            
            # Aggiorna solo se i valori sono presenti e non vuoti nel payload
            if data.get("new_date"):
                appointment.data = data["new_date"]
            if data.get("new_time"):
                appointment.orario = data["new_time"]
            if data.get("nome_paziente"):
                appointment.nome_paziente = data["nome_paziente"]
            if data.get("cognome_paziente"):
                appointment.cognome_paziente = data["cognome_paziente"]
            if data.get("tipologia_visita"):
                appointment.tipologia_visita = data["tipologia_visita"]
            if data.get("numero_studio"):
                appointment.numero_studio = data["numero_studio"]
            if data.get("voce_prezzario"):
                appointment.voce_prezzario = data["voce_prezzario"]
            if "note" in data:  # anche se è vuota, la nota verrà aggiornato
                appointment.note = data["note"]
            
            appointment.save()
            return JsonResponse({"success": True, "message": "Appuntamento aggiornato!"})
        except Appointment.DoesNotExist:
            return JsonResponse({"success": False, "error": "Appuntamento non trovato"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

# VIEWS APPROVE APPOINTMENT
@method_decorator(catch_exceptions, name='dispatch')
class ApproveAppointmentView(LoginRequiredMixin,View):
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.confermato = True  # Segna l'appuntamento come confermato
        appointment.save()
        return JsonResponse({"success": True, "message": "Appuntamento confermato!"})

# VIEWS DELETE APPOINTMENT
@method_decorator(catch_exceptions, name='dispatch')
class DeleteAppointmentView(View):
    def post(self, request, appointment_id):  # 👈 aggiungi questo
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            return JsonResponse({"success": True, "message": "Appuntamento eliminato con successo!"})
        except Appointment.DoesNotExist:
            return JsonResponse({"success": False, "error": "Appuntamento non trovato"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

# VIEW SEARCH APPOINTMENTS
@method_decorator(catch_exceptions, name='dispatch')
class SearchAppointmentsView(LoginRequiredMixin,View):
    def get(self, request):
        query = request.GET.get("q", "").lower().strip()
        if query:
            # Puoi estendere il filtro a più campi, ad esempio:
            appointments = Appointment.objects.filter(
                Q(nome_paziente__icontains=query) | Q(tipologia_visita__icontains=query) | Q(orario__icontains=query)
            )
            results = list(appointments.values("id", "nome_paziente", "tipologia_visita", "orario"))
            return JsonResponse({"success": True, "appointments": results})
        return JsonResponse({"success": False, "error": "Nessuna query fornita"})
    
# VIEW CREATE PATIENT FROM SECOND MODAL
@method_decorator(catch_exceptions, name='dispatch')
class CreaPazienteView(LoginRequiredMixin,View):

    login_url = 'loginPage'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
            name = data.get("name", "").strip()
            surname = data.get("surname", "").strip()
            phone = data.get("phone", "").strip()
            email = data.get("email", "").strip() 
            
            if not name or not surname:
                return JsonResponse({"success": False, "error": "Nome e cognome sono obbligatori!"}, status=400)

            if not dottore:
                return JsonResponse({"success": False, "error": "Devi essere autenticato per aggiungere un paziente."}, status=403)
            
            # Creazione paziente
            paziente = TabellaPazienti.objects.create(
                name=name,
                surname=surname,
                phone=phone,
                email=email,
                dottore=dottore
            )

            return JsonResponse({
                "success": True,
                "message": "Paziente aggiunto con successo!",
                "id": paziente.id,
                "full_name": f"{paziente.name} {paziente.surname}"
            })

        except json.JSONDecodeError:
            #print("❌ Errore JSON ricevuto nel backend!")  # DEBUG
            return JsonResponse({"success": False, "error": "Formato JSON non valido."}, status=400)

        except Exception as e:
            #print(f"❌ Errore nel backend: {e}")  # DEBUG
            return JsonResponse({"success": False, "error": str(e)}, status=500)





#----------------------------------------
# ------ SEZIONE RICERCA PAZIENTE -------
#----------------------------------------

# VIEW PER SEZIONE RICERCA PAZIENTI
@method_decorator(catch_exceptions, name='dispatch')
class RisultatiRender(LoginRequiredMixin,View):
    def get(self, request):
          
        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persone = TabellaPazienti.objects.filter(dottore=dottore)
 
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

@method_decorator(catch_exceptions, name='dispatch')
class InserisciPazienteView(LoginRequiredMixin,View):

    def get(self, request):

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        context = {
            'dottore' : dottore
        }
        return render(request, "includes/InserisciPaziente.html", context)  
    
    def post(self, request):
        try:
            success = None
            errore = None
            codice_fiscale = request.POST.get('codice_fiscale')
            
            dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
            context = {'dottore': dottore}

            def parse_date(date_str):
                return date_str if date_str else None

            paziente = TabellaPazienti.objects.filter(dottore=dottore, codice_fiscale=codice_fiscale).first()

            if paziente:
                dati_modificati = False
                for field in TabellaPazienti._meta.get_fields():
                    if not (hasattr(field, 'attname') and field.attname):
                        continue
                    field_name = field.attname
                    if field_name in ['id', 'dottore', 'codice_fiscale', 'created_at']:
                        continue

                    val = request.POST.get(field_name)
                    if val is not None:
                        current_val = getattr(paziente, field_name)
                        new_val = parse_date(val) if isinstance(field, models.DateField) else val
                        if str(current_val) != str(new_val):
                            setattr(paziente, field_name, new_val)
                            dati_modificati = True

                if dati_modificati:
                    paziente.save()
                    success = "I dati del paziente sono stati aggiornati con successo!"
                else:
                    errore = "⚠️ Il paziente esiste già e non sono stati forniti nuovi dati da aggiornare."
            else:
                paziente = TabellaPazienti(
                    dottore=dottore,
                    codice_fiscale=codice_fiscale,
                    name=request.POST.get('name'),
                    surname=request.POST.get('surname'),
                    dob=parse_date(request.POST.get('dob')),
                    gender=request.POST.get('gender'),
                    cap=request.POST.get('cap'),
                    province=request.POST.get('province'),
                    place_of_birth=request.POST.get('place_of_birth'),
                    chronological_age=request.POST.get('chronological_age')
                )

                for field in TabellaPazienti._meta.get_fields():
                    if not (hasattr(field, 'attname') and field.attname):
                        continue
                    field_name = field.attname
                    if field_name in ['id', 'dottore', 'codice_fiscale', 'created_at', 'name', 'surname', 'dob', 'gender', 'cap', 'province', 'place_of_birth', 'chronological_age']:
                        continue

                    val = request.POST.get(field_name)
                    if val:
                        setattr(paziente, field_name, parse_date(val) if isinstance(field, models.DateField) else val)

                paziente.save()
                success = "Nuovo paziente salvato con successo!"

            # 🔽 CREAZIONE REFERTI ETA' METABOLICA SE PRESENTI
            referto_fields = [
                f.attname for f in RefertiEtaMetabolica._meta.get_fields()
                if hasattr(f, 'attname') and f.attname not in ['id', 'dottore', 'paziente', 'data_referto', 'storico_punteggi']
            ]

            if any(request.POST.get(field) for field in referto_fields):
                nuovo_referto = RefertiEtaMetabolica(
                    dottore=dottore,
                    paziente=paziente,
                )

                for field in referto_fields:
                    val = request.POST.get(field)
                    if val:
                        field_obj = RefertiEtaMetabolica._meta.get_field(field)
                        if isinstance(field_obj, models.DateField):
                            setattr(nuovo_referto, field, parse_date(val))
                        elif isinstance(field_obj, models.JSONField):
                            try:
                                setattr(nuovo_referto, field, json.loads(val))
                            except:
                                setattr(nuovo_referto, field, []) 
                        else:
                            setattr(nuovo_referto, field, val)

                nuovo_referto.save()
                success = (success or "") + "Aggiunto nuovo paziente e generato il primo referto metabolico con successo!"

            if success:
                context["success"] = success
            if errore:
                context["errore"] = errore

            return render(request, "includes/InserisciPaziente.html", context)

        except Exception as e:
            context["errore"] = f"Errore di sistema: {str(e)}. Verifica i campi e riprova."
            return render(request, "includes/InserisciPaziente.html", context)










#----------------------------------------
# ------ SEZIONE CARTELLA PAZIENTE ------
#----------------------------------------

# VIEW CARTELLA PAZIENTE
@method_decorator(catch_exceptions, name='dispatch')
class CartellaPazienteView(LoginRequiredMixin,View):

    def get(self, request, id):
         
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=id)

        # DATI PER GLI INDICATORI DI PERFORMANCE
        ## DATI CAPACITA' VITALE
        ultimo_referto_capacita_vitale = persona.referti_test.order_by('-data_ora_creazione').first()

        ##STORICO APPUNTAMENTI
        storico_appuntamenti = Appointment.objects.filter(
            Q(nome_paziente__icontains=persona.name.strip()) |
            Q(cognome_paziente__icontains=persona.surname.strip())
        ).order_by('data', 'orario')


        today = now().date()

        # Totale appuntamenti
        totale_appuntamenti = storico_appuntamenti.count()

        ultimo_appuntamento = storico_appuntamenti.filter(data__lt=today).last() or None
        prossimo_appuntamento = storico_appuntamenti.filter(data__gte=today).first() or None


        ## DATI RESILIENZA


        ## DATI ETA' METABOLICA 
        referti_recenti = persona.referti_eta_metabolica.all().order_by('-data_referto')
        ultimo_referto_eta_metabolica = referti_recenti.first() if referti_recenti.exists() else None

        punteggio_eta_metabolica = ''

        if ultimo_referto_eta_metabolica:
            if ultimo_referto_eta_metabolica.punteggio_finale is not None:
                punteggio_eta_metabolica = ultimo_referto_eta_metabolica.punteggio_finale
            else:
                punteggio_eta_metabolica = ultimo_referto_eta_metabolica.eta_metabolica
        else:
            punteggio_eta_metabolica = None


        ## MICROBIOTA    



        #DATI REFERTI ETA' BIOLOGICA
        referti_recenti = persona.referti.all().order_by('-data_referto')
        dati_estesi = DatiEstesiReferti.objects.filter(referto__in=referti_recenti)
        ultimo_referto = referti_recenti.first() if referti_recenti else None
        
        dati_estesi_ultimo_referto = None
        if ultimo_referto:
            dati_estesi_ultimo_referto = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()
     

        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto,
            'dottore' : dottore,
            'referti_test_recenti': ultimo_referto,

            #ULTIMO REFERTO ETA METABOLICA
            'punteggio_eta_metabolica': punteggio_eta_metabolica,
            #ULTIMO REFERTO CAPACITA' VITALE
            'ultimo_referto_capacita_vitale': ultimo_referto_capacita_vitale,
            'storico_appuntamenti': storico_appuntamenti,
            'totale_appuntamenti': totale_appuntamenti,
            'ultimo_appuntamento': ultimo_appuntamento,
            'prossimo_appuntamento': prossimo_appuntamento,
        }

        return render(request, "includes/cartellaPaziente.html", context)

    def post(self, request, id):
        
        def parse_italian_date(value):
            try:
                return datetime.strptime(value, "%d/%m/%Y").date()
            except (ValueError, TypeError):
                return None


        # ---- DATI NECESSARI AL RENDERING DELLA CARTELLA ----
        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=id)

        persona.codice_fiscale = request.POST.get('codice_fiscale')
        persona.dob = parse_date(request.POST.get('dob'))
        persona.residence = request.POST.get('residence')
        persona.cap = request.POST.get('cap')
        persona.province = request.POST.get('province')
        persona.gender = request.POST.get('gender')
        persona.associate_staff = request.POST.get('associate_staff')
        persona.blood_group = request.POST.get('blood_group')
        persona.email = request.POST.get('email')
        persona.phone = request.POST.get('phone')
        persona.place_of_birth = request.POST.get('place_of_birth')

        persona.dob = parse_italian_date(request.POST.get('dob'))
        persona.lastVisit = parse_italian_date(request.POST.get('lastVisit'))
        persona.upcomingVisit = parse_italian_date(request.POST.get('upcomingVisit'))

        persona.save()

        
        # DATI PER GLI INDICATORI DI PERFORMANCE
        ## DATI CAPACITA' VITALE
        ultimo_referto_capacita_vitale = persona.referti_test.order_by('-data_ora_creazione').first()


        ## DATI RESILIENZA


        ## DATI ETA' METABOLICA 
        referti_recenti = persona.referti_eta_metabolica.all().order_by('-data_referto')
        ultimo_referto_eta_metabolica = referti_recenti.first() if referti_recenti.exists() else None

        ## MICROBIOTA    



        #DATI REFERTI ETA' BIOLOGICA
        referti_recenti = persona.referti.all().order_by('-data_referto')
        dati_estesi = DatiEstesiReferti.objects.filter(referto__in=referti_recenti)
        ultimo_referto = referti_recenti.first() if referti_recenti else None
        
        dati_estesi_ultimo_referto = None
        if ultimo_referto:
            dati_estesi_ultimo_referto = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()


        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto,
            'dottore' : dottore,
            'referti_test_recenti': ultimo_referto,

            #ULTIMO REFERTO ETA METABOLICA
            'ultimo_referto_eta_metabolica': ultimo_referto_eta_metabolica,
            #ULTIMO REFERTO CAPACITA' VITALE
            'ultimo_referto_capacita_vitale': ultimo_referto_capacita_vitale,
            "success" : True,
            
        }

        return render(request, "includes/cartellaPaziente.html", context)

# VIEW STORICO
@method_decorator(catch_exceptions, name='dispatch')
class StoricoView(LoginRequiredMixin,View):
    def get(self, request, id):
        # Recupero Dottore e Paziente
        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=id)
        
        today = timezone.now().date()  # Ottieni la data corrente senza l'orario

        # Filtra gli appuntamenti del paziente in base al nome e cognome
        storico_appuntamenti = Appointment.objects.filter(
            Q(nome_paziente__icontains=persona.name.strip()) &
            Q(cognome_paziente__icontains=persona.surname.strip()) &
            Q(dottore=dottore)  # Aggiungi il filtro per il dottore
        ).order_by('data', 'orario')

        # Impostazione del paginatore (ad es. 10 referti per pagina)
        paginator = Paginator(storico_appuntamenti, 4)
        page_number = request.GET.get('page')
        storico_page = paginator.get_page(page_number)

        # Totale appuntamenti per il paziente
        totale_appuntamenti = storico_appuntamenti.count()

        # Appuntamenti confermati
        appuntamenti_confermati = storico_appuntamenti.filter(confermato=True).count()

        # Calcolo appuntamenti per mese
        appuntamenti_per_mese = storico_appuntamenti.annotate(month=ExtractMonth('data')).values('month').annotate(count=Count('id')).order_by('month')

         # Crea una lista con i conteggi degli appuntamenti per ogni mese (1-12)
        appuntamenti_per_mese_count = [0] * 12  # Inizializza una lista di 12 valori (uno per ogni mese)

        # Appuntamento futuro più vicino (il prossimo)
        prossimo_appuntamento = storico_appuntamenti.filter(data__gte=today).order_by('data').first()

        # Appuntamenti passati (count degli appuntamenti con data < oggi)
        appuntamenti_passati = storico_appuntamenti.filter(data__lt=today).count()

        # Appuntamenti passati (ultimi)
        ultimo_appuntamento = storico_appuntamenti.filter(data__lt=today).last()

        for item in appuntamenti_per_mese:
            # Popola il conteggio per ogni mese (mese - 1 perché i mesi in Python sono indicizzati da 1 a 12)
            appuntamenti_per_mese_count[item['month'] - 1] = item['count']

        context = {
            'dottore': dottore,
            'persona': persona,
            'storico_appuntamenti': storico_appuntamenti,
            'totale_appuntamenti': totale_appuntamenti,
            'appuntamenti_confermati': appuntamenti_confermati,
            'prossimo_appuntamento': prossimo_appuntamento,
            'appuntamenti_passati': appuntamenti_passati,
            'ultimo_appuntamento': ultimo_appuntamento,
            'storico_page': storico_page,
            'appuntamenti_per_mese': appuntamenti_per_mese_count,
        }

        return render(request, 'cartella_paziente/sezioni_storico/storico.html', context)

## VIEW ESAMI
@method_decorator(catch_exceptions, name='dispatch')
class EsamiView(View):
    def get(self, request, id):
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=id)

        context = {
            'persona': persona,
            'dottore': dottore,
        }

        return render(request, 'cartella_paziente/sezioni_storico/esami.html', context)

## VIEW TERAPIA
@method_decorator(catch_exceptions, name='dispatch')
class TerapiaView(View):
    def get(self, request, id):
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=id)

        # Terape in studio (se vuoi mostrarle anche in GET)
        terapie_studio = TerapiaInStudio.objects.filter(paziente=persona).order_by('-created_at')
        terapie_domiciliari = TerapiaDomiciliare.objects.filter(paziente=persona).order_by('-created_at')

        context = {
            'persona': persona,
            'dottore': dottore,
            'terapie_studio': terapie_studio,
            'terapie_domiciliari': terapie_domiciliari
        }

        return render(request, 'cartella_paziente/sezioni_storico/terapie.html', context)

    def post(self, request, id):
        form_type = request.POST.get("form_type")
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        # Salvataggio terapia in studio
        if form_type == "studio":
            persona = get_object_or_404(TabellaPazienti, id=id, dottore=dottore)
            tipologia = request.POST.get("tipologia")
            descrizione = request.POST.get("descrizione")
            data_inizio = parse_date(request.POST.get("data_inizio"))
            data_fine = parse_date(request.POST.get("data_fine")) or None

            terapia = TerapiaInStudio.objects.create(
                paziente=persona,
                tipologia=tipologia,
                descrizione=descrizione,
                data_inizio=data_inizio,
                data_fine=data_fine,
            )

            return JsonResponse({
                'success': True,
                'terapia': {
                    'id': terapia.id,
                    'descrizione': terapia.descrizione,
                    'data_inizio': terapia.data_inizio.strftime('%d/%m/%Y'),
                    'data_fine': terapia.data_fine.strftime('%d/%m/%Y') if terapia.data_fine else None
                }
            })
        elif form_type == "domiciliare":
            persona = get_object_or_404(TabellaPazienti, id=id, dottore=dottore)
            farmaco = request.POST.get("farmaco")
            assunzioni = int(request.POST.get("assunzioni"))
            data_inizio = parse_date(request.POST.get("data_inizio"))
            data_fine = parse_date(request.POST.get("data_fine")) or None

            # Recupero dinamico degli orari
            orari_dict = {}
            for i in range(1, assunzioni + 1):
                key = f"orario{i}"
                orario_val = request.POST.get(key)
                if orario_val:
                    orari_dict[key] = orario_val

            # Creazione
            terapia = TerapiaDomiciliare.objects.create(
                paziente=persona,
                farmaco=farmaco,
                assunzioni=assunzioni,
                orari=orari_dict,
                data_inizio=data_inizio,
                data_fine=data_fine
            )

            return JsonResponse({
                'success': True,
                'terapia': {
                    'id': terapia.id,
                    'farmaco': terapia.farmaco,
                    'assunzioni': terapia.assunzioni,
                    'orari': terapia.orari,
                    'data_inizio': terapia.data_inizio.strftime('%d/%m/%Y') if terapia.data_inizio else None,
                    'data_fine': terapia.data_fine.strftime('%d/%m/%Y') if terapia.data_fine else None
                }
            })


        return JsonResponse({'success': False})

# ELIMINA TERAPIA FUNZIONE
@method_decorator(catch_exceptions, name='dispatch')
class EliminaTerapiaStudioView(View):
    def post(self, request, id):
        terapia = get_object_or_404(TerapiaInStudio, id=id)
        terapia.delete()
        return JsonResponse({'success': True})

## ELIMINA TERAPIA DOMICILIARE
class TerapiaDomiciliareDeleteView(View):
    def post(self, request, id):
        terapia = get_object_or_404(TerapiaDomiciliare, id=id)
        terapia.delete()
        return JsonResponse({'success': True})

# MODIFICA TERAPIA STUDIO
# MODIFICA TERAPIA
@method_decorator(catch_exceptions, name='dispatch')
class ModificaTerapiaStudioView(View):
    def post(self, request, id):
        terapia = get_object_or_404(TerapiaInStudio, id=id)

        terapia.tipologia = request.POST.get('tipologia')
        terapia.descrizione = request.POST.get('descrizione')
        terapia.data_inizio = parse_date(request.POST.get('data_inizio'))
        terapia.data_fine = parse_date(request.POST.get('data_fine')) or None
        terapia.save()

        return JsonResponse({
            'success': True,
            'terapia': {
                'id': terapia.id,
                'descrizione': terapia.descrizione,
                'data_inizio': terapia.data_inizio.strftime('%d/%m/%Y'),
                'data_fine': terapia.data_fine.strftime('%d/%m/%Y') if terapia.data_fine else None
            }
        })

# MODIFICA TERAPIA DOMICILIARE
@method_decorator(csrf_exempt, name='dispatch')
class ModificaTerapiaDomiciliareView(View):
    def post(self, request, id):
        from django.utils.dateparse import parse_date

        terapia = TerapiaDomiciliare.objects.filter(id=id).first()
        if not terapia:
            return JsonResponse({'success': False, 'message': 'Terapia non trovata'}, status=404)

        farmaco = request.POST.get("farmaco")
        assunzioni = int(request.POST.get("assunzioni"))
        data_inizio = parse_date(request.POST.get("data_inizio"))
        data_fine = parse_date(request.POST.get("data_fine")) if request.POST.get("data_fine") else None

        orari_dict = {}
        for i in range(1, assunzioni + 1):
            key = f"orario{i}"
            orario_val = request.POST.get(key)
            if orario_val:
                orari_dict[key] = orario_val

        # Aggiorna i valori
        terapia.farmaco = farmaco
        terapia.assunzioni = assunzioni
        terapia.orari = orari_dict
        terapia.data_inizio = data_inizio
        terapia.data_fine = data_fine
        terapia.save()

        return JsonResponse({'success': True, 'message': 'Terapia aggiornata con successo!'})

# DETTAGLI TERAPIA DOMICILIARE
class DettagliTerapiaDomiciliareView(View):
    def get(self, request, id):
        try:
            terapia = TerapiaDomiciliare.objects.get(id=id)
            return JsonResponse({
                'success': True,
                'terapia': {
                    'id': terapia.id,
                    'farmaco': terapia.farmaco,
                    'assunzioni': terapia.assunzioni,
                    'orari': terapia.orari,
                    'data_inizio': terapia.data_inizio.strftime('%Y-%m-%d') if terapia.data_inizio else '',
                    'data_fine': terapia.data_fine.strftime('%Y-%m-%d') if terapia.data_fine else '',
                }
            })
        except TerapiaDomiciliare.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Terapia non trovata'}, status=404)

## VIEW DIAGNOSI
# VIEW DIAGNOSI
@method_decorator(catch_exceptions, name='dispatch')
class DiagnosiView(View):
    def get(self, request, id):

        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=id)

        # Terape in studio (se vuoi mostrarle anche in GET)
        terapie_studio = TerapiaInStudio.objects.filter(paziente=persona).order_by('-created_at')

        context = {
            'persona': persona,
            'dottore': dottore,
            'terapie_studio': terapie_studio,  # opzionale se la tabella è JS-based
        }

        return render(request, 'cartella_paziente/sezioni_storico/terapie.html', context)

    def post(self, request, id):
        form_type = request.POST.get("form_type")

        # Salvataggio terapia in studio
        if form_type == "studio":
            persona = get_object_or_404(TabellaPazienti, id=id)
            tipologia = request.POST.get("tipologia")
            descrizione = request.POST.get("descrizione")
            data_inizio = parse_date(request.POST.get("data_inizio"))
            data_fine = parse_date(request.POST.get("data_fine")) or None

            terapia = TerapiaInStudio.objects.create(
                paziente=persona,
                tipologia=tipologia,
                descrizione=descrizione,
                data_inizio=data_inizio,
                data_fine=data_fine,
            )

            return JsonResponse({
                'success': True,
                'terapia': {
                    'id': terapia.id,
                    'descrizione': terapia.descrizione,
                    'data_inizio': terapia.data_inizio.strftime('%d/%m/%Y'),
                    'data_fine': terapia.data_fine.strftime('%d/%m/%Y') if terapia.data_fine else None
                }
            })

        return JsonResponse({'success': False})

# ELIMINA TERAPIA FUNZIONE
@method_decorator(catch_exceptions, name='dispatch')
class EliminaTerapiaStudioView(View):
    def post(self, request, id):
        terapia = get_object_or_404(TerapiaInStudio, id=id)
        terapia.delete()
        return JsonResponse({'success': True})

# MODIFICA TERAPIA
@method_decorator(catch_exceptions, name='dispatch')
class ModificaTerapiaStudioView(View):
    def post(self, request, id):
        terapia = get_object_or_404(TerapiaInStudio, id=id)

        terapia.tipologia = request.POST.get('tipologia')
        terapia.descrizione = request.POST.get('descrizione')
        terapia.data_inizio = parse_date(request.POST.get('data_inizio'))
        terapia.data_fine = parse_date(request.POST.get('data_fine')) or None
        terapia.save()

        return JsonResponse({
            'success': True,
            'terapia': {
                'id': terapia.id,
                'descrizione': terapia.descrizione,
                'data_inizio': terapia.data_inizio.strftime('%d/%m/%Y'),
                'data_fine': terapia.data_fine.strftime('%d/%m/%Y') if terapia.data_fine else None
            }
        })

## VIEW DIAGNOSI
@method_decorator(catch_exceptions, name='dispatch')
class DiagnosiView(LoginRequiredMixin,View):
    def get(self, request, id):

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=id)

        context = {
            'persona': persona, 
            'dottore' : dottore,   
        }

        return render(request, 'cartella_paziente/sezioni_storico/diagnosi.html', context)

## SEZIONE MUSCOLO
@method_decorator(catch_exceptions, name='dispatch')
class ValutazioneMSView(LoginRequiredMixin,View):

    def get(self, request, persona_id):

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=persona_id)

        context = {
            'persona': persona,
            'dottore' : dottore,
        }

        return render(request, "cartella_paziente/indici_di_performance/valutazioneMS.html", context)

    def post(self, request, persona_id):     
        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=persona_id)

        try:
            retrivedData = ValutazioneMS.objects.create(
                paziente=persona,

                # Attività fisica
                frequenza_a_f=request.POST.get("frequenza_a_f"),
                tipo_a_f=request.POST.get("tipo_a_f"),
                stile_vita=request.POST.get("stile_vita"),

                # Anamnesi muscolo-scheletrica
                terapie_inf=request.POST.get("terapie_inf"),
                diagnosi_t=request.POST.get("diagnosi_t"),
                sintomi_t=request.POST.get("sintomi_t"),

                # Esame Generale
                palpazione=request.POST.get("palpazione"),
                osservazione=request.POST.get("osservazione"),
                m_attiva=request.POST.get("m_attiva"),
                m_passiva=request.POST.get("m_passiva"),
                dolorabilità=request.POST.get("dolorabilità"),
                scala_v_a=request.POST.get("scala_v_a"),

                # Esame muscolo-scheletrico
                mo_attivo=request.POST.get("mo_attivo"),
                mo_a_limitazioni=request.POST.get("mo_a_limitazioni"),
                mo_passivo=request.POST.get("mo_passivo"),
                mo_p_limitazioni=request.POST.get("mo_p_limitazioni"),
                comparazioni_m=request.POST.get("comparazioni_m"),
                circ_polp=request.POST.get("circ_polp"),
                tono_m=request.POST.get("tono_m"),
                scala_ashworth=request.POST.get("scala_ashworth"),

                # Esame posturale
                v_frontale=request.POST.get("v_frontale"),
                v_laterale=request.POST.get("v_laterale"),
                p_testa=request.POST.get("p_testa"),
                spalle=request.POST.get("spalle"),
                ombelico=request.POST.get("ombelico"),
                a_inferiori=request.POST.get("a_inferiori"),
                piedi=request.POST.get("piedi"),
                colonna_v=request.POST.get("colonna_v"),
                curvatura_c=request.POST.get("curvatura_c"),
                curvatura_d=request.POST.get("curvatura_d"),
                curvatura_l=request.POST.get("curvatura_l"),
                posizione_b=request.POST.get("posizione_b"),
                equilibrio_s=request.POST.get("equilibrio_s"),
                equilibrio_d=request.POST.get("equilibrio_d"),
                p_dolenti=request.POST.get("p_dolenti"),

                # Valutazione funzionale
                gravita_disfunzione_posturale=request.POST.get("gravita_disfunzione_posturale"),
                rischio_infortuni=request.POST.get("rischio_infortuni"),
                suggerimenti=request.POST.get("suggerimenti"),
                considerazioni_finali=request.POST.get("considerazioni_finali"),
            )

            retrivedData.save()

        except Exception as e:
            print("Errore nel salvataggio del referto:", e)

        context = {
            'persona': persona,
            'dottore': dottore,
            'successo': True
        }
        return render(request, "cartella_paziente/indici_di_performance/valutazioneMS.html", context)

## SEZIONE DATI BASE
@method_decorator(catch_exceptions, name='dispatch')
class DatiBaseView(LoginRequiredMixin,View):

    def get(self, request, id):
        persona = get_object_or_404(TabellaPazienti, id=id)

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        context = {
            'persona': persona,
            'dottore' : dottore
        }
        return render(request, "cartella_paziente/dati_base/dati_base.html", context)
    
    def post(self, request, id):

        print(request.POST)

        persona = get_object_or_404(TabellaPazienti, id=id)
        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        try:
            
            #Informazioni occupazione
            persona.professione = request.POST.get("professione") or "No"
            persona.pensionato = request.POST.get("pensionato") or "No"

            #Per la donna
            persona.menarca = request.POST.get('menarca') or "No"
            persona.ciclo = request.POST.get('ciclo') or "No"
            persona.sintomi = request.POST.get('sintomi') or "No"
            persona.esordio = request.POST.get('esordio') or "No"
            persona.parto = request.POST.get('parto') or "No"
            persona.post_parto = request.POST.get('post_parto') or "No"
            persona.aborto = request.POST.get('aborto') or "No"

            # Stile di vita - Alcol
            persona.alcol = request.POST.get("alcol") or "No"
            persona.alcol_type = request.POST.get("alcol_type") or "No"
            persona.data_alcol = request.POST.get("data_alcol")
            persona.alcol_frequency = request.POST.get("alcol_frequency") or "No"

            # Stile di vita - Fumo
            persona.smoke = request.POST.get("smoke") or "No"
            persona.smoke_frequency = request.POST.get("smoke_frequency") or "No"
            persona.reduced_intake = request.POST.get("reduced_intake") or "No"

            # Stile di vita - Sport
            persona.sport = request.POST.get("sport") or "No"
            persona.sport_livello = request.POST.get("sport_livello") or "No"
            persona.sport_frequency = request.POST.get("sport_frequency") or "No"

            # Stile di vita - Sedentarietà
            persona.attivita_sedentaria = request.POST.get("attivita_sedentaria") or "No"
            persona.livello_sedentarieta = request.POST.get("livello_sedentarieta") or "No"
            persona.sedentarieta_nota = request.POST.get("sedentarieta_nota") or "No"

            # Anamnesi
            persona.m_cardiache = request.POST.get("m_cardiache_fam") or "No"
            persona.diabete_m = request.POST.get("diabete_m") or "No"
            persona.ipertensione = request.POST.get("ipertensione") or "No"
            persona.obesita = request.POST.get("obesita") or "No"
            persona.m_tiroidee = request.POST.get("m_tiroidee") or "No"
            persona.m_polmonari = request.POST.get("m_polmonari") or "No"
            persona.tumori = request.POST.get("tumori") or "No"
            persona.allergie = request.POST.get("allergie") or "No"
            persona.m_psichiatriche = request.POST.get("m_psichiatriche") or "No"
            persona.patologie = request.POST.get("patologie") or "No"
            persona.p_p_altro = request.POST.get("p_p_altro") or "No"
            persona.t_farmaco = request.POST.get("t_farmaco") or "No"
            persona.t_dosaggio = request.POST.get("t_dosaggio") or "No"
            persona.t_durata = request.POST.get("t_durata") or "No"

            # Esame Obiettivo
            persona.a_genarale = request.POST.get("a_generale") or "No"
            persona.psiche = request.POST.get("psiche") or "No"
            persona.r_ambiente = request.POST.get("r_ambiente") or "No"
            persona.s_emotivo = request.POST.get("s_emotivo") or "No"
            persona.costituzione = request.POST.get("costituzione") or "No"
            persona.statura = request.POST.get("statura") or "No"
            persona.s_nutrizionale = request.POST.get("s_nutrizionale") or "No"
            persona.eloquio = request.POST.get("eloquio") or "No"

            # Informazioni del sangue
            persona.pressure_min = request.POST.get("pressure_min") or "No"
            persona.pressure_max = request.POST.get("pressure_max") or "No"
            persona.heart_rate = request.POST.get("heart_rate") or "No"
            persona.blood_group = request.POST.get("blood_group") or "No"
            persona.rh_factor = request.POST.get("rh_factor") or "No"

            persona.save()

            context = {
                'persona': persona,
                'dottore': dottore,
                'success': 'I dati sono stati aggiornati correttamente' 
            }

        except Exception as e:
            context = {
                'persona': persona,
                'dottore': dottore,
                'errore': f"system error: {str(e)} --- Controlla di aver inserito tutti i dati corretti nei campi necessari e riprova." 
            }
    

        return render(request, "cartella_paziente/dati_base/dati_base.html", context)  


## SEZIONE ETA' METABOLICA
@method_decorator(catch_exceptions, name='dispatch')
class ComposizioneView(LoginRequiredMixin,View):

    def get(self, request, id):

        persona = get_object_or_404(TabellaPazienti, id=id)

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        ultimo_referto = RefertiEtaMetabolica.objects.filter(paziente=persona).order_by('-data_referto').first()


        context = {
            'persona': persona,
            'dottore' : dottore,
            'ultimo_referto': ultimo_referto
        }

        return render(request, "cartella_paziente/eta_metabolica/etaMetabolica.html", context)

    def post(self, request, id):

        eta_metabolica_calcolata = None
        success = False
        punteggio = None

        persona = get_object_or_404(TabellaPazienti, id=id)
        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        try:
            bmi_date = request.POST.get("bmi_detection_date")
            girth_date = request.POST.get("girth_date")
            bmi_detection_date = datetime.strptime(bmi_date, "%Y-%m-%d").date() if bmi_date else None
            girth_detection_date = datetime.strptime(girth_date, "%Y-%m-%d").date() if girth_date else None

            # PREPARAZIONE DEI DATI PER IL CALCOLO DELL'ETÀ METABOLICA
            dati_calcolo = {
                'eta': persona.chronological_age,  
                'sesso': persona.gender,  
                'BMI': float(request.POST.get("bmi")) if request.POST.get("bmi") else None,
                'grasso_percento': float(request.POST.get("grasso")) if request.POST.get("grasso") else None,
                'acqua_percento': float(request.POST.get("acqua")) if request.POST.get("acqua") else None,
                'massa_muscolare_percento': float(request.POST.get("massa_muscolare")) if request.POST.get("massa_muscolare") else None,
                'WHR': float(request.POST.get("whr")) if request.POST.get("whr") else None,
                'glicemia': float(request.POST.get("glicemia")) if request.POST.get("glicemia") else None,
                'HbA1c': float(request.POST.get("emoglobina_g")) if request.POST.get("emoglobina_g") else None,
                'HOMA_IR': float(request.POST.get("homa_ir")) if request.POST.get("homa_ir") else None,
                'TyG': float(request.POST.get("tyg")) if request.POST.get("tyg") else None,
                'HDL': float(request.POST.get("hdl")) if request.POST.get("hdl") else None,
                'LDL': float(request.POST.get("ldl")) if request.POST.get("ldl") else None,
                'trigliceridi': float(request.POST.get("trigliceridi")) if request.POST.get("trigliceridi") else None,
                'AST': float(request.POST.get("ast")) if request.POST.get("ast") else None,
                'ALT': float(request.POST.get("alt")) if request.POST.get("alt") else None,
                'GGT': float(request.POST.get("ggt")) if request.POST.get("ggt") else None,
                'bilirubina': float(request.POST.get("bili_t")) if request.POST.get("bili_t") else None,
                'SII': float(request.POST.get("sii")) if request.POST.get("sii") else None,
                'HGS': float(request.POST.get("hgs")) if request.POST.get("hgs") else None,
                'cortisolo': float(request.POST.get("c_plasmatico")) if request.POST.get("c_plasmatico") else None,
            }

            # Proviamo a recuperare il valore dal campo eta_metabolica (se presente)
            input_eta_metabolica = request.POST.get("eta_metabolica")
            try:
                input_eta_metabolica_val = float(input_eta_metabolica) if input_eta_metabolica and input_eta_metabolica.strip() != "" else None
            except ValueError:
                input_eta_metabolica_val = None

            # Se è presente un valore valido nel campo eta_metabolica…
            if input_eta_metabolica_val is not None:
                # Verifica se tutti i dati necessari per il calcolo sono stati inseriti
                if all(value is not None for value in dati_calcolo.values()):
                    eta_metabolica_calcolata = calcola_eta_metabolica(dati_calcolo)
                    punteggio = eta_metabolica_calcolata
                else:
                    # Se non sono stati inseriti tutti i dati, usa il valore fornito
                    punteggio = input_eta_metabolica_val
            else:
                # Se il campo eta_metabolica non è stato fornito, prova a calcolare se ci sono tutti i dati
                if all(value is not None for value in dati_calcolo.values()):
                    eta_metabolica_calcolata = calcola_eta_metabolica(dati_calcolo)
                    punteggio = eta_metabolica_calcolata
                else:
                    success = True

            # Salva il referto nella tabella RefertiEtaMetabolica
            RefertiEtaMetabolica.objects.create(
                dottore=dottore,
                paziente=persona,
                punteggio_finale=eta_metabolica_calcolata,
                # Composizione corporea
                bmi=request.POST.get("bmi"),
                grasso=request.POST.get("grasso"),
                acqua=request.POST.get("acqua"),
                massa_muscolare=request.POST.get("massa_muscolare"),
                bmr=request.POST.get("bmr"),
                whr=request.POST.get("whr"),
                whtr=request.POST.get("whtr"),
                # Profilo glicemico e insulinico
                glicemia=request.POST.get("glicemia"),
                ogtt=request.POST.get("ogtt"),
                emoglobina_g=request.POST.get("emoglobina_g"),
                insulina_d=request.POST.get("insulina_d"),
                curva_i=request.POST.get("curva_i"),
                homa_ir=request.POST.get("homa_ir"),
                tyg=request.POST.get("tyg"),
                # Profilo lipidico
                c_tot=request.POST.get("c_tot"),
                hdl=request.POST.get("hdl"),
                ldl=request.POST.get("ldl"),
                trigliceridi=request.POST.get("trigliceridi"),
                # Profilo epatico
                ast=request.POST.get("ast"),
                alt=request.POST.get("alt"),
                ggt=request.POST.get("ggt"),
                bili_t=request.POST.get("bili_t"),
                # Infiammazione
                pcr=request.POST.get("pcr"),
                hgs=request.POST.get("hgs"),
                sii=request.POST.get("sii"),
                # Stress e antropometria
                c_plasmatico=request.POST.get("c_plasmatico"),
                massa_ossea=request.POST.get("massa_ossea"),
                eta_metabolica=request.POST.get("eta_metabolica"),
                grasso_viscerale=request.POST.get("grasso_viscerale"),
                # Dati anagrafici e misurazioni
                height=request.POST.get("altezza"),
                weight=request.POST.get("weight"),
                p_fisico=request.POST.get("p_fisico"),
                girth_value=request.POST.get("girth_value"),
                girth_notes=request.POST.get("note_addominali"),
                bmi_detection_date=bmi_detection_date,
                girth_date=girth_detection_date
            )

            ultimo_referto = RefertiEtaMetabolica.objects.filter(paziente=persona).order_by('-data_referto').first()

            context = {
                'persona': persona,
                'dottore': dottore,
                'success': success,
                'punteggio': punteggio,
                'ultimo_referto': ultimo_referto
            }

        except Exception as e:
            print(e)
            context = {
                'persona': persona,
                'dottore': dottore,
                'errore': "Controlla di aver inserito tutti i dati corretti nei campi necessari e riprova." 
            }

        return render(request, "cartella_paziente/eta_metabolica/etaMetabolica.html", context)

@method_decorator(catch_exceptions, name='dispatch')
class ComposizioneChartView(LoginRequiredMixin,View):

    def get(self, request, id):
        paziente = get_object_or_404(TabellaPazienti, id=id)
        referti = RefertiEtaMetabolica.objects.filter(paziente=paziente).order_by('data_referto')

        mesi = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giug', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']

        # --- 1) COMPOSIZIONE CORPOREA ---
        dati_bmi = {m: [] for m in mesi}
        dati_muscolo = {m: [] for m in mesi}
        dati_grasso = {m: [] for m in mesi}

        # --- 2) GLICEMICO ---
        dati_glicemia = {m: [] for m in mesi}
        dati_emoglobina = {m: [] for m in mesi}
        dati_insulina = {m: [] for m in mesi}

        # --- 3) LIPIDICO ---
        dati_c_tot = {m: [] for m in mesi}
        dati_hdl = {m: [] for m in mesi}
        dati_ldl = {m: [] for m in mesi}
        dati_trigliceridi = {m: [] for m in mesi}

        # --- 4) EPATICO ---
        dati_ast = {m: [] for m in mesi}
        dati_alt = {m: [] for m in mesi}
        dati_ggt = {m: [] for m in mesi}
        dati_bili_t = {m: [] for m in mesi}

        # --- 5) INFIAMMAZIONE & STRESS (PCR, HGS, SII, c_plasmatico)
        dati_pcr = {m: [] for m in mesi}
        dati_hgs = {m: [] for m in mesi}
        dati_sii = {m: [] for m in mesi}
        dati_c_plasmatico = {m: [] for m in mesi}

        # --- LOOP SU TUTTI I REFERTI ---
        for r in referti:
            mese_index = localtime(r.data_referto).month - 1
            mese_nome = mesi[mese_index]

            # COMPOSIZIONE
            try:
                bmi_val = float(r.bmi.replace(',', '.')) if r.bmi else None
                muscolo_val = float(r.massa_muscolare.replace(',', '.')) if r.massa_muscolare else None
                grasso_val = float(r.grasso.replace(',', '.')) if r.grasso else None
            except:
                bmi_val = muscolo_val = grasso_val = None

            if bmi_val is not None:
                dati_bmi[mese_nome].append(bmi_val)
            if muscolo_val is not None:
                dati_muscolo[mese_nome].append(muscolo_val)
            if grasso_val is not None:
                dati_grasso[mese_nome].append(grasso_val)

            # GLICEMICO
            try:
                glic_val = float(r.glicemia.replace(',', '.')) if r.glicemia else None
                hba1c_val = float(r.emoglobina_g.replace(',', '.')) if r.emoglobina_g else None
                ins_val = float(r.insulina_d.replace(',', '.')) if r.insulina_d else None
            except:
                glic_val = hba1c_val = ins_val = None

            if glic_val is not None:
                dati_glicemia[mese_nome].append(glic_val)
            if hba1c_val is not None:
                dati_emoglobina[mese_nome].append(hba1c_val)
            if ins_val is not None:
                dati_insulina[mese_nome].append(ins_val)

            # LIPIDICO
            try:
                ctot_val = float(r.c_tot.replace(',', '.')) if r.c_tot else None
                hdl_val = float(r.hdl.replace(',', '.')) if r.hdl else None
                ldl_val = float(r.ldl.replace(',', '.')) if r.ldl else None
                trig_val = float(r.trigliceridi.replace(',', '.')) if r.trigliceridi else None
            except:
                ctot_val = hdl_val = ldl_val = trig_val = None

            if ctot_val is not None:
                dati_c_tot[mese_nome].append(ctot_val)
            if hdl_val is not None:
                dati_hdl[mese_nome].append(hdl_val)
            if ldl_val is not None:
                dati_ldl[mese_nome].append(ldl_val)
            if trig_val is not None:
                dati_trigliceridi[mese_nome].append(trig_val)

            # EPATICO
            try:
                ast_val = float(r.ast.replace(',', '.')) if r.ast else None
                alt_val = float(r.alt.replace(',', '.')) if r.alt else None
                ggt_val = float(r.ggt.replace(',', '.')) if r.ggt else None
                bili_val = float(r.bili_t.replace(',', '.')) if r.bili_t else None
            except:
                ast_val = alt_val = ggt_val = bili_val = None

            if ast_val is not None:
                dati_ast[mese_nome].append(ast_val)
            if alt_val is not None:
                dati_alt[mese_nome].append(alt_val)
            if ggt_val is not None:
                dati_ggt[mese_nome].append(ggt_val)
            if bili_val is not None:
                dati_bili_t[mese_nome].append(bili_val)

            # INFIAMMAZIONE & STRESS
            try:
                pcr_val = float(r.pcr.replace(',', '.')) if r.pcr else None
                hgs_val = float(r.hgs.replace(',', '.')) if r.hgs else None
                sii_val = float(r.sii.replace(',', '.')) if r.sii else None
                cplas_val = float(r.c_plasmatico.replace(',', '.')) if r.c_plasmatico else None
            except:
                pcr_val = hgs_val = sii_val = cplas_val = None

            if pcr_val is not None:
                dati_pcr[mese_nome].append(pcr_val)
            if hgs_val is not None:
                dati_hgs[mese_nome].append(hgs_val)
            if sii_val is not None:
                dati_sii[mese_nome].append(sii_val)
            if cplas_val is not None:
                dati_c_plasmatico[mese_nome].append(cplas_val)

        # Funzione per calcolare le medie e avere 12 valori
        def calcola_medie(diz):
            return [
                round(sum(diz[m]) / len(diz[m]), 2) if diz[m] else None
                for m in mesi
            ]

        # COMPOSIZIONE
        bmi_values = calcola_medie(dati_bmi)
        muscolo_values = calcola_medie(dati_muscolo)
        grasso_values = calcola_medie(dati_grasso)

        # GLICEMICO
        glicemia_values = calcola_medie(dati_glicemia)
        hba1c_values = calcola_medie(dati_emoglobina)
        insulina_values = calcola_medie(dati_insulina)

        # LIPIDICO
        c_tot_values = calcola_medie(dati_c_tot)
        hdl_values = calcola_medie(dati_hdl)
        ldl_values = calcola_medie(dati_ldl)
        trigliceridi_values = calcola_medie(dati_trigliceridi)

        # EPATICO
        ast_values = calcola_medie(dati_ast)
        alt_values = calcola_medie(dati_alt)
        ggt_values = calcola_medie(dati_ggt)
        bili_values = calcola_medie(dati_bili_t)

        # INFIAMMAZIONE & STRESS
        pcr_values = calcola_medie(dati_pcr)
        hgs_values = calcola_medie(dati_hgs)
        sii_values = calcola_medie(dati_sii)
        cplas_values = calcola_medie(dati_c_plasmatico)

        # Passiamo tutto in JSON
        context = {
            'persona': paziente,

            # Composizione
            'bmi': json.dumps(bmi_values),
            'massa_muscolare': json.dumps(muscolo_values),
            'grasso': json.dumps(grasso_values),

            # Glicemico
            'glicemia': json.dumps(glicemia_values),
            'hba1c': json.dumps(hba1c_values),
            'insulina': json.dumps(insulina_values),

            # Lipidico
            'col_tot': json.dumps(c_tot_values),
            'hdl': json.dumps(hdl_values),
            'ldl': json.dumps(ldl_values),
            'trigliceridi': json.dumps(trigliceridi_values),

            # Epatico
            'ast': json.dumps(ast_values),
            'alt': json.dumps(alt_values),
            'ggt': json.dumps(ggt_values),
            'bili_t': json.dumps(bili_values),

            # Infiammazione & Stress
            'pcr': json.dumps(pcr_values),
            'hgs': json.dumps(hgs_values),
            'sii': json.dumps(sii_values),
            'cplas': json.dumps(cplas_values),
        }
        return render(request, 'cartella_paziente/eta_metabolica/grafici.html', context)

@method_decorator(catch_exceptions, name='dispatch')
class RefertiComposizioneView(LoginRequiredMixin,View):
    def get(self, request, id):
        persona = get_object_or_404(TabellaPazienti, id=id)

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        referti = RefertiEtaMetabolica.objects.filter(paziente=persona).order_by('-data_referto')
        
        # Impostazione del paginatore (ad es. 10 referti per pagina)
        paginator = Paginator(referti, 7)
        page_number = request.GET.get('page')
        referti_page = paginator.get_page(page_number)

        context = {
            'persona': persona,
            'dottore': dottore,
            'referti': referti_page, 
        }

        return render(request, 'cartella_paziente/eta_metabolica/elencoReferti.html', context)


## SEZIONE CAPACITA' VITALE
@method_decorator(catch_exceptions, name='dispatch')
class EtaVitaleView(LoginRequiredMixin,View):

    def get(self, request, id):

        persona = get_object_or_404(TabellaPazienti, id=id)
  
        referti_test_recenti = persona.referti_test.all().order_by('-data_ora_creazione')
    
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        context = {
            'persona': persona,
            'referti_test_recenti': referti_test_recenti,
            'dottore': dottore
        }

        return render(request, "cartella_paziente/capacita_vitale/EtaVitale.html", context)
    
    def post(self):
        return

@method_decorator(catch_exceptions, name='dispatch')
class TestEtaVitaleView(LoginRequiredMixin,View):

    def get(self,request, id):

        persona = get_object_or_404(TabellaPazienti, id=id)

        ultimo_referto = persona.referti.order_by('-data_referto').first()
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
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

        return render(request, "cartella_paziente/capacita_vitale/testVitale.html", context)
 
    def post(self, request, id):

        try:
            persona = get_object_or_404(TabellaPazienti, id=id)
            data = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}
            referti_test_recenti = persona.referti_test.all().order_by('-data_ora_creazione')
            dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

            Somma_MMSE = (
                int(data.get('doc_1', 0)) +
                int(data.get('doc_2', 0)) +
                int(data.get('doc_3', 0)) +
                int(data.get('doc_4', 0)) +
                int(data.get('doc_5', 0)) +
                int(data.get('doc_6', 0)) +
                int(data.get('doc_7', 0)) +
                int(data.get('doc_8', 0)) +
                int(data.get('doc_9', 0)) +
                int(data.get('doc_10', 0)) +
                int(data.get('doc_11', 0)) 
            )

            Somma_GDS = (
                int(data.get('dop_1', 0)) +
                int(data.get('dop_2', 0)) +
                int(data.get('dop_3', 0)) +
                int(data.get('dop_4', 0)) +
                int(data.get('dop_5', 0)) +
                int(data.get('dop_6', 0)) +
                int(data.get('dop_7', 0)) +
                int(data.get('dop_8', 0)) +
                int(data.get('dop_9', 0)) +
                int(data.get('dop_10', 0)) +
                int(data.get('dop_11', 0)) +
                int(data.get('dop_12', 0)) +
                int(data.get('dop_13', 0)) +
                int(data.get('dop_14', 0)) +
                int(data.get('dop_15', 0)) 
            )

            Somma_LOC = (
                int(data.get('loc_1', 0)) +
                int(data.get('loc_2', 0)) +
                int(data.get('loc_3', 0)) +
                int(data.get('loc_4', 0)) +
                int(data.get('loc_5', 0)) +
                int(data.get('loc_6', 0)) +
                int(data.get('loc_7', 0)) +
                int(data.get('loc_8', 0)) 
            )

            Somma_Vista = (
                int(data.get('dos_1', 0)) +
                int(data.get('dos_2', 0))
            )

            Somma_Udito =  int(data.get('dos_3', 0)) 

            Somma_HGS = str(data.get('dodv', None))

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
          
            PFT = int(data.get('pft-1', '0') or 0)
         
            ISQ = (
                int(data.get('SiIm_1', 0)) +
                int(data.get('SiIm_2', 0)) +
                int(data.get('SiIm_3', 0)) +
                int(data.get('SiIm_4', 0)) +
                int(data.get('SiIm_5', 0)) +
                int(data.get('SiIm_6', 0)) +
                int(data.get('SiIm_7', 0))
            )   
    
            BMI = float(data.get('bmi-1', 0) or 0)
            CDP = float(data.get('Cir_Pol', 0) or 0)
            WHR = float(data.get('WHip', 0) or 0)
            WHR_Ratio = str(data.get('Whei', None))

            CST = int(data.get('numero_rip', 0) or 0) / int(data.get('tot_secondi', 0) or 1)
           
            GS = int(data.get('distanza', 0) or 0) / int(data.get('tempo_s', 0) or 1)
       
            PPT = int(data.get('tempo_s_pick', 0) or 1)
    
            punteggioFinale = CalcoloPunteggioCapacitaVitale(
                                Somma_MMSE, Somma_GDS, Somma_LOC,
                                Somma_Vista, Somma_Udito, Somma_HGS, PFT,
                                ISQ, BMI, CDP, WHR, WHR_Ratio, CST, 
                                GS, PPT, Sarc_f_Somma, persona.gender )


            referto = ArchivioRefertiTest(
                paziente = persona,
                punteggio = punteggioFinale,
                #documento = request.FILES.get('documento')
            )
            referto.save()


            datiEstesi = DatiEstesiRefertiTest(
                referto = referto,

                #DOMINIO COGNITIVO 
                MMSE = Somma_MMSE,

                #DOMINIO PSICOLOGICO
                GDS = Somma_GDS,
                LOC = Somma_LOC,

                #DOMINIO SENSORIALE
                Vista = Somma_Vista,
                Udito = Somma_Udito,

                #DOMINIO DELLA VITALITA'
                HGS = Somma_HGS,
                PFT = PFT,

                #SISTEMA IMMUNITARIO
                ISQ = ISQ,
                BMI = BMI,
                CDP = CDP,
                WHR = WHR,
                WHR_Ratio = WHR_Ratio,

                #DOMINIO DELLA LOCOMOZIONE
                CST = CST,
                GS = GS,
                PPT = PPT,
                SARC_F = Sarc_f_Somma,
                FSS = Fss_Somma,

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


                #BIOMARCATORI CIRCOLANTI DELL'INFIAMMAZIONE
                Lymph = safe_float(data, 'Lymph'),
                Lymph_el = safe_float(data, 'Lymph_el'),
                wbc = safe_float(data, 'wbc'),
                Proteins_c = safe_float(data, 'Proteins_c'),
                Inter_6 = safe_float(data, 'Inter_6'),
                Tnf = safe_float(data, 'Tnf'),
                Mono = safe_float(data, 'Mono'),
                Mono_el = safe_float(data, 'Mono_el'),    
            )

            datiEstesi.save()

            context = {
            'persona': persona,
            'modal' : True,
            'Referto': referto,
            'referti_test_recenti': referti_test_recenti,
            'dottore': dottore
            }

            return render(request, "cartella_paziente/capacita_vitale/EtaVitale.html", context)

        except Exception as e:
            print(e)

            context = {
                'persona': persona,
                'modal': False,
                'errore': "Qualcosa è andato storto, controlla di inserire i valori corretti e riprova",
                'referti_test_recenti': referti_test_recenti,
                'dottore': dottore
            }    

            return render(request, "cartella_paziente/capacita_vitale/testVitale.html", context)

@method_decorator(catch_exceptions, name='dispatch')
class RefertoQuizView(LoginRequiredMixin,View):
    def get(self, request, persona_id, referto_id):

        persona = get_object_or_404(TabellaPazienti, id=persona_id)

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        referto = get_object_or_404(ArchivioRefertiTest, id=referto_id)

        ultimo_referto = persona.referti.order_by('-data_referto')
        
        datiEstesi = None
        if referto:
            datiEstesi = DatiEstesiRefertiTest.objects.filter(referto=referto).first()

        testo_risultato = ''

        if float(referto.punteggio) >= 0 and float(referto.punteggio) <= 2.59:
            testo_risultato = """
                                Ottima capacità vitale: Stato di salute eccellente sia a livello
                                fisico che mentale. La forza muscolare, la funzionalità
                                respiratoria e la mobilità sono ottimali. Il soggetto mostra
                                un’ottima capacità cognitiva, un buon benessere psicologico e
                                una bassa vulnerabilità allo stress. Il rischio di declino
                                funzionale e mentale è minimo.
                            """

        elif float(referto.punteggio) >= 2.60 and float(referto.punteggio) <= 5.09:
            testo_risultato = """
                                Buona capacità vitale: Buono stato di salute con lievi segni di
                                riduzione della forza muscolare o della resistenza fisica.
                                Possibile lieve declino cognitivo o stati emotivi fluttuanti, come
                                stress occasionale o lieve ansia. Il soggetto è autonomo, ma
                                potrebbe beneficiare di interventi per mantenere le capacità
                                motorie e il benessere mentale.
                            """

        elif float(referto.punteggio) >= 5.10 and float(referto.punteggio) <= 7.59:
            testo_risultato ="""
                                Capacità vitale compromessa: Si evidenziano difficoltà motorie
                                moderate, minore forza muscolare e resistenza. Potrebbero
                                esserci segni di declino cognitivo o un aumento di ansia e
                                stress, con possibili difficoltà nella gestione emotiva. Il rischio
                                di cadute, affaticamento mentale e riduzione dell’autonomia
                                cresce. È consigliato un supporto medico e strategie di
                                miglioramento.
                            """

        elif float(referto.punteggio) >= 7.60 and float(referto.punteggio) <= 10:
            testo_risultato ="""
                                Capacità vitale gravemente compromessa: Mobilità e
                                resistenza fisica sono compromesse, con elevato rischio di
                                fragilità e perdita di autonomia. Il declino cognitivo può
                                manifestarsi con difficoltà di concentrazione, memoria e
                                orientamento. Sul piano psicologico, possono essere presenti
                                ansia significativa, depressione o distress emotivo. È necessario
                                un intervento mirato per migliorare la qualità della vita.
                            """


        context = {
            'persona': persona,
            'ultimo_referto': ultimo_referto,
            'datiEstesi': datiEstesi,
            'dottore' : dottore,
            'referto' : referto,
            'testo_risultato': testo_risultato,
        }

        return render(request, "cartella_paziente/capacita_vitale/RefertoQuiz.html", context)

@method_decorator(catch_exceptions, name='dispatch')
class QuizEtaVitaleUpdateView(LoginRequiredMixin,View):

    def get(self, request, id):
        
        persona = get_object_or_404(TabellaPazienti, id=id)

        ultimo_referto = persona.referti.order_by('-data_referto').first()
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        referti_test_recenti = persona.referti_test.all().order_by('-data_ora_creazione')

        dati_estesi = None
        if ultimo_referto:
            dati_estesi = DatiEstesiReferti.objects.filter(referto=ultimo_referto).first()

        card_to_show = request.GET.get('card_name')

        context = {
            'persona': persona,
            'dati_estesi': dati_estesi,
            'dottore' : dottore,
            'referti_test_recenti': referti_test_recenti,
            'card_to_show': card_to_show
        }

        return render(request, 'includes/testVitale.html', context)
    
    def post(self, request, id):
        return 

@method_decorator(catch_exceptions, name='dispatch')
class StampaRefertoView(LoginRequiredMixin,View):
    def get(self, request, persona_id, referto_id):

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, dottore=dottore, id=persona_id)
        referto = get_object_or_404(ArchivioRefertiTest, id=referto_id)
        referti_test_recenti = persona.referti_test.all().order_by('-data_ora_creazione')
        ultimo_referto = persona.referti.order_by('-data_referto')
        
        datiEstesi = None
        if referto:
            datiEstesi = DatiEstesiRefertiTest.objects.filter(referto=referto).first()

        testo_risultato = ''

        if float(referto.punteggio) >= 0 and float(referto.punteggio) <= 2.59:
            testo_risultato = """
                                Ottima capacità vitale: Stato di salute eccellente sia a livello
                                fisico che mentale. La forza muscolare, la funzionalità
                                respiratoria e la mobilità sono ottimali. Il soggetto mostra
                                un’ottima capacità cognitiva, un buon benessere psicologico e
                                una bassa vulnerabilità allo stress. Il rischio di declino
                                funzionale e mentale è minimo.
                            """

        elif float(referto.punteggio) >= 2.60 and float(referto.punteggio) <= 5.09:
            testo_risultato = """
                                Buona capacità vitale: Buono stato di salute con lievi segni di
                                riduzione della forza muscolare o della resistenza fisica.
                                Possibile lieve declino cognitivo o stati emotivi fluttuanti, come
                                stress occasionale o lieve ansia. Il soggetto è autonomo, ma
                                potrebbe beneficiare di interventi per mantenere le capacità
                                motorie e il benessere mentale.
                            """

        elif float(referto.punteggio) >= 5.10 and float(referto.punteggio) <= 7.59:
            testo_risultato ="""
                                Capacità vitale compromessa: Si evidenziano difficoltà motorie
                                moderate, minore forza muscolare e resistenza. Potrebbero
                                esserci segni di declino cognitivo o un aumento di ansia e
                                stress, con possibili difficoltà nella gestione emotiva. Il rischio
                                di cadute, affaticamento mentale e riduzione dell’autonomia
                                cresce. È consigliato un supporto medico e strategie di
                                miglioramento.
                            """

        elif float(referto.punteggio) >= 7.60 and float(referto.punteggio) <= 10:
            testo_risultato ="""
                                Capacità vitale gravemente compromessa: Mobilità e
                                resistenza fisica sono compromesse, con elevato rischio di
                                fragilità e perdita di autonomia. Il declino cognitivo può
                                manifestarsi con difficoltà di concentrazione, memoria e
                                orientamento. Sul piano psicologico, possono essere presenti
                                ansia significativa, depressione o distress emotivo. È necessario
                                un intervento mirato per migliorare la qualità della vita.
                            """

        context = {
            'scarica' : True,
            'persona': persona,
            'ultimo_referto': ultimo_referto,
            'datiEstesi': datiEstesi,
            'referti_test_recenti': referti_test_recenti,
            'dottore' : dottore,
            'referto' : referto,
            'testo_risultato': testo_risultato,
        }

        return render(request, "cartella_paziente/capacita_vitale/EtaVitale.html", context)


## SEZIONE ETA' BIOLOGICA
def safe_float(data, key, default=0.0):
    try:
        return float(data.get(key, default))
    except (ValueError, TypeError):
        return default

@method_decorator(catch_exceptions, name='dispatch')
class CalcolatoreRender(LoginRequiredMixin,View):
    
    def get(self, request, id):

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        persona = get_object_or_404(TabellaPazienti, id=id)

        context = {
            'dottore' : dottore,
            'persona': persona,
        }

        codice_fiscale = request.GET.get('parametro')

        if codice_fiscale:
            try:
                paziente = TabellaPazienti.objects.get(dottore=dottore, codice_fiscale=codice_fiscale)
                context.update({
                    "paziente": paziente,
                    "id_persona": paziente.id
                })
            except TabellaPazienti.DoesNotExist:
                context.update({"error": "Paziente non trovato."})

            return render(request, 'cartella_paziente/eta_biologica/calcolatore.html', context)
        
        else:
            return render(request, 'cartella_paziente/eta_biologica/calcolatore.html', context)

        
    def post(self, request, id):
        data = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}
        

        persona = get_object_or_404(TabellaPazienti, id=id)

        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        try:

            paziente = TabellaPazienti.objects.filter(
                dottore=dottore,
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
                        'dottore': dottore,
                        "persona": persona
                    }

                    return render(request, "cartella_paziente/eta_biologica/calcolatore.html", context)
                
                else:
                    
                    context = {
                        "show_modal": False,
                        "error": "Operazione non andata a buon fine: 'Un Utente con questo Codice Fiscale è gia presente all'interno del database'. ",
                        "data": data,
                        'dottore': dottore,
                        'persona': persona
                    }
                    return render(request, "cartella_paziente/eta_biologica/calcolatore.html", context)

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

                return render(request, "cartella_paziente/eta_biologica/calcolatore.html", context)

        except Exception as e:
            error_message = f"System error: {str(e)}\n{traceback.format_exc()}"
            print(error_message)

            context = {
                "error": "Si è verificato un errore di sistema. Controlla di aver inserito tutti i dati corretti nei campi necessari e riprova.",
                "dettaglio": error_message 
            }
            return render(request, "cartella_paziente/eta_biologica/calcolatore.html", context)

@method_decorator(catch_exceptions, name='dispatch')
class ElencoRefertiView(LoginRequiredMixin,View):

    def get(self, request, id):
        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=id)
        
        #DATI REFERTI ETA' BIOLOGICA
        referti_recenti = persona.referti.all().order_by('-data_referto')
        dati_estesi = DatiEstesiReferti.objects.filter(referto__in=referti_recenti)
        
        dati_estesi_ultimo_referto = None

        context = {
            'persona': persona,
            'referti_recenti': referti_recenti,
            'dati_estesi': dati_estesi,
            'dati_estesi_ultimo_referto': dati_estesi_ultimo_referto,
            'dottore' : dottore,
        }

        return render(request, "cartella_paziente/eta_biologica/elencoReferti.html", context)
   
@method_decorator(catch_exceptions, name='dispatch')
class PersonaDetailView(LoginRequiredMixin,View):
    def get(self, request, persona_id):

        # RECUPERO DOTTORE
        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        # RECUPERO PAZIENTE
        persona = get_object_or_404(TabellaPazienti, dottore=dottore, id=persona_id)

        # Recupera l'ID del referto dalla query string
        referto_id = request.GET.get('referto_id')

        # Recupera il referto specifico se l'ID è passato, altrimenti l'ultimo referto
        if referto_id:
            referto = get_object_or_404(ArchivioReferti, id=referto_id, paziente=persona)
        else:
            referto = ArchivioReferti.objects.filter(paziente=persona).order_by("-data_ora_creazione").first()

        # Ottieni i dati estesi associati al referto selezionato
        dati_estesi = DatiEstesiReferti.objects.filter(referto=referto).first() if referto else None

        # Preparazione del contesto per il template
        context = {
            'persona': persona,
            'referto': referto,
            'datiEstesi': dati_estesi,
            'dottore': dottore,
        }
        return render(request, "cartella_paziente/eta_biologica/Referto.html", context)



## SEZIONE RESILIENZA
@method_decorator(catch_exceptions, name='dispatch')
class ResilienzaView(LoginRequiredMixin,View):
    def get(self, request, persona_id):

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=persona_id)

        context = {
            'persona': persona,
            'dottore' : dottore,
        }

        return render(request, "cartella_paziente/resilienza/Resilienza.html", context)
    
    def post(self, request, persona_id): 
        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=persona_id)

        # Estrai i dati dal form (con gestione errori base)
        try:
            retrivedData = Resilienza.objects.create(
                paziente=persona,
                hrv=request.POST.get("hrv"),
                cortisolo=request.POST.get("cortisolo"),
                ros=request.POST.get("ros"),
                osi=request.POST.get("osi"),
                droms=request.POST.get("dRoms"),
                pcr=request.POST.get("pcr"),
                nlr=request.POST.get("nlr"),
                homa=request.POST.get("homa_t"),
                ir=request.POST.get("ir_t"),
                omega_3=request.POST.get("omega_3"),
                vo2max=request.POST.get("vo2"),
            )
            retrivedData.save()

        except Exception as e:
            print("Errore nel salvataggio del referto:", e)

        context = {
            'persona': persona,
            'dottore': dottore,
            'successo': True
        }
        return render(request, "cartella_paziente/resilienza/Resilienza.html", context)
    

## SEZIONE PIANO TERAPEUTICO
@method_decorator(catch_exceptions, name='dispatch')
class PianoTerapeutico(LoginRequiredMixin,View):

    def get(self, request, persona_id):

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)
        persona = get_object_or_404(TabellaPazienti, id=persona_id)

        #ELENCO PRESCRIZIONI ESAMI PAZIENTE
        visite_list = PrescrizioniEsami.objects.filter(paziente=persona).order_by('-data_visita')
        
        paginator = Paginator(visite_list, 5)  
        page_number = request.GET.get('page')
        visite_page = paginator.get_page(page_number)

        context = {
            'persona': persona,
            'dottore' : dottore,
            'visite': visite_page,  
        }

        return render(request, 'cartella_paziente/piano_terapeutico/piano_terapeutico.html', context)

### SEZIONE PRESCRIZIONI ESAMI
@method_decorator(catch_exceptions, name='dispatch')
class PrescrizioniView(LoginRequiredMixin,View):

    def get(self, request, persona_id):

        persona = get_object_or_404(TabellaPazienti, id=persona_id)

        
        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        context = {
            'persona': persona,
            'dottore': dottore,
        }

        return render(request, "cartella_paziente/sezioni_storico/esami.html", context)


    def post(self, request, persona_id):
        persona = get_object_or_404(TabellaPazienti, id=persona_id)
        
        listaCodici = request.POST.get('codici_esami')
        data_list = json.loads(listaCodici)
        numeri = [x for x in data_list if x.isdigit()]

        nuova_visita = PrescrizioniEsami.objects.create(
            paziente=persona,
            esami_prescritti=json.dumps(numeri),
        )

        return redirect('piano_terapeutico', persona_id)

# TO DEFINE
@method_decorator(catch_exceptions, name='dispatch')
class UpdatePersonaContactView(LoginRequiredMixin,View):

    def post(self, request, id):
        
        if request.method == "POST":
            try:
                # Estrai il corpo della richiesta
                data = json.loads(request.body)
                cap = data.get("cap")
                province = data.get("province")
                residence = data.get("residence")
                email = data.get("email")
                phone = data.get("phone")
                associate_staff = data.get("associate_staff")
                lastVisit = data.get("lastVisit")
                upcomingVisit = data.get("upcomingVisit")
                blood_group = data.get("blood_group")

                # Recupera il modello e aggiorna i dati
                from .models import TabellaPazienti  # Sostituisci con il tuo modello
                persona = TabellaPazienti.objects.get(id=id)
                persona.cap = cap
                persona.residence = residence
                persona.province = province
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



    def get(self, request, id):

        persona = get_object_or_404(TabellaPazienti, id=id)
  
        referti_test_recenti = persona.referti_test.all().order_by('-data_ora_creazione')

        dottore = get_object_or_404(UtentiRegistratiCredenziali, user=request.user)

        context = {
            'persona': persona,
            'referti_test_recenti': referti_test_recenti,
            'dottore': dottore
        }

        return render(request, "cartella_paziente/capacita_vitale/EtaVitale.html", context)

@method_decorator(catch_exceptions, name='dispatch')
class RefertoView(LoginRequiredMixin,View):
    def get(self, request, referto_id):
        referto = ArchivioReferti.objects.get(id=referto_id)
        return render(request, 'cartella_paziente/eta_biologica//Referto.html', {'data_referto': referto.data_referto})




