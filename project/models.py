from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
    )
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Contributor",
        related_name="contributions",
    )
    name = models.CharField(
        max_length=256,
        verbose_name="Nom du projet",
        help_text="Donnez un nom à votre projet",
    )
    description = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        help_text="Description facultative",
    )
    category = models.CharField(
        max_length=128,
        verbose_name="Catégorie",
        choices=(
            ("Back-end", "Back-end"),
            ("Front-end", "Front-end"),
            ("iOS", "iOS"),
            ("Android", "Android"),
        ),
    )
    created_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Précise si le projet doit être considéré comme actif. Décochez ceci plutôt que de supprimer le projet.",
        verbose_name="Actif",
    )
    slug_name = models.SlugField(max_length=256, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """save the slug_name"""

        self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)


class Contributor(models.Model):
    """Project contributors"""

    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contributor", "project")


class Issue(models.Model):
    """define a task, a bug or feature in the project"""

    # only a project contributor can create an issue
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issue_owner",
        verbose_name="Auteur",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name="Projet",
        related_name="issues",
    )
    name = models.CharField(
        max_length=256,
        verbose_name="Nom de l'issue",
        help_text="Donnez un nom à votre issue",
    )
    description = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        help_text="Description facultative",
    )
    status = models.CharField(
        max_length=32,
        verbose_name="Statut",
        default="To Do",
        choices=(
            ("To Do", "To Do"),
            ("In Progress", "In Progress"),
            ("Finished", "Finished"),
        ),
    )
    priority = models.CharField(
        max_length=32,
        verbose_name="Priorité",
        choices=(("Low", "Low"), ("Medium", "Medium"), ("High", "High")),
    )
    category = models.CharField(
        max_length=32,
        verbose_name="Balise",
        choices=(("Bug", "Bug"), ("Feature", "Feature"), ("Task", "Task")),
    )
    # only a project contributor can be assigned to an issue
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Assigné à",
        null=True,
    )
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    """used to comment an issue"""

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")

    # only a project contributor can comment an issue
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
    )
    description = models.TextField(max_length=5000)

    issue_url = models.URLField(null=True)

    # uuid is the unique comment id
    uuid = models.IntegerField(null=True)
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    def __str__(self):
        return f"{self.uuid}"

    def save(self, *args, **kwargs):
        self.issue_url = f"http://127.0.0.1:8000/api/issue/?issue_id={self.issue.id}"
        super().save(*args, **kwargs)
