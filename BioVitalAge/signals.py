from django.db.models.signals import post_save # type: ignore
from django.dispatch import receiver # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.hashers import check_password # type: ignore
from .models import UtentiRegistratiCredenziali

@receiver(post_save, sender=UtentiRegistratiCredenziali)
def sync_user_with_credential(sender, instance, created, **kwargs):
    # 1) Nuovo record → crea User con create_user()
    if created and not instance.user:
        user = User.objects.create_user(
            username=instance.email,
            email=instance.email,
            password=instance.password
        )
        instance.user = user
        instance.save(update_fields=['user'])

    # 2) Record esistente → sincronizza email & password
    elif instance.user:
        u = instance.user
        dirty = False
        if u.email != instance.email:
            u.email = u.username = instance.email
            dirty = True
        # se la password nel model non corrisponde a quella di User
        if not u.check_password(instance.password):
            u.set_password(instance.password)
            dirty = True
        if dirty:
            u.save()
