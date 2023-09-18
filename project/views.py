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

from project.serializers import ProjectListSerializer, ContributorSerializer
from project.models import Project, Contributor
from authentication.permissions import IsOwnerOrReadOnly


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.all()
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    # permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Contributor.objects.all()
        project_id = self.request.GET.get("project_id")
        if project_id:
            queryset = queryset.filter(project=project_id)
        return queryset
