from django.urls import path
from . import views


urlpatterns = [
    path("", views.LoginRenderingPage.as_view(), name='loginPage'),
    path("Home_Page", views.HomePageRender.as_view(), name='HomePage'),
    path("Calcolatore_Page", views.CalcolatoreRender.as_view(), name='Calcolatore'),
    path("Risultati_Page", views.RisultatiRender.as_view(), name='Risultati'),
    path("persona/<int:id>/", views.PersonaDetailView.as_view(), name="persona_detail"),
]