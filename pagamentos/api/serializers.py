from pagamentos.models import SolicitacaoSaque, Saldo
from rest_framework import serializers


class SaldoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saldo
        fields = '__all__'


class SolicitacaoSaqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacaoSaque
        # fields = '__all__'
        exclude = ['user']


class ValorAAdicionarSerializer(serializers.Serializer):
    valor = serializers.DecimalField(max_digits=10, decimal_places=2)
