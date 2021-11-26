from caso_de_teste.api.serializers import CasoDeTesteSerializer, PreCondicaoSerializer, AcaoSerializer
from rest_framework import viewsets
from caso_de_teste.models import PreCondicao, Acao, CasoDeTeste


class CasoDeTesteViewset(viewsets.ModelViewSet):
    queryset = CasoDeTeste.objects.all()
    serializer_class = CasoDeTesteSerializer


class PreCondicaoViewset(viewsets.ModelViewSet):
    queryset = PreCondicao.objects.all()
    serializer_class = PreCondicaoSerializer


class AcaoViewset(viewsets.ModelViewSet):
    queryset = Acao.objects.all()
    serializer_class = AcaoSerializer
