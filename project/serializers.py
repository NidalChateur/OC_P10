from datetime import date
from dataclasses import fields

from pyexpat import model
from tabnanny import verbose
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
