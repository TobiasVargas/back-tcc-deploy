from rest_framework import serializers
from core.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    is_analista_de_testes = serializers.BooleanField()
    is_tester = serializers.BooleanField()


class UserContribSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password']


class UserSerializer(serializers.ModelSerializer):
    user = UserContribSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'imagem', 'is_analista_de_testes', 'is_tester']
