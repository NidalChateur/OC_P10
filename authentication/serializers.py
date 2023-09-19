# from dataclasses import field
from datetime import date

# from dataclasses import fields

# from pyexpat import model
# from tabnanny import verbose
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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

    def create(self, validated_data):
        default_password = "00000000pw"
        user = User.objects.create_user(**validated_data)
        user.set_password(default_password)
        user.save()

        return user


class UserNoPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
        )

    def to_representation(self, instance):
        """hide the user's email if the "can_be_contacted" field is False"""

        data = super().to_representation(instance)
        request = self.context.get("request")
        if request and request.user.username != instance.username:
            if not instance.can_be_contacted:
                data.pop("email")

        return data

    def age(self, birthdate) -> int:
        """return the user age"""

        today = date.today()
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )

        return age

    def validate(self, data):
        """check if the user.age > 15 to keep the "can_data_be_shared" field on True"""

        if data["birthdate"]:
            age = self.age(data["birthdate"])
            if age and age <= 15 and data["can_data_be_shared"]:
                raise serializers.ValidationError(
                    "Votre age doit être supérieur à 15ans pour partager vos données."
                )
        else:
            data["can_data_be_shared"] = False
            data["can_be_contacted"] = False

        return data

    def create(self, validated_data):
        default_password = "00000000pw"
        user = User.objects.create_user(**validated_data)
        user.set_password(default_password)
        user.save()

        return user


# # en standby
# class UserSerializer(serializers.ModelSerializer):
#     password_confirm = serializers.CharField(
#         write_only=True, label="Confirmation du mot de passe"
#     )

#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "username",
#             "email",
#             "can_be_contacted",
#             "first_name",
#             "last_name",
#             "birthdate",
#             "can_data_be_shared",
#             "image",
#             "password",
#             "password_confirm",
#         )

#     def age(self, birthdate) -> int:
#         """return the user age"""

#         today = date.today()
#         age = (
#             today.year
#             - birthdate.year
#             - ((today.month, today.day) < (birthdate.month, birthdate.day))
#         )

#         return age

#     def validate(self, data):
#         check_list = [
#             data["password"] == data["first_name"],
#             data["password"] == data["last_name"],
#             data["password"] == data["last_name"] + data["first_name"],
#             data["password"] == data["first_name"] + data["last_name"],
#             data["password"] == data["username"],
#             data["password"] == data["email"],
#             data["password"] == data["birthdate"],
#         ]
#         if any(check_list):
#             raise serializers.ValidationError(
#                 "Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles."
#             )

#         if len(data["password"]) < 8:
#             raise serializers.ValidationError(
#                 "Votre mot de passe doit contenir au minimum 8 caractères."
#             )
#         if data["password"].isdigit():
#             raise serializers.ValidationError(
#                 "Votre mot de passe ne peut pas être entièrement numérique."
#             )
#         if data["password"].isalpha():
#             raise serializers.ValidationError(
#                 "Votre mot de passe doit contenir au moins un chiffre."
#             )
#         if data["password"] != data["password_confirm"]:
#             raise serializers.ValidationError(
#                 "Les deux mots de passe ne correspondent pas."
#             )
#         if data["birthdate"]:
#             age = self.age(data["birthdate"])
#             if age and age <= 15 and data["can_data_be_shared"]:
#                 raise serializers.ValidationError(
#                     "Votre age doit être supérieur à 15ans pour partager vos données."
#                 )
#         else:
#             data["can_data_be_shared"] = False
#             data["can_be_contacted"] = False

#         return data

#     def to_representation(self, instance):
#         """hide the user's email if the "can_be_contacted" field is False"""

#         data = super().to_representation(instance)
#         request = self.context.get("request")
#         if request and request.user.username != instance.username:
#             data.pop("password")
#             if not instance.can_be_contacted:
#                 data.pop("email")

#         return data

#     def create(self, validated_data):
#         validated_data.pop(
#             "password_confirm"
#         )  # Retirez le champ de confirmation avant la création
#         user = User.objects.create_user(**validated_data)

#         return user
