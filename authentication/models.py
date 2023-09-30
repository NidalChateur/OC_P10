from django.db import models
from django.contrib.auth.models import AbstractUser


from PIL import Image


class User(AbstractUser):
    WIDTH = 200

    # to automatically set 'email', 'first_name', 'last_name' as required
    email = models.EmailField()
    first_name = models.CharField(max_length=128, verbose_name="Prénom")
    last_name = models.CharField(max_length=128, verbose_name="Nom")
    birthdate = models.DateField(
        verbose_name="Date de naissance",
        help_text="Vous devez avoir plus de 15 ans.",
    )
    # if "can_be_contacted" is False : the "email" field is hidden to other users
    can_be_contacted = models.BooleanField(
        verbose_name="Peux être contacté",
        choices=((True, "Oui"), (False, "Non")),
        help_text="Votre email sera masquée aux autres utilisateurs si vous choisissez 'NON'.",
    )
    # if "can_data_be_shared" is False : the user data are hidden to other users
    can_data_be_shared = models.BooleanField(
        verbose_name="Partager ses données",
        choices=((True, "Oui"), (False, "Non")),
        help_text="Votre profil sera masqué aux autres utilisateurs et vos informations non partagées si vous choisissez 'NON'.",
    )
    image = models.ImageField(
        verbose_name="Photo de profil",
        null=True,
        blank=True,
    )

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
