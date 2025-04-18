from django.urls import path # type: ignore
from . import views
from .views import *

urlpatterns = [

    # URL PER LOGIN
    path("",                                                    views.LoginRenderingPage.as_view(),                  name='loginPage'),
    path("logout",                                              LogOutRender.as_view(),                              name="logout"),
    path('accept-disclaimer/',                                  AcceptDisclaimerView.as_view(),                      name='accept_disclaimer'),

    # URL NAVBAR    
    path('accounts/profile/',                                   ProfileView.as_view(),                               name='profile'),

    # -- URL HOME PAGE --
    path("Home_Page",                                           HomePageRender.as_view(),                            name='HomePage'),

    ## URL SIDEBAR
    path('api/appointment-notifications/',                      AppointmentNotificationsView.as_view(),              name='appointment-notifications'),
    path('api/medical-news-notifications/',                     MedicalNewsNotificationsView.as_view(),              name='medical-news-notifications'),

    ## URL HOME PAGE / STATISTICHE
    path("Home_Page/Statistiche",                               views.StatisticheView.as_view(),                     name="statistiche"),

    ## URL APPUNTAMENTI
    path('Home_Page/Appuntamenti',                              views.AppuntamentiView.as_view(),                    name='appuntamenti'),
    path("salva-appuntamento/",                                 views.AppuntamentiSalvaView.as_view(),               name="salva_appuntamento"),
    path('get-appointments/',                                   AppuntamentiGetView.as_view(),                       name='get_appointments'),
    path('get-appointment/<int:appointment_id>/',               GetSingleAppointmentView.as_view(),                  name='get_appointment'),
    path('update-appointment/<int:appointment_id>/',            UpdateAppointmentView.as_view(),                     name='update_appointment'),
    path('delete-appointment/<int:appointment_id>/',            DeleteAppointmentView.as_view(),                     name='delete_appointment'),
    path("api/appointments/<int:appointment_id>/approve/",      views.ApproveAppointmentView.as_view(),              name="approve_appointment"),
    path("api/appointments/<int:appointment_id>/delete/",       views.DeleteAppointmentView.as_view(),               name="delete_appointment"),
    path('search-appointments/',                                SearchAppointmentsView.as_view(),                    name='search_appointments'),

    # -- URL PER LA SEZIONE RICERCA PAZIENTE --
    path("Ricerca_Pazienti",                                    views.RisultatiRender.as_view(),                     name='Risultati'),

    ## URL INSERISCI PAZIENTE
    path("AggiungiPaziente/",                                   views.InserisciPazienteView.as_view(),               name="inserisci_paziente"),
    path("aggiungi-paziente/",                                  views.CreaPazienteView.as_view(),                    name="aggiungi_paziente"),

    # -- URL SEZIONE CARTELLA PAZIENTE --
    ## URL PER LA CARTELLA DEL PAZIENTE
    path("CartellaPaziente/<int:id>/",                          views.CartellaPazienteView.as_view(),                 name="cartella_paziente"),

    ## URL SEZIONI STORICO
    path("CartellaPaziente/<int:id>/Storico",                   views.StoricoView.as_view(),                          name="storico"),
    path("CartellaPaziente/<int:id>/Terapie",                   views.TerapiaView.as_view(),                          name="terapie"),

    ## URL SEZIONE DIAGNOSI
    path("CartellaPaziente/<int:id>/Diagnosi",                  views.DiagnosiView.as_view(),                         name="diagnosi"),

    ## URL SEZIONE TERAPIE
    path("elimina-terapia-studio/<int:id>/", EliminaTerapiaStudioView.as_view(), name="elimina_terapia_studio"),
    path("modifica-terapia-studio/<int:id>/", ModificaTerapiaStudioView.as_view(), name="modifica_terapia_studio"),

    ## SEZIONE MUSCOLO
    path('Valutazione_Muscolo_Scheletrica/<int:persona_id>/',   views.ValutazioneMSView.as_view(),                    name='valutazione_m_s'), 

    ## URL PER SEZIONE DATI BASE 
    path("DatiBase/<int:id>/",                                  views.DatiBaseView.as_view(),                         name="dati_base"),

    ## -- URL SEZIONE ETA' METABOLICA --
    path("Patients/<int:id>/Composizione",                      views.ComposizioneView.as_view(),                     name="composizione"),
    path("Patients/<int:id>/Composizione/Chart",                views.ComposizioneChartView.as_view(),                name="grafici_composizione"),
    path("Patients/<int:id>/Composizione/Referti",              views.RefertiComposizioneView.as_view(),              name="referti_composizione"),
    
    # URL PER IL TEST DELLA CAPACITA' VITALE
    path('EtaVitale/<int:id>/',                                 views.EtaVitaleView.as_view(),                        name='etaVitale'),
    path('TestVitale/<int:id>/',                                views.TestEtaVitaleView.as_view(),                    name='TestetaVitale'),
    path('RefertoTest/<int:persona_id>/<int:referto_id>/',      views.RefertoQuizView.as_view(),                      name='referto_test'),
    path('UpdateTestVitale/<int:id>/',                          views.QuizEtaVitaleUpdateView.as_view(),              name='updateTestEtaVitale'), 
    
    
    # URL PER ETA BIOLOGICA 
    path("Eta_Biologica/Calcolatore/<int:id>/",                        views.CalcolatoreRender.as_view(),             name='Calcolatore'),
    path("Eta_Biologica/ElencoReferti/Referto/<int:persona_id>/",      views.PersonaDetailView.as_view(),             name="persona_detail"),
    path("Eta_Biologica/ElencoReferti/<int:id>/",                      views.ElencoRefertiView.as_view(),             name="elenco_referti"),


    ## URL SEZIONE RESILIENZA 
    path('Resilienza/<int:persona_id>/',                               views.ResilienzaView.as_view(),                name='resilienza'),
    
    ## URL PIANO TERAPEUTICO
    path('Cartella_Paziente/Piano_Terapeutico/<int:persona_id>/',           views.PianoTerapeutico.as_view(),          name='piano_terapeutico'),
    path('CartellaPaziente/Piano_Terapeutico/Prescrizioni_Esami/<int:persona_id>/', views.PrescrizioniView.as_view(),  name='prescrizioni'),
    
    # TO DEFINE
    path('DownloadPdfVitale/<int:persona_id>/<int:referto_id>',              views.StampaRefertoView.as_view(),         name='download_pdf_vitale'),
    path('update-persona/<int:id>/',                                         views.UpdatePersonaContactView.as_view(),  name='update_persona_contact'), 
]




    



