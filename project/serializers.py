from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from project.models import Project, Contributor, Issue, Comment


class DateTimeMixin(serializers.Serializer):
    """used to display the "created_time" fields"""

    created_time = serializers.SerializerMethodField(read_only=True)

    def get_created_time(self, obj):
        "return a DateTimeField formatted"

        return obj.created_time.strftime("%Y-%m-%d %H:%M:%S")


class UserContributorSerializer(serializers.ModelSerializer):
    """used to display the "author" and "contributor" fields"""

    class Meta:
        model = get_user_model()
        fields = ("username",)


class AdminProjectSerializer(DateTimeMixin, serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field="username",
        label="Auteur",
    )
    contributors = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "author",
            "description",
            "category",
            "is_active",
            "contributors",
            "issues",
            "created_time",
        )

    def get_contributors(self, instance):
        """use UserContributorSerializer to display the "contributors" field"""

        queryset = instance.contributors.all()
        serializer = UserContributorSerializer(queryset, many=True)

        return serializer.data

    def get_issues(self, instance):
        """use IssueSerializer to display the "issues" field"""

        queryset = instance.issues.all()
        serializer = IssueSerializer(queryset, many=True)

        return serializer.data

    def validate(self, data):
        """check if the project exists"""

        if Project.objects.filter(slug_name=slugify(data["name"])):
            raise serializers.ValidationError("Un projet avec ce nom existe déjà.")

        return data

    def create(self, validated_data):
        """create a Project instance and a Contributor instance then
        set the connected user as author and contributor"""

        project = Project(**validated_data)
        project.save()

        # create the contribution of the author
        contributor = Contributor()
        contributor.contributor = project.author
        contributor.project = project
        contributor.save()

        return project


class ProjectSerializer(AdminProjectSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "author",
            "description",
            "category",
            "contributors",
            "issues",
            "created_time",
        )

    def get_author(self, instance):
        """use UserContributorSerializer to display the "author" field"""

        queryset = instance.author
        serializer = UserContributorSerializer(queryset)

        return serializer.data

    def create(self, validated_data):
        """create a Project instance and a Contributor instance then
        set the connected user as author and contributor"""

        user = self.context.get("request").user

        # set the authenticated user as the author
        validated_data["author"] = user

        # create the project
        project = Project(**validated_data)
        project.save()

        # create the contribution of the author
        contributor = Contributor()
        contributor.contributor = project.author
        contributor.project = project
        contributor.save()

        return project


class AdminContributorSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(),
        slug_field="name",
        label="Projet",
    )
    contributor = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field="username",
        label="Contributeur",
    )

    class Meta:
        model = Contributor
        fields = (
            "id",
            "project",
            "contributor",
        )


class ContributorSerializer(AdminContributorSerializer):
    "only the project author can create a contribution"

    class Meta:
        model = Contributor
        fields = (
            "id",
            "project",
            "contributor",
        )

    def __init__(self, *args, **kwargs):
        """allow selecting a limited list of instances for the 'project' and 'contributor'
        fields in the viewset"""

        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request:
            current_user_username = request.user.username
            self.fields["contributor"].queryset = get_user_model().objects.exclude(
                username=current_user_username
            )
            self.fields["project"].queryset = Project.objects.filter(
                author=request.user
            )

    def validate(self, data):
        request = self.context.get("request")
        project = data["project"]
        if request.user != project.author:
            raise serializers.ValidationError("Vous n'êtes pas l'auteur du projet.")

        return data


