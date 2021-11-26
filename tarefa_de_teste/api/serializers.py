from rest_framework import serializers
from tarefa_de_teste.models import PublicacaoDoPlanoDeTeste, ManifestacaoInteresse, ExecucaoTeste
from core.api.serializers import UserContribSerializer


class PublicacaoPlanoTesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicacaoDoPlanoDeTeste
        fields = '__all__'


class ManifestacaoInteresseSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = ManifestacaoInteresse
        exclude = ['user']


class ManifestacaoInteresseSerializerList(serializers.ModelSerializer):
    user = UserContribSerializer(many=False, read_only=True)

    class Meta:
        model = ManifestacaoInteresse
        fields = '__all__'


class ExecucaoTesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecucaoTeste
        fields = '__all__'
