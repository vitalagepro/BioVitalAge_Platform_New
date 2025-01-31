from django.contrib import admin
from .models import *

admin.site.register(UtentiRegistratiCredenziali)
admin.site.register(TabellaPazienti)
admin.site.register(ArchivioReferti)
admin.site.register(DatiEstesiReferti)
admin.site.register(ArchivioRefertiTest)
admin.site.register(DatiEstesiRefertiTest)
admin.site.register(PrescrizioniUtenti)
