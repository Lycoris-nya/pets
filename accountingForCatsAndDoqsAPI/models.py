import uuid

from django.db import models
from django.dispatch import receiver
from django.db.models import signals


class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='photos/')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)


@receiver(signal=signals.pre_delete, sender=Photo)
def on_photo_delete(sender, instance, **kwargs):
    instance.image.delete(save=True)
