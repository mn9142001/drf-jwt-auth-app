from rest_framework import serializers
from django.contrib.auth.models import User

class PromoteUserPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        extra_kwargs = {
            'email' : {"read_only" : True}
        }
        fields = ('is_staff', 'email', 'id')