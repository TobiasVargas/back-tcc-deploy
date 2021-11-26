from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from cenario_de_teste.api.serializers import CenarioDeTesteSerializer
from cenario_de_teste.models import CenarioDeTeste
from plano_de_teste.models import PlanoDeTeste


class CenarioDeTesteViewset(viewsets.ModelViewSet):
    serializer_class = CenarioDeTesteSerializer
    queryset = CenarioDeTeste.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['plano_de_teste']
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']

    # def create(self, request, *args, **kwargs):
    #     serializer = CenarioDeTesteSerializer(data=request.data)
    #     if serializer.is_valid():
    #         plano_de_teste = PlanoDeTeste.objects.filter(id=serializer.data['plano_de_teste']).first()
    #         if plano_de_teste.user != request.user:
    #             return Response(status=status.HTTP_403_FORBIDDEN)
    #         return super().create(self, request, *args, **kwargs)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def update(self, request, *args, **kwargs):
    #     serializer = CenarioDeTesteSerializer(data=request.data)
    #     if serializer.is_valid():
    #         plano_de_teste = PlanoDeTeste.objects.filter(id=serializer.data['plano_de_teste']).first()
    #         if plano_de_teste.user != request.user:
    #             return Response(status=status.HTTP_403_FORBIDDEN)
    #         return super().update(self, request, *args, **kwargs)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, *args, **kwargs):
    #     cenario_de_teste = self.get_object()
    #     if cenario_de_teste.plano_de_teste.user != request.user:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     return super().destroy(self, request, *args, **kwargs)
