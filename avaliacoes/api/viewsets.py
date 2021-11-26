from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from avaliacoes.models import Avaliacao
from avaliacoes.api.serializers import AvaliacaoCreateSerializer, AvaliacaoListSerializer


class AvaliacaoViewset(viewsets.ModelViewSet):
    serializer_class = AvaliacaoCreateSerializer
    queryset = Avaliacao.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = AvaliacaoCreateSerializer(data=request.data)
        if serializer.is_valid():
            avaliacao = Avaliacao()
            avaliacao.plano_de_teste_id = serializer.data['plano_de_teste']
            avaliacao.nota = serializer.data['nota']
            avaliacao.descricao = serializer.data['descricao']
            avaliacao.user = request.user
            avaliacao.save()
            serializer = AvaliacaoListSerializer(instance=avaliacao)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        self.serializer_class = AvaliacaoListSerializer
        self.queryset = Avaliacao.objects.all()

        param_plano_de_teste = request.GET.get('plano_de_teste', '')
        if param_plano_de_teste != '':
            self.queryset = self.queryset.filter(plano_de_teste_id=param_plano_de_teste)
        return super().list(self, request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def by_user(self, request, *args, **kwargs):
        param_user = request.GET.get('user', '')
        if param_user == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.queryset = Avaliacao.objects.filter(user=param_user)
        return super().list(self, request, *args, **kwargs)
