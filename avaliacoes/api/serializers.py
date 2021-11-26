from avaliacoes.models import Avaliacao
from rest_framework import serializers


class AvaliacaoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        exclude = ['user']


class AvaliacaoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'
