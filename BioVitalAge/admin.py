from django.contrib import admin # type: ignore
from .models import *

admin.site.register(UtentiRegistratiCredenziali)
admin.site.register(TabellaPazienti)
admin.site.register(RefertiEtaBiologica)
admin.site.register(DatiEstesiRefertiEtaBiologica)
admin.site.register(RefertiCapacitaVitale)
admin.site.register(DatiEstesiRefertiCapacitaVitale)
admin.site.register(PrescrizioniEsami)
admin.site.register(Appointment)
admin.site.register(Resilienza)
admin.site.register(ValutazioneMS)
admin.site.register(RefertiEtaMetabolica)
