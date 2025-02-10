from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.LoginRenderingPage.as_view(), name='loginPage'),
    path("Home_Page", HomePageRender.as_view(), name='HomePage'),
    path("Login",LogOutRender.as_view(), name="logout"),
    path('accept-disclaimer/', AcceptDisclaimerView.as_view(), name='accept_disclaimer'),
    path("Calcolatore_Page", views.CalcolatoreRender.as_view(), name='Calcolatore'),
    path("Risultati_Page", views.RisultatiRender.as_view(), name='Risultati'),
    path("persona/<int:id>/", views.PersonaDetailView.as_view(), name="persona_detail"),
    path("persona/<int:id>/<int:referto_id>/", views.PersonaDetailView.as_view(), name="persona_detail"),
    path("CartellaPaziente/<int:id>/", views.CartellaPazienteView.as_view(), name="cartella_paziente"),
    path("DatiBase/<int:id>/", views.DatiBaseView.as_view(), name="dati_base"),
    path("AggiungiPaziente/", views.InserisciPazienteView.as_view(), name="inserisci_paziente"),
    path("Home_Page/Statistiche", views.StatisticheView.as_view(), name="statistiche"),
    path("Patients/<int:id>/Composizione", views.ComposizioneView.as_view(), name="composizione"),
    path('update-persona/<int:id>/', views.update_persona_contact, name='update_persona_contact'),
    path('update-persona-composizione/<int:id>/', views.update_persona_composizione, name='update_persona_composizione'),
    path('EtaVitale/<int:id>/', views.EtaVitaleView.as_view(), name='etaVitale'),
    path('TestVitale/<int:id>/', views.TestEtaVitaleView.as_view(), name='TestetaVitale'),
    path('RefertoTest/<int:persona_id>/<int:referto_id>/', views.RefertoQuizView.as_view(), name='referto_test'),
    path('Prescrizioni/<int:persona_id>/', views.PrescrizioniView.as_view(), name='prescrizioni'),
    path("api/update_blood_data/<int:id>/", UpdateBloodDataView.as_view(), name="update_blood_data"),
    path("CartellaPaziente/Update/<int:persona_id>/<int:visite_id>/", DettagliPrescrizioni.as_view(), name="dettagli_prescrizioni"),
    path("CartellaPaziente/Download/<int:persona_id>/<int:visite_id>/", ScaricaReferto.as_view(), name="scarica_pdf"),
]




    



