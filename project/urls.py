from django.urls import path, include
from rest_framework import routers

from project.views import (
    ProjectViewset,
    ContributorViewset,
    AdminProjectViewset,
    AdminContributorViewset,
    IssueViewset,
    AdminIssueViewset,
    AdminCommentViewset,
    CommentViewset,
)


router = routers.SimpleRouter()
router.register("project", ProjectViewset, basename="project")
router.register("contributor", ContributorViewset, basename="contributor")
router.register("issue", IssueViewset, basename="issue")
router.register("comment", CommentViewset, basename="comment")

# admin viewset
router.register("admin/project", AdminProjectViewset, basename="admin-project")
router.register(
    "admin/contributor", AdminContributorViewset, basename="admin-contributor"
)
router.register("admin/issue", AdminIssueViewset, basename="admin-issue")
router.register("admin/comment", AdminCommentViewset, basename="admin-comment")


urlpatterns = [
    path("api/", include(router.urls)),
]
