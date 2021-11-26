from rest_framework import serializers
from registro_de_falha.models import RegistroDeTeste, AnexoRegistroFalha, PassoReproducaoFalha


class AnexoRegistroFalhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnexoRegistroFalha
        fields = '__all__'


class PassoReproducaoFalhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassoReproducaoFalha
        fields = '__all__'


class RegistroDeTesteSerializer(serializers.ModelSerializer):
    passos_reproducao_falha = PassoReproducaoFalhaSerializer(many=True, read_only=True, allow_null=True)
    anexos_registro_falha = AnexoRegistroFalhaSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = RegistroDeTeste
        fields = '__all__'
