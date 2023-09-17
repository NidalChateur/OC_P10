from datetime import date
# from dataclasses import fields

# from pyexpat import model
# from tabnanny import verbose
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


# le mot de ne s'envoi pas dans une requête http (manière non sécurisée à revoir)
class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        write_only=True, label="Confirmation du mot de passe"
    )

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
            "password",
            "password_confirm",
        )

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
        check_list = [
            data["password"] == data["first_name"],
            data["password"] == data["last_name"],
            data["password"] == data["last_name"] + data["first_name"],
            data["password"] == data["first_name"] + data["last_name"],
            data["password"] == data["username"],
            data["password"] == data["email"],
            data["password"] == data["birthdate"],
        ]
        if any(check_list):
            raise serializers.ValidationError(
                "Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles."
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

        age = self.age(data["birthdate"])
        if age and age <= 15 and data["can_data_be_shared"]:
            raise serializers.ValidationError(
                "Votre age doit être supérieur à 15ans pour partager vos données."
            )
        return data

    def to_representation(self, instance):
        """hide the user's email if the "can_be_contacted" field is False"""

        data = super().to_representation(instance)
        if not instance.can_be_contacted:
            data.pop("email")
        data.pop("password")

        return data

    def create(self, validated_data):
        validated_data.pop(
            "password_confirm"
        )  # Retirez le champ de confirmation avant la création
        user = User.objects.create_user(**validated_data)
        
        return user
