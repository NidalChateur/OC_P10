# from datetime import date
# from dataclasses import fields

# from pyexpat import model
# from tabnanny import verbose
from cProfile import label
from rest_framework import serializers
from django.contrib.auth import get_user_model


from project.models import Project, Contributor


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
