from django.urls import path
from . import views
from .views import HomePageRender, AcceptDisclaimerView

urlpatterns = [
    path("", views.LoginRenderingPage.as_view(), name='loginPage'),
    path("Home_Page", HomePageRender.as_view(), name='HomePage'),
    path('accept-disclaimer/', AcceptDisclaimerView.as_view(), name='accept_disclaimer'),
    path("Calcolatore_Page", views.CalcolatoreRender.as_view(), name='Calcolatore'),
    path("Risultati_Page", views.RisultatiRender.as_view(), name='Risultati'),
    path("persona/<int:id>/", views.PersonaDetailView.as_view(), name="persona_detail"),
    path("CartellaPaziente/<int:id>/", views.CartellaPazienteView.as_view(), name="cartella_paziente"),
    path("DatiBase/<int:id>/", views.DatiBaseView.as_view(), name="dati_base"),
    path("AggiungiPaziente/", views.InserisciPazienteView.as_view(), name="inserisci_paziente"),
    path("Home_Page/Statistiche", views.StatisticheView.as_view(), name="statistiche"),
    path("Patients/<int:id>/Composizione", views.ComposizioneView.as_view(), name="composizione"),
    path('update-persona/<int:id>/', views.update_persona_contact, name='update_persona_contact'),
    path('EtaVitale/<int:id>/', views.EtaVitaleView.as_view(), name='etaVitale'),
    path('TestVitale/<int:id>/', views.TestEtaVitaleView.as_view(), name='TestetaVitale'),
]



