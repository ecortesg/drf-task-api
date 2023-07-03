from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task


@receiver(post_save, sender=Task)
def create_task(sender, instance, created, **kwargs):
    if created:
        print('Task created')

@receiver(post_save, sender=Task)
def update_task(sender, instance, created, **kwargs):
    if created == False:
        print('Task updated')
