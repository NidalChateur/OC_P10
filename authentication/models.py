from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

from PIL import Image

from datetime import date


class User(AbstractUser):
    WIDTH = 200

    birthdate = models.DateField(
        verbose_name="Date de naissance",
    )
    # if "can_be_contacted" is False : the "email" field is hidden
    can_be_contacted = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Peux être contacté",
        choices=((True, "Oui"), (False, "Non")),
    )
    # can_data_be_shared is True only if age > 15
    # if "can_data_be_shared" is False : the user data are hidden
    can_data_be_shared = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Partager ses données",
        choices=((True, "Oui"), (False, "Non")),
    )
    image = models.ImageField(verbose_name="Photo de profil", blank=True, null=True)
    # vue admin django http://127.0.0.1:8000/admin suffisant ?
    # créer une vue admin et permettre à l'admin de désactiver l'utilisateur
    # active=models.BooleanField(default=True)

    def __str__(self):
        return f"{str(self.username).capitalize()}"

    def resize_image(self):
        """Resize the image while maintaining the original height/width aspect ratio
        width == 200px"""

        if self.image:
            image = Image.open(self.image)

            # get the original height/width aspect ratio
            width, height = image.size

            # get the new height/width aspect ratio
            new_width = self.WIDTH
            new_height = int(height * (new_width / width))

            # resize the image
            image = image.resize((new_width, new_height), Image.LANCZOS)

            # Save
            image.save(self.image.path)

    def save(self, *args, **kwargs):
        """Override the save method with the resize_image"""

        super().save(*args, **kwargs)
        self.resize_image()
