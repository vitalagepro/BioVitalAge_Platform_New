from django.contrib import admin
from .models import UtentiRegistratiCredenziali,TabellaPazienti, ArchivioReferti, DatiEstesiReferti

admin.site.register(UtentiRegistratiCredenziali)
admin.site.register(TabellaPazienti)
admin.site.register(ArchivioReferti)
admin.site.register(DatiEstesiReferti)