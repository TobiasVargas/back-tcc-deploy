from rest_framework import serializers
from reclamacoes.models import Reclamacao


class ReclamacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reclamacao
        # fields = '__all__'
        exclude = ['user']
