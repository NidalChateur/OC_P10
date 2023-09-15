from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from PIL import Image


class Project(models.Model):
    """Project model"""

    # ne pas le mettre ici
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Contributor", related_name="contributions"
    )
    # project creator
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(
        max_length=128, verbose_name="Nom du projet", null=True, blank=True
    )
    description = models.TextField(max_length=2048, blank=True, null=True)
    project_type = models.CharField(
        max_length=128,
        verbose_name="Type du projet",
        choices=(
            ("Back-end", "Back-end"),
            ("Front-end", "Front-end"),
            ("iOS", "iOS"),
            ("Android", "Android"),
        ),
        null=True,
        blank=True,
    )
    time_created = models.DateTimeField(auto_now_add=True)


# UserProject
#   user
#   project
class Contributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # champ commentaire
    contribution = models.CharField(max_length=255, blank=True)

# a retirer
    # class Meta:
    #     unique_together = ("contributor", "project")
