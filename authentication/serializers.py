from datetime import date

from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, label="Mot de passe"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        label="Confirmation du mot de passe",
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "can_be_contacted",
            "first_name",
            "last_name",
            "birthdate",
            "can_data_be_shared",
            "image",
            "password",
            "password_confirm",
        ]

    def to_representation(self, instance):
        """hide the user's email if the "can_be_contacted" field is False"""

        data = super().to_representation(instance)
        request = self.context.get("request")
        if (not request.user.is_superuser) and (
            request.user.username != instance.username
        ):
            if not instance.can_be_contacted:
                data.pop("email")

        return data

    def age(self, birthdate: date) -> int:
        """return the user age"""

        today = date.today()
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )

        return age

    def validate(self, data):
        """check 'password' and 'birthdate' fields"""

        try:
            """test before the instance creation with password validation (used in list view)"""

            if self.age(data["birthdate"]) <= 15:
                raise serializers.ValidationError(
                    "Votre age doit être supérieur à 15ans, si ce n'est pas le cas, veuillez contacter l'admin."
                )
            if len(data["password"]) < 8:
                raise serializers.ValidationError(
                    "Votre mot de passe doit contenir au minimum 8 caractères."
                )
            if data["password"].isdigit():
                raise serializers.ValidationError(
                    "Votre mot de passe ne peut pas être entièrement numérique."
                )
            if data["password"].isalpha():
                raise serializers.ValidationError(
                    "Votre mot de passe doit contenir au moins un chiffre."
                )
            if data["password"] != data["password_confirm"]:
                raise serializers.ValidationError(
                    "Les deux mots de passe ne correspondent pas."
                )

            check_list = [
                data["first_name"] in data["password"],
                data["last_name"] in data["password"],
                data["username"] in data["password"],
                data["email"] in data["password"],
                str(data["birthdate"].year) in data["password"],
            ]
            if any(check_list):
                raise serializers.ValidationError(
                    "Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles."
                )

            return data

        except KeyError:
            """test before the update instance without password validation (used in detail view)"""

            if self.age(data["birthdate"]) <= 15:
                raise serializers.ValidationError(
                    "Votre age doit être supérieur à 15ans, si ce n'est pas le cas, veuillez contacter l'admin."
                )

            return data

    def create(self, validated_data):
        """erase 'password_confirm' fiel and create the user instance"""

        validated_data.pop("password_confirm")
        user = get_user_model().objects.create_user(**validated_data)

        return user


class UserDetailSerializer(UserListSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "can_be_contacted",
            "first_name",
            "last_name",
            "birthdate",
            "can_data_be_shared",
            "image",
        ]


class AdminUserListSerializer(UserListSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "can_be_contacted",
            "first_name",
            "last_name",
            "birthdate",
            "can_data_be_shared",
            "image",
            "is_active",
            "is_staff",
            "is_superuser",
            "password",
            "password_confirm",
        )


class AdminUserDetailSerializer(AdminUserListSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "can_be_contacted",
            "first_name",
            "last_name",
            "birthdate",
            "can_data_be_shared",
            "image",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class ChangePasswordSerializer(UserListSerializer):
    old_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        label="Ancien mot de passe",
    )

    class Meta:
        model = get_user_model()
        fields = ("old_password", "password", "password_confirm")

    def validate(self, data):
        user = self.context.get("request").user

        if not user.check_password(data["old_password"]):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")

        user_data = {
            "password": data["password"],
            "password_confirm": data["password_confirm"],
            "username": user.username,
            "birthdate": user.birthdate,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        if data["old_password"] == data["password"]:
            raise serializers.ValidationError(
                "Vous devez choisir un mot passe différent."
            )

        # use UserListSerializer.validate() method with the user data
        data = super().validate(user_data)

        return data
