from rest_framework import serializers
from caso_de_teste.models import CasoDeTeste, PreCondicao, Acao
from registro_de_falha.api.serializers import RegistroDeTesteSerializer


class PreCondicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreCondicao
        fields = '__all__'


class AcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acao
        fields = '__all__'


class CasoDeTesteSerializer(serializers.ModelSerializer):
    pre_condicoes = PreCondicaoSerializer(many=True, read_only=True)
    acoes = AcaoSerializer(many=True, read_only=True)
    registrodeteste = RegistroDeTesteSerializer(many=False, read_only=True, allow_null=True)

    class Meta:
        model = CasoDeTeste
        fields = '__all__'