class AdminIssueSerializer(DateTimeMixin, serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field="username",
        label="Auteur",
        help_text="Seul un contributeur au projet peut être auteur de cette issue",
    )
    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(),
        slug_field="name",
        label="Projet",
        help_text="Seul les projets auxquels vous avez contribué sont sélectionnables ",
    )
    assigned_to = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field="username",
        label="Assigné à",
        help_text="Seul un contributeur au projet peut être assigné",
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = (
            "id",
            "project",
            "author",
            "name",
            "description",
            "status",
            "priority",
            "category",
            "assigned_to",
            "created_time",
            "comments",
        )

    def get_comments(self, instance):
        """use CommentSerializer to display the "comments" field"""

        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)

        return serializer.data

    def validate(self, data):
        """validate 'author' and 'assigned_to' fields :
        -only a project contributor can create an issue
        -only a project contributor can be assigned to an issue"""

        project = data["project"]

        try:
            author = data["author"]
        except KeyError:
            author = self.context.get("request").user

        assigned_user = data["assigned_to"]
        # get the project contributors list
        project_contributors = (
            get_user_model()
            .objects.filter(contributor__project=project)
            .values_list("username", flat=True)
        )

        # check if the Issue.author is a project contributor
        if not Contributor.objects.filter(contributor=author, project=project):
            raise serializers.ValidationError(
                f"Vous n'êtes pas contributeur au projet '{project.name}'."
            )

        # check if the Issue.assigned_to is a project contributor
        if not Contributor.objects.filter(contributor=assigned_user, project=project):
            raise serializers.ValidationError(
                f"'{assigned_user.username}' n'est pas contributeur au projet '{project.name}'."
                f" Voici la liste des contributeurs que vous pouvez assigner :"
                f"{list(project_contributors)}"
            )

        return data


class IssueSerializer(AdminIssueSerializer):
    author = serializers.SerializerMethodField()

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
            "created_time",
            "comments",
        )

    def get_author(self, instance):
        """use UserContributorSerializer to display the "author" field"""

        queryset = instance.author
        serializer = UserContributorSerializer(queryset)

        return serializer.data

    def __init__(self, *args, **kwargs):
        """allow selecting a limited list of instances for the 'project'
        field in the viewset"""

        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request:
            contributed_projects = Project.objects.filter(
                contributor__contributor=request.user, is_active=True
            )
            self.fields["project"].queryset = contributed_projects

    def create(self, validated_data):
        """create an Issue instance then set the connected user as author"""

        request = self.context.get("request")
        validated_data["author"] = request.user
        issue = Issue(**validated_data)
        issue.save()

        return issue


class AdminCommentSerializer(DateTimeMixin, serializers.ModelSerializer):
    issue_url = serializers.URLField(read_only=True)
    uuid = serializers.IntegerField(read_only=True)
    issue = serializers.SlugRelatedField(
        queryset=Issue.objects.all(),
        slug_field="name",
        label="Issue",
        help_text="Seules les issues des projets auxquels vous avez contribué sont sélectionnables ",
    )
    author = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field="username",
        label="Auteur",
        help_text="Seul un contributeur au projet peut commenter une issue",
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "issue",
            "author",
            "description",
            "issue_url",
            "uuid",
            "created_time",
        )

    def validate(self, data):
        try:
            author = data["author"]
        except KeyError:
            author = self.context.get("request").user

        issue = data["issue"]
        project = issue.project

        if not Contributor.objects.filter(contributor=author, project=project):
            raise serializers.ValidationError(
                f"Vous n'êtes pas contributeur au projet '{project.name}' pour commenter son issue."
            )

        return data

    def create(self, validated_data):
        """create the comment instance and set the uuid attribute and
        the connected user as author"""

        validated_data["author"]
        try:
            validated_data["author"]
        except KeyError:
            validated_data["author"] = self.context.get("request").user

        comment = Comment(**validated_data)
        comment.save()
        comment.uuid = comment.id
        comment.save()

        return comment


class CommentSerializer(AdminCommentSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "issue",
            "author",
            "description",
            "issue_url",
            "uuid",
            "created_time",
        )

    def get_author(self, instance):
        """use UserContributorSerializer to display the "author" field"""

        queryset = instance.author
        serializer = UserContributorSerializer(queryset)

        return serializer.data

    def __init__(self, *args, **kwargs):
        """allow selecting a limited list of instances for the 'issue'
        field in the viewset"""

        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request:
            contributed_projects = Project.objects.filter(
                contributor__contributor=request.user, is_active=True
            )
            contributed_projects_issues = Issue.objects.filter(
                project__in=contributed_projects
            )

            self.fields["issue"].queryset = contributed_projects_issues
