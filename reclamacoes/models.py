from django.db import models
from plano_de_teste.models import PlanoDeTeste
from django.contrib.auth.models import User


class Reclamacao(models.Model):
    STATUS_CHOICES = (
        (1, 'Aberta'),
        (2, 'Julgada Vitória'),
        (3, 'Julgada Derrota'),
    )

    descricao = models.TextField()
    plano_de_teste = models.ForeignKey(PlanoDeTeste, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.descricao
