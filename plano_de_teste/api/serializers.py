from rest_framework import serializers
from plano_de_teste.models import PlanoDeTeste, Dispositivo, Operadora, Navegador, SistemaOperacional, TipoProduto
from cenario_de_teste.api.serializers import CenarioDeTesteSerializer
from tarefa_de_teste.api.serializers import PublicacaoPlanoTesteSerializer
from django.contrib.auth.models import User
from avaliacoes.models import Avaliacao
from avaliacoes.api.serializers import AvaliacaoListSerializer


class TipoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProduto
        fields = '__all__'


class SistemaOperacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SistemaOperacional
        fields = '__all__'


class DispositivoSerializer(serializers.ModelSerializer):
    sistema_operacional = SistemaOperacionalSerializer(many=False, read_only=True)

    class Meta:
        model = Dispositivo
        fields = '__all__'


class DispositivoSerializerCreateUpdate(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = '__all__'


class OperadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operadora
        fields = '__all__'


class NavegadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navegador
        fields = '__all__'


class UserPlanoDeTesteSerializer(serializers.ModelSerializer):
    avaliacao_set = AvaliacaoListSerializer(read_only=True, many=True, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'avaliacao_set']


class PlanoDeTesteSerializer(serializers.ModelSerializer):
    operadoras = OperadoraSerializer(many=True, read_only=True)
    dispositivos = DispositivoSerializer(many=True, read_only=True)
    navegadores = NavegadorSerializer(many=True, read_only=True)
    tipo_produto = TipoProdutoSerializer(many=False, read_only=True)
    cenarios_de_teste = CenarioDeTesteSerializer(many=True, read_only=True)
    publicacaodoplanodeteste = PublicacaoPlanoTesteSerializer(many=False, read_only=True, allow_null=True)
    user = UserPlanoDeTesteSerializer(read_only=True, many=False)

    class Meta:
        model = PlanoDeTeste
        fields = '__all__'


class PlanoDeTesteSerializerCreateUpdate(serializers.ModelSerializer):
    class Meta:
        model = PlanoDeTeste
        exclude = ['user']
