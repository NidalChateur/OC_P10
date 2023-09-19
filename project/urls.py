from django.urls import path, include
from rest_framework import routers

from project.views import (
    ProjectViewset,
    ContributorViewset,
    AdminProjectViewset,
    AdminContributorViewset,
    IssueViewset,
    AdminIssueViewset,
)


router = routers.SimpleRouter()
router.register("project", ProjectViewset, basename="project")
router.register("contributor", ContributorViewset, basename="contributor")
router.register("issue", IssueViewset, basename="issue")

# admin viewset
router.register("admin/project", AdminProjectViewset, basename="admin-project")
router.register(
    "admin/contributor", AdminContributorViewset, basename="admin-contributor"
)
router.register("admin/issue", AdminIssueViewset, basename="admin-issue")

# router.register("comment", CommentViewset, basename="comment")


urlpatterns = [
    path("api/", include(router.urls)),
]
