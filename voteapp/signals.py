from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Role)
def create_vote_check(sender, instance, created, **kwargs):
    if created:
        VoteCheck.objects.create(role=instance)
