from django.urls import path
from . import views
from .views import *

urlpatterns = [

    # URL PER LOGIN
    path("", views.LoginRenderingPage.as_view(), name='loginPage'),
    path("Home_Page", HomePageRender.as_view(), name='HomePage'),
    path("Login",LogOutRender.as_view(), name="logout"),
    path('accept-disclaimer/', AcceptDisclaimerView.as_view(), name='accept_disclaimer'),
    
    # URL HOME PAGE / STATISTICHE
    path("Home_Page/Statistiche", views.StatisticheView.as_view(), name="statistiche"),

    # URL PER CALCOLATORE
    path("Calcolatore_Page", views.CalcolatoreRender.as_view(), name='Calcolatore'),

    # URL PER LA RICECA
    path("Risultati_Page", views.RisultatiRender.as_view(), name='Risultati'),

    # URL INSERISCI PAZIENTE
    path("AggiungiPaziente/", views.InserisciPazienteView.as_view(), name="inserisci_paziente"),

    # URL PER VEDERE IL REFERTO DEL CALCOLO DELL'ETA' BIOLOGICA
    path("persona/<int:persona_id>/", views.PersonaDetailView.as_view(), name="persona_detail"),
    path("persona/<int:persona_id>/<int:referto_id>/", views.PersonaDetailView.as_view(), name="persona_detail"),

    # URL PER LA CARTELLA DEL PAZIENTE
    path("CartellaPaziente/<int:id>/", views.CartellaPazienteView.as_view(), name="cartella_paziente"),
    path("ElencoReferti/<int:id>/", views.ElencoRefertiView.as_view(), name="elenco_referti"),
    path("DatiBase/<int:id>/", views.DatiBaseView.as_view(), name="dati_base"),
    path("Patients/<int:id>/Composizione", views.ComposizioneView.as_view(), name="composizione"),
    path('Prescrizioni/<int:persona_id>/', views.PrescrizioniView.as_view(), name='prescrizioni'),
    
    path("CartellaPaziente/Update/<int:persona_id>/<int:visite_id>/", DettagliPrescrizioni.as_view(), name="dettagli_prescrizioni"),
    path("CartellaPaziente/Download/<int:persona_id>/<int:visite_id>/", ScaricaReferto.as_view(), name="scarica_pdf"),

    path("api/update_blood_data/<int:id>/", UpdateBloodDataView.as_view(), name="update_blood_data"),
    path('update-persona-composizione/<int:id>/', views.update_persona_composizione, name='update_persona_composizione'),
    path('update-persona/<int:id>/', views.update_persona_contact, name='update_persona_contact'),
    path('update-persona-composizione/<int:id>/', views.update_persona_composizione, name='update_persona_composizione'),

    # URL PER IL TEST DELLA CAPACITA' VITALE
    path('EtaVitale/<int:id>/', views.EtaVitaleView.as_view(), name='etaVitale'),
    path('TestVitale/<int:id>/', views.TestEtaVitaleView.as_view(), name='TestetaVitale'),
    path('RefertoTest/<int:persona_id>/<int:referto_id>/', views.RefertoQuizView.as_view(), name='referto_test'),
    path('DownloadPdfVitale/<int:persona_id>/<int:referto_id>', views.StampaRefertoView.as_view(), name='download_pdf_vitale'),
    


]




    



