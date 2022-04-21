from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse
# Create your models here.

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.DecimalField(max_digits=10000000, decimal_places=2, help_text='Token or Royalty',null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profiles:profiledetail", kwargs={"username": self.user.username})

    
def post_save_user_receiver(sender, instance, created,*args,**kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        
post_save.connect(post_save_user_receiver, sender=User)