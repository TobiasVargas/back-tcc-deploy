from django.db import models
from django.contrib.auth.models import User


class Saldo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)


class SolicitacaoSaque(models.Model):
    STATUS_CHOICES = (
        (1, 'Solicitada'),
        (2, 'Recusada'),
        (3, 'Efetuada')
    )

    mercado_pago = models.CharField(max_length=254)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    comprovante = models.FileField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)


class Lancamento(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel_em = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estornado = models.BooleanField(default=False)
