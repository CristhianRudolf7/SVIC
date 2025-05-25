from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Usuarios


@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    if created:
        Usuarios.objects.create(user=instance)
        print('¡Perfil de usuario creado!')
    else:
        instance.profile.save()
        print('¡Perfil de usuario actualizado!')
