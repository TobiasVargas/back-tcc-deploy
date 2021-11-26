from django.db import models
from plano_de_teste.models import PlanoDeTeste
from django.contrib.auth.models import User


class PublicacaoDoPlanoDeTeste(models.Model):
    STATUS_CHOICES = (
        (1, 'Não Publicado'),
        (2, 'Publicado'),
        (3, 'Pausado'),
    )
    plano_de_teste = models.OneToOneField(PlanoDeTeste, on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=2, max_digits=5)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.plano_de_teste.nome_produto


class ManifestacaoInteresse(models.Model):
    STATUS_CHOICES = (
        (1, 'Solicitado'),
        (2, 'Aprovado'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacao = models.ForeignKey(PublicacaoDoPlanoDeTeste, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)


class ExecucaoTeste(models.Model):
    interesse = models.ForeignKey(ManifestacaoInteresse, on_delete=models.CASCADE)
