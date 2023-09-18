# from datetime import date
# from dataclasses import fields

# from pyexpat import model
# from tabnanny import verbose
from rest_framework import serializers
from django.contrib.auth import get_user_model


from project.models import Project, Contributor


class UserContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username",)


class ProjectListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ("id", "author", "contributors", "name", "description", "category")

    def get_author(self, instance):
        queryset = instance.author
        serializer = UserContributorSerializer(queryset)

        return serializer.data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["author"] = request.user

            project = Project(**validated_data)
            project.save()

            contributor = Contributor()
            contributor.contributor = project.author
            contributor.project = project
            contributor.save()

            return project

        raise serializers.ValidationError(
            "L'utilisateur doit être connecté pour créer un projet."
        )


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ("id", "project", "contributor")


# class ProjectListSerializer(serializers.ModelSerializer):
#     # author = serializers.SerializerMethodField()

#     class Meta:
#         model = Project
#         fields = ("id", "author", "contributors", "name", "description", "category")

#     def get_author(self, instance):
#         queryset = instance.author
#         serializer = UserSerializer(queryset)
#         return serializer.data
