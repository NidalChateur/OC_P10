from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
import project

from project.models import Project, Contributor, Issue


class UserContributorSerializer(serializers.ModelSerializer):
    """used to display the "author" and "contributor" fields"""

    class Meta:
        model = get_user_model()
        fields = ("username",)


class AdminProjectSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), slug_field="username", label="Auteur"
    )
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ("id", "author", "contributors", "name", "description", "category")

    def get_contributors(self, instance):
        """use UserContributorSerializer to display the "contributors" field"""

        queryset = instance.contributors.all()
        serializer = UserContributorSerializer(queryset, many=True)

        return serializer.data


class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ("id", "author", "contributors", "name", "description", "category")

    def get_author(self, instance):
        """use UserContributorSerializer to display the "author" field"""

        queryset = instance.author
        serializer = UserContributorSerializer(queryset)

        return serializer.data

    def get_contributors(self, instance):
        """use UserContributorSerializer to display the "contributors" field"""

        queryset = instance.contributors.all()
        serializer = UserContributorSerializer(queryset, many=True)

        return serializer.data

    def create(self, validated_data):
        """create a Project instance and a Contributor instance and
        set the connected user as author and contributor"""

        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            # set the authenticated user as the author
            validated_data["author"] = request.user

            # check if the project exists
            if Project.objects.filter(name=validated_data["name"]):
                raise serializers.ValidationError("Un projet avec ce nom existe déjà.")

            # create the project
            project = Project(**validated_data)
            project.save()

            # create the contribution of the author
            contributor = Contributor()
            contributor.contributor = project.author
            contributor.project = project
            contributor.save()

            return project

        raise serializers.ValidationError(
            "L'utilisateur doit être connecté pour créer un projet."
        )


class AdminContributorSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(),
        slug_field="name",
    )
    contributor = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field="username",
    )

    class Meta:
        model = Contributor
        fields = (
            "id",
            "project",
            "contributor",
        )


class ContributorSerializer(serializers.ModelSerializer):
    "only the project author can create a contribution"

    project = serializers.SlugRelatedField(
        queryset=[],
        slug_field="name",
    )
    contributor = serializers.SlugRelatedField(
        queryset=[],
        slug_field="username",
    )

    class Meta:
        model = Contributor
        fields = (
            "id",
            "project",
            "contributor",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")

        if request and request.user:
            current_user_username = request.user.username
            self.fields["contributor"].queryset = get_user_model().objects.exclude(
                username=current_user_username
            )
            self.fields["project"].queryset = Project.objects.filter(
                author=request.user
            )

    def create(self, validated_data):
        """check if the authenticated user is the project author
        then it creates a contributor"""

        request = self.context.get("request")
        project = validated_data["project"]
        if request.user != project.author:
            raise serializers.ValidationError("Vous n'êtes pas l'auteur du projet.")

        contributor = Contributor(**validated_data)
        contributor.save()

        return contributor


class AdminIssueSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    project = serializers.SlugRelatedField(
        queryset=[], slug_field="name", label="Projet"
    )
    assigned_to = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field="username",
        label="Assigné à",
    )

    class Meta:
        model = Issue
        fields = (
            "id",
            "author",
            "project",
            "name",
            "description",
            "status",
            "priority",
            "category",
            "assigned_to",
        )

    def get_author(self, instance):
        """use UserContributorSerializer to display the "author" field"""

        serializer = UserContributorSerializer(instance.author)

        return serializer.data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")

        if request and request.user:
            contributed_projects = Project.objects.filter(
                contributor__contributor=request.user, is_active=True
            )
            self.fields["project"].queryset = contributed_projects

    def create(self, validated_data):
        request = self.context.get("request")
        project = validated_data["project"]
        assigned_user = validated_data["assigned_to"]
        contributors = (
            get_user_model()
            .objects.filter(contributor__project=project)
            .values_list("username", flat=True)
        )

        # check if the Issue.assigned_to is a project contributor
        if not Contributor.objects.filter(contributor=assigned_user, project=project):
            raise serializers.ValidationError(
                f"'{assigned_user.username}' n'est pas contributeur au projet '{project.name}'."
                f" Voici la liste des contributeurs que vous pouvez assigner :"
                f"{list(contributors)}"
            )

        validated_data["author"] = request.user
        issue = Issue(**validated_data)
        issue.save()

        return issue


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    project = serializers.SlugRelatedField(
        queryset=[], slug_field="name", label="Projet"
    )
    assigned_to = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field="username",
        label="Assigné à",
    )

    class Meta:
        model = Issue
        fields = (
            "id",
            "author",
            "project",
            "name",
            "description",
            "status",
            "priority",
            "category",
            "assigned_to",
        )

    def get_author(self, instance):
        """use UserContributorSerializer to display the "author" field"""

        serializer = UserContributorSerializer(instance.author)

        return serializer.data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")

        if request and request.user:
            contributed_projects = Project.objects.filter(
                contributor__contributor=request.user, is_active=True
            )
            self.fields["project"].queryset = contributed_projects

    def create(self, validated_data):
        request = self.context.get("request")
        project = validated_data["project"]
        assigned_user = validated_data["assigned_to"]
        contributors = (
            get_user_model()
            .objects.filter(contributor__project=project)
            .values_list("username", flat=True)
        )

        # check if the Issue.author is a project contributor
        if not Contributor.objects.filter(contributor=request.user, project=project):
            raise serializers.ValidationError(
                f"Vous n'êtes pas contributeur au projet '{project.name}'."
            )

        # check if the Issue.assigned_to is a project contributor
        if not Contributor.objects.filter(contributor=assigned_user, project=project):
            raise serializers.ValidationError(
                f"'{assigned_user.username}' n'est pas contributeur au projet '{project.name}'."
                f" Voici la liste des contributeurs que vous pouvez assigner :"
                f"{list(contributors)}"
            )

        validated_data["author"] = request.user
        issue = Issue(**validated_data)
        issue.save()

        return issue
