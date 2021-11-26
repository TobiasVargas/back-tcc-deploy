from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from reclamacoes.models import Reclamacao
from reclamacoes.api.serializers import ReclamacaoSerializer


class ReclamacaoViewset(viewsets.ModelViewSet):
    queryset = Reclamacao.objects.all()
    serializer_class = ReclamacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ReclamacaoSerializer(data=request.data)
        if serializer.is_valid():
            reclamacao = Reclamacao()
            reclamacao.user = request.user
            reclamacao.plano_de_teste_id = serializer.data['plano_de_teste']
            reclamacao.descricao = serializer.data['descricao']
            reclamacao.save()
            serializer = ReclamacaoSerializer(instance=reclamacao)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        param_plano_de_teste = request.GET.get('plano_de_teste', '')
        self.queryset = Reclamacao.objects.filter(user=request.user)
        if param_plano_de_teste != '':
            self.queryset = self.queryset.filter(plano_de_teste_id=param_plano_de_teste)
        return super().list(self, request, *args, **kwargs)
