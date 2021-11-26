from django.contrib import admin
from plano_de_teste.models import TipoProduto, PlanoDeTeste, Operadora, SistemaOperacional, Dispositivo, Navegador


admin.site.register(TipoProduto)
admin.site.register(PlanoDeTeste)
admin.site.register(Operadora)
admin.site.register(SistemaOperacional)
admin.site.register(Dispositivo)
admin.site.register(Navegador)
