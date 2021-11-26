from django.contrib import admin
from pagamentos.models import Saldo, Lancamento, SolicitacaoSaque


admin.site.register(Saldo)
admin.site.register(Lancamento)
admin.site.register(SolicitacaoSaque)
