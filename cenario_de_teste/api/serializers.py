from rest_framework import serializers
from cenario_de_teste.models import CenarioDeTeste
from caso_de_teste.api.serializers import CasoDeTesteSerializer


class CenarioDeTesteSerializer(serializers.ModelSerializer):
    casos_de_teste = CasoDeTesteSerializer(many=True, read_only=True)

    class Meta:
        model = CenarioDeTeste
        fields = '__all__'
