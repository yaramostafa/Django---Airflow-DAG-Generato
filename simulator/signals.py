from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Simulator
from django.core.management import call_command

@receiver(post_save, sender=Simulator)
def regenerate_dags(sender, instance, **kwargs):
    call_command('generate_dags')