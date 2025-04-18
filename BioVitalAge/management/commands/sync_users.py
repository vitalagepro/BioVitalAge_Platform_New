
from django.core.management.base import BaseCommand # type: ignore
from django.contrib.auth.models import User # type: ignore
from BioVitalAge.models import UtentiRegistratiCredenziali

class Command(BaseCommand):
    help = 'Sincronizza le password da UtentiRegistratiCredenziali a User'

    def handle(self, *args, **options):
        qs = UtentiRegistratiCredenziali.objects.exclude(user__isnull=True)
        for cred in qs:
            u = cred.user
            u.set_password(cred.password)
            u.save()
            self.stdout.write(f'🔑 Password aggiornata per {u.username}')
        self.stdout.write(self.style.SUCCESS('✅ Sincronizzazione completata'))
