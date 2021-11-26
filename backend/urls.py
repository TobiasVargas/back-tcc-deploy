from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_swagger.views import get_swagger_view
from backend import settings
from plano_de_teste.api.viewsets import PlanoDeTesteViewset, TipoProdutoViewset, SistemaOperacionalViewset, \
    NavegadorViewset, OperadoraViewset, DispositivoViewset
from core.api.viewsets import UserProfileViewset
from cenario_de_teste.api.viewsets import CenarioDeTesteViewset
from caso_de_teste.api.viewsets import CasoDeTesteViewset, AcaoViewset, PreCondicaoViewset
from tarefa_de_teste.api.viewsets import PublicacaoPlanoDeTesteViewset, ManifestacaoInteresseViewset, \
    ExecucaoTesteViewset
from registro_de_falha.api.viewsets import RegistroDeTesteViewset, AnexoRegistroFalhaViewset, \
    PassoReproducaoFalhaViewset
from pagamentos.api.viewsets import SaldoViewset, SolicitacaoSaqueViewset
from avaliacoes.api.viewsets import AvaliacaoViewset
from reclamacoes.api.viewsets import ReclamacaoViewset


def redirect_to_admin(request):
    return HttpResponseRedirect('/admin')


schema_view = get_swagger_view(title='TCC API')

router_v1 = routers.DefaultRouter()
router_v1.register('planos-de-teste', PlanoDeTesteViewset)
router_v1.register('tipos-de-produto', TipoProdutoViewset)
router_v1.register('sistemas-operacionais', SistemaOperacionalViewset)
router_v1.register('navegadores', NavegadorViewset)
router_v1.register('operadoras', OperadoraViewset)
router_v1.register('dispositivos', DispositivoViewset)
router_v1.register('users', UserProfileViewset)
router_v1.register('cenarios-de-teste', CenarioDeTesteViewset)
router_v1.register('casos-de-teste', CasoDeTesteViewset)
router_v1.register('acoes', AcaoViewset)
router_v1.register('pre-condicoes', PreCondicaoViewset)
router_v1.register('tarefa-de-teste', PublicacaoPlanoDeTesteViewset)
router_v1.register('manifestacao-de-interesse', ManifestacaoInteresseViewset)
router_v1.register('execucao-de-teste', ExecucaoTesteViewset)
router_v1.register('registro-de-teste', RegistroDeTesteViewset)
router_v1.register('anexo-registro-de-falha', AnexoRegistroFalhaViewset)
router_v1.register('passo-reproducao-falha', PassoReproducaoFalhaViewset)
router_v1.register('saldo', SaldoViewset)
router_v1.register('avaliacoes', AvaliacaoViewset)
router_v1.register('reclamacoes', ReclamacaoViewset)
router_v1.register('solicitacoes-de-saque', SolicitacaoSaqueViewset)

urlpatterns = [
    path('', redirect_to_admin),
    path('swagger/', schema_view, name="docs"),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/v1/', include('rest_framework.urls')),
    path('api/v1/', include(router_v1.urls)),
    path('openapi', get_schema_view(
            title='API TCC',
            description='Docs API TCC',
            version='0.1.1'
        ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    # em caso de erro alterar a linha staticfiles para static no caminho do virtualenv
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
