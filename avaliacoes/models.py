from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from plano_de_teste.models import PlanoDeTeste


class Avaliacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user_avaliado = models.ForeignKey(User, on_delete=models.CASCADE, related_name="avaliado")
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    descricao = models.TextField(null=True, blank=True)
    plano_de_teste = models.ForeignKey(PlanoDeTeste, on_delete=models.CASCADE)
