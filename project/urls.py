from django.urls import path, include
from rest_framework import routers

from project.views import (
    ProjectViewset,
    ContributorViewset,
    AdminProjectViewset,
    AdminContributorViewset,
)

# from project.views import IssueViewset
# from project.views import CommentViewset


router = routers.SimpleRouter()
router.register("project", ProjectViewset, basename="project")
router.register("contributor", ContributorViewset, basename="contributor")

router.register("admin/project", AdminProjectViewset, basename="admin-project")
router.register(
    "admin/contributor", AdminContributorViewset, basename="admin-contributor"
)

# router.register("issue", IssueViewset, basename="issue")
# router.register("comment", CommentViewset, basename="comment")


urlpatterns = [
    path("api/", include(router.urls)),
]
