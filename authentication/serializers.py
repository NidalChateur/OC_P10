from rest_framework import serializers
from django.contrib.auth import get_user_model

from datetime import date
from dataclasses import fields


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "birthdate",
            "image",
            "can_be_contacted",
            "can_data_be_shared",
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
        age = self.age(data["birthdate"])
        if age <= 15 and data["can_data_be_shared"]:
            raise serializers.ValidationError(
                "Votre age doit être supérieur à 15ans pour partager vos données."
            )

        return data
