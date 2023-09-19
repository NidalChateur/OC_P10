"""Seules les contributeurs d'un projets peuvent accéder au projet ainsi qu'à ses issues et ses comments
    - Le contributeur d'un projet peut créer des issues afin de planifier une nouvelle fonctionnalité ou régler un bug
    - Le contributeur
    
    - L’auteur d’une ressource peut modifier ou supprimer cette ressource. Les autres
utilisateurs ne peuvent que lire la ressource.
"""
from django.shortcuts import render
from urllib import request
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth import get_user_model

from project.serializers import (
    ProjectSerializer,
    ContributorSerializer,
    AdminProjectSerializer,
    AdminContributorSerializer,
    IssueSerializer,
    AdminIssueSerializer,
)
from project.models import Project, Contributor, Issue
from project.permissions import IsOwnerOrReadOnly, IsAdminAuthenticated


class MultipleSerializerMixin:
    """utilise serializer detail si l'utilisateur consulte la vue de détail"""

    detail_serializer_class = None

    def get_serializer_class(self):
        # retrieve est le détail
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AdminProjectViewset(ModelViewSet):
    serializer_class = AdminProjectSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.all()

        # url filter on Project.category
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class ProjectViewset(ModelViewSet):
    """The project contributors can read the project but only the author can edit it !"""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # queryset = Project.objects.all()
        # return queryset

        queryset = Project.objects.filter(
            contributor__contributor=self.request.user, is_active=True
        )

        # url filter on Project.category
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class AdminContributorViewset(ModelViewSet):
    serializer_class = AdminContributorSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        queryset = Contributor.objects.all()

        # url filter on Contributor.id
        project_id = self.request.GET.get("project_id")
        if project_id:
            queryset = queryset.filter(project=project_id)

        return queryset


class ContributorViewset(ModelViewSet):
    """Only a project author can create a contribution !"""

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # queryset = Contributor.objects.all()
        # return queryset
        queryset = Contributor.objects.filter(
            project__author=self.request.user, project__is_active=True
        )

        # url filter on Contributor.id
        project_id = self.request.GET.get("project_id")
        if project_id:
            queryset = queryset.filter(project=project_id)

        return queryset


class AdminIssueViewset(ModelViewSet):
    serializer_class = AdminIssueSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        queryset = Issue.objects.all()

        # url filter on Issue.project.name
        project_name = self.request.GET.get("project_name")
        if project_name:
            queryset = queryset.filter(project__name=project_name)

        return queryset


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # queryset = Issue.objects.all()
        contributed_projects = Project.objects.filter(
            contributor__contributor=self.request.user, is_active=True
        )
        queryset = Issue.objects.filter(project__in=contributed_projects)

        # url filter on Issue.project.name
        project_name = self.request.GET.get("project_name")
        if project_name:
            queryset = queryset.filter(project__name=project_name)

        return queryset
