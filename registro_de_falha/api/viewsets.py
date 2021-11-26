from rest_framework import viewsets
from registro_de_falha.api.serializers import AnexoRegistroFalhaSerializer, PassoReproducaoFalhaSerializer, \
    RegistroDeTesteSerializer
from registro_de_falha.models import PassoReproducaoFalha, AnexoRegistroFalha, RegistroDeTeste


class RegistroDeTesteViewset(viewsets.ModelViewSet):
    queryset = RegistroDeTeste.objects.all()
    serializer_class = RegistroDeTesteSerializer


class PassoReproducaoFalhaViewset(viewsets.ModelViewSet):
    queryset = PassoReproducaoFalha.objects.all()
    serializer_class = PassoReproducaoFalhaSerializer


class AnexoRegistroFalhaViewset(viewsets.ModelViewSet):
    queryset = AnexoRegistroFalha.objects.all()
    serializer_class = AnexoRegistroFalhaSerializer
