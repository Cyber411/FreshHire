from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from.models import SeekerProfile, EmployerProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            EmployerProfile.objects.create(user=instance)
        else:
            SeekerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_staff:
        instance.employerprofile.save()
    else:
        instance.seekerprofile.save()