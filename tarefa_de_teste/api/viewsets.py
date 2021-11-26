import datetime
from datetime import date

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from tarefa_de_teste.models import ManifestacaoInteresse, ExecucaoTeste, PublicacaoDoPlanoDeTeste
from tarefa_de_teste.api.serializers import PublicacaoPlanoTesteSerializer, ExecucaoTesteSerializer, \
    ManifestacaoInteresseSerializerCreate, ManifestacaoInteresseSerializerList
from pagamentos.models import Saldo, Lancamento


class PublicacaoPlanoDeTesteViewset(viewsets.ModelViewSet):
    queryset = PublicacaoDoPlanoDeTeste.objects.all()
    serializer_class = PublicacaoPlanoTesteSerializer

    def create(self, request, *args, **kwargs):
        serializer = PublicacaoPlanoTesteSerializer(data=request.data)
        if serializer.is_valid():
            publicacao = PublicacaoDoPlanoDeTeste()
            publicacao.plano_de_teste_id = serializer.data['plano_de_teste']
            publicacao.valor = serializer.data['valor']
            publicacao.status = 1
            publicacao.save()

            saldo = Saldo.objects.filter(user=publicacao.plano_de_teste.user).first()
            saldo.valor = float(saldo.valor) - float(serializer.data['valor'])
            saldo.save()

            serializer = PublicacaoPlanoTesteSerializer(instance=publicacao)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManifestacaoInteresseViewset(viewsets.ModelViewSet):
    queryset = ManifestacaoInteresse.objects.all()
    serializer_class = ManifestacaoInteresseSerializerCreate

    def list(self, request, *args, **kwargs):
        self.serializer_class = ManifestacaoInteresseSerializerList
        self.queryset = ManifestacaoInteresse.objects.filter(publicacao__plano_de_teste__user=request.user, status=1)
        return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ManifestacaoInteresseSerializerList
        return super().retrieve(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = ManifestacaoInteresseSerializerCreate(data=request.data)
        if serializer.is_valid():
            interesse = ManifestacaoInteresse()
            interesse.user = request.user
            interesse.publicacao_id = serializer.data['publicacao']
            interesse.save()
            serializer = ManifestacaoInteresseSerializerList(instance=interesse)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def aprovar(self, request, *args, **kwargs):
        manifestacao = self.get_object()
        manifestacao.status = 2
        manifestacao.save()

        valor = manifestacao.publicacao.valor

        lancamento = Lancamento()
        lancamento.valor = valor
        lancamento.disponivel_em = date.today() + datetime.timedelta(days=30)
        lancamento.user = manifestacao.user
        lancamento.save()

        serializer = ManifestacaoInteresseSerializerCreate(instance=manifestacao)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExecucaoTesteViewset(viewsets.ModelViewSet):
    serializer_class = ExecucaoTesteSerializer
    queryset = ExecucaoTeste.objects.all()
