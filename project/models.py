from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from PIL import Image


class Project(models.Model):
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
    )
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Contributor", related_name="contributions"
    )
    name = models.CharField(
        max_length=256, verbose_name="Nom du projet", null=True, blank=True
    )
    description = models.TextField(max_length=5000, blank=True, null=True)
    category = models.CharField(
        max_length=128,
        verbose_name="Catégorie",
        choices=(
            ("Back-end", "Back-end"),
            ("Front-end", "Front-end"),
            ("iOS", "iOS"),
            ("Android", "Android"),
        ),
        null=True,
        blank=True,
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    """Seules les contributeurs d'un projets peuvent accéder au projet ainsi qu'à ses issues et ses comments
    - Le contributeur d'un projet peut créer des issues afin de planifier une nouvelle fonctionnalité ou régler un bug
    - Le contributeur"""

    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # champ commentaire
    # contribution = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("contributor", "project")


# class Issue(models.Model):
#     """define a task, a bug or feature in the project"""

#     # ici ce sont les contributeurs d'un projet uniquement qui sont sélectionnable
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="issue_owner",
#         verbose_name="Auteur",
#     )
#     project = models.ForeignKey(
#         Project, on_delete=models.CASCADE, verbose_name="Projet", related_name="issues"
#     )
#     name = models.CharField(max_length=256, verbose_name="Nom du problème")
#     description = models.TextField(max_length=5000, blank=True, null=True)
#     status = models.CharField(
#         max_length=32,
#         verbose_name="Statut",
#         default="To Do",
#         choices=(
#             ("To DO", "To DO"),
#             ("In Progress", "In Progress"),
#             ("Finished", "Finished"),
#         ),
#     )
#     priority = models.CharField(
#         max_length=32,
#         verbose_name="Priorité",
#         choices=(("LOW", "LOW"), ("MEDIUM", "MEDIUM"), ("HIGH", "HIGH")),
#     )
#     issue_type = models.CharField(
#         max_length=32,
#         verbose_name="Balise",
#         choices=(("BUG", "BUG"), ("FEATURE", "FEATURE"), ("TASK", "TASK")),
#     )
#     # ici ce sont les contributeurs d'un projet uniquement qui sont sélectionnable
#     assigned_to = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         verbose_name="Assigné à",
#         null=True,
#         blank=True,
#     )
#     created_time = models.DateTimeField(
#         auto_now_add=True, verbose_name="Date de création"
#     )

#     def __str__(self):
#         return self.name


# class Comment(models.Model):
#     """used to comment an issue"""

#     issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")

#     # ici ce sont les contributeurs d'un projet uniquement qui sont sélectionnable
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         verbose_name="Auteur",
#     )
#     description = models.TextField(max_length=5000, blank=True, null=True)

#     # Il doit aussi donner un lien vers une issue.
#     issue_url = models.URLField(null=True)

#     # un identifiant unique de type uuid est automatiquement généré.  Ce
#     # dernier permet de mieux référencer le comment.
#     uuid = models.IntegerField(null=True)
#     created_time = models.DateTimeField(
#         auto_now_add=True, verbose_name="Date de création"
#     )

#     def __str__(self):
#         return f"{self.uuid}"

#     def save(self, *args, **kwargs):
#         self.uuid = self.id
#         # self.issue_url= ...
#         super().save(*args, **kwargs)
