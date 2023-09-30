from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from project.serializers import (
    ProjectSerializer,
    ContributorSerializer,
    AdminProjectSerializer,
    AdminContributorSerializer,
    AdminIssueSerializer,
    IssueSerializer,
    AdminCommentSerializer,
    CommentSerializer,
)
from project.models import Project, Contributor, Issue, Comment
from project.permissions import IsOwnerOrReadOnly


class AdminProjectViewset(ModelViewSet):
    serializer_class = AdminProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = Project.objects.all()

        # url filter on Project.category
        # http://127.0.0.1:8000/api/admin/project/?category=xxx
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)

        # url filter on Project.name
        # http://127.0.0.1:8000/api/admin/project/?project_name=xxx
        project_name = self.request.GET.get("project_name")
        if project_name:
            queryset = queryset.filter(name=project_name)

        return queryset


class ProjectViewset(ModelViewSet):
    """The project contributors can read the project but only the author can edit it"""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # select only projects where the connected user is a contributor
        queryset = Project.objects.filter(
            contributor__contributor=self.request.user, is_active=True
        )

        # url filter on Project.category
        # http://127.0.0.1:8000/api/project/?category=xxx
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)

        # url filter on Project.name
        # http://127.0.0.1:8000/api/project/?project_name=xxx
        project_name = self.request.GET.get("project_name")
        if project_name:
            queryset = queryset.filter(name=project_name)

        return queryset


class AdminContributorViewset(ModelViewSet):
    serializer_class = AdminContributorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = Contributor.objects.all()

        # url filter on Contributor.id
        project_id = self.request.GET.get("project_id")
        if project_id:
            queryset = queryset.filter(project=project_id)

        return queryset


class ContributorViewset(ModelViewSet):
    """Only a project author can create a contribution"""

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # select only contributors to the project where the connected user is the author
        queryset = Contributor.objects.filter(
            project__author=self.request.user, project__is_active=True
        )
        # queryset = Contributor.objects.all()

        # url filter on Contributor.id
        project_id = self.request.GET.get("project_id")
        if project_id:
            queryset = queryset.filter(project=project_id)

        return queryset


class AdminIssueViewset(ModelViewSet):
    """only a project contributor can be assigned and act as the issue author"""

    serializer_class = AdminIssueSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = Issue.objects.all()

        # url filter on Issue.id
        issue_id = self.request.GET.get("issue_id")
        if issue_id:
            queryset = queryset.filter(id=issue_id)

        return queryset


class IssueViewset(ModelViewSet):
    """only a project contributor can be assigned and act as the issue author"""

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # select only issues where the connected user is a project contributor
        contributed_projects = Project.objects.filter(
            contributor__contributor=self.request.user, is_active=True
        )
        queryset = Issue.objects.filter(project__in=contributed_projects)

        # url filter on Issue.id
        issue_id = self.request.GET.get("issue_id")
        if issue_id:
            queryset = queryset.filter(id=issue_id)

        return queryset


class AdminCommentViewset(ModelViewSet):
    """only a project contributor can create a comment on an issue"""

    serializer_class = AdminCommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = Comment.objects.all()

        # url filter on Comment.id
        comment_id = self.request.GET.get("comment_id")
        if comment_id:
            queryset = queryset.filter(id=comment_id)

        return queryset


class CommentViewset(ModelViewSet):
    """only a project contributor can create a comment on an issue"""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # get the comments of contributed projects
        contributed_projects = Project.objects.filter(
            contributor__contributor=self.request.user, is_active=True
        )
        contributed_projects_issues = Issue.objects.filter(
            project__in=contributed_projects
        )
        queryset = Comment.objects.filter(issue__in=contributed_projects_issues)

        # url filter on Comment.id
        comment_id = self.request.GET.get("comment_id")
        if comment_id:
            queryset = queryset.filter(id=comment_id)

        return queryset
