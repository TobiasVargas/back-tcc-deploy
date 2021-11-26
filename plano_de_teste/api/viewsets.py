from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from plano_de_teste.models import PlanoDeTeste, TipoProduto, Navegador, Dispositivo, Operadora, SistemaOperacional
from plano_de_teste.api.serializers import PlanoDeTesteSerializer, TipoProdutoSerializer, NavegadorSerializer, \
    DispositivoSerializer, OperadoraSerializer, SistemaOperacionalSerializer, PlanoDeTesteSerializerCreateUpdate, \
    DispositivoSerializerCreateUpdate
from tarefa_de_teste.models import ExecucaoTeste, PublicacaoDoPlanoDeTeste, ManifestacaoInteresse
from django.db.models import Q


class TipoProdutoViewset(viewsets.ModelViewSet):
    queryset = TipoProduto.objects.all()
    serializer_class = TipoProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().create(self, request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().update(self, request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().partial_update(self, request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().destroy(self, request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PlanoDeTesteViewset(viewsets.ModelViewSet):
    queryset = PlanoDeTeste.objects.all()
    serializer_class = PlanoDeTesteSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            serializer = PlanoDeTesteSerializerCreateUpdate(data=request.data)
            if serializer.is_valid():
                novo_plano_teste = PlanoDeTeste()
                novo_plano_teste.user = request.user
                novo_plano_teste.tipo_produto = TipoProduto.objects.filter(id=serializer.data['tipo_produto']).first()
                novo_plano_teste.nome_produto = serializer.data['nome_produto']
                novo_plano_teste.url_acesso = serializer.data['url_acesso']
                novo_plano_teste.descricao = serializer.data['descricao']
                novo_plano_teste.detalhes_autenticacao = serializer.data['detalhes_autenticacao']
                novo_plano_teste.versao_produto = serializer.data['versao_produto']
                novo_plano_teste.estado_lancamento_produto = serializer.data['estado_lancamento_produto']
                novo_plano_teste.save()
                serializer = self.get_serializer(novo_plano_teste)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            serializer = PlanoDeTesteSerializerCreateUpdate(data=request.data)
            if serializer.is_valid():
                plano_de_teste = self.get_object()
                if not plano_de_teste:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                if not plano_de_teste.user == request.user:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                plano_de_teste.nome_produto = serializer.data['nome_produto']
                plano_de_teste.url_acesso = serializer.data['url_acesso']
                plano_de_teste.descricao = serializer.data['descricao']
                plano_de_teste.detalhes_autenticacao = serializer.data['detalhes_autenticacao']
                plano_de_teste.versao_produto = serializer.data['versao_produto']
                plano_de_teste.estado_lancamento_produto = serializer.data['estado_lancamento_produto']
                plano_de_teste.save()
                serializer = self.get_serializer(plano_de_teste)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        plano_de_teste = self.get_object()
        if not plano_de_teste:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not plano_de_teste.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = PlanoDeTeste.objects.filter(user=request.user)
        return super().list(self, request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def publicados(self, request, *args, **kwargs):
        self.queryset = PlanoDeTeste.objects.filter(Q(publicacaodoplanodeteste__isnull=False),
                                                    Q(publicacaodoplanodeteste__status=2),
                                                    ~Q(publicacaodoplanodeteste__manifestacaointeresse__status=2))
        param_filtro = request.GET.get('filtro', '')
        if param_filtro != '':
            self.queryset = self.queryset.filter(nome_produto__icontains=param_filtro) | \
                            self.queryset.filter(descricao__icontains=param_filtro) | \
                            self.queryset.filter(dispositivo__nome__icontains=param_filtro) | \
                            self.queryset.filter(dispositivo__sistema_operacional__nome__icontains=param_filtro)
        return super().list(self, request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def em_testes(self, request, *args, **kwargs):
        manifestacoes = ManifestacaoInteresse.objects.filter(user=request.user, status=2) | \
                        ManifestacaoInteresse.objects.filter(publicacao__plano_de_teste__user=request.user, status=2)
        self.queryset = PlanoDeTeste.objects.filter(publicacaodoplanodeteste__manifestacaointeresse__in=manifestacoes)
        return super().list(self, request, *args, **kwargs)


class NavegadorViewset(viewsets.ModelViewSet):
    queryset = Navegador.objects.all()
    serializer_class = NavegadorSerializer


class DispositivoViewset(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer

    def create(self, request, *args, **kwargs):
        serializer = DispositivoSerializerCreateUpdate(data=request.data)
        if serializer.is_valid():
            novo_dispositivo = Dispositivo()
            novo_dispositivo.plano_de_teste = PlanoDeTeste.objects.filter(id=serializer.data['plano_de_teste']).first()
            novo_dispositivo.sistema_operacional_id = serializer.data['sistema_operacional']
            novo_dispositivo.nome = serializer.data['nome']
            novo_dispositivo.save()
            serializer = self.get_serializer(novo_dispositivo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = DispositivoSerializerCreateUpdate(data=request.data)
        if serializer.is_valid():
            dispositivo = self.get_object()
            if not dispositivo:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if dispositivo.plano_de_teste.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            sistema_operacional = SistemaOperacional.objects.filter(id=serializer.data['sistema_operacional']).first()
            if not sistema_operacional:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            dispositivo.nome = serializer.data['nome']
            dispositivo.sistema_operacional_id = serializer.data['sistema_operacional']
            dispositivo.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OperadoraViewset(viewsets.ModelViewSet):
    queryset = Operadora.objects.all()
    serializer_class = OperadoraSerializer


class SistemaOperacionalViewset(viewsets.ModelViewSet):
    queryset = SistemaOperacional.objects.all()
    serializer_class = SistemaOperacionalSerializer
