from django.db import models
from cenario_de_teste.models import CenarioDeTeste


class CasoDeTeste(models.Model):
    cenario_de_teste = models.ForeignKey(CenarioDeTeste, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    objetivo = models.TextField()
    # resultado = models.TextField(null=True, blank=True)
    # data_execucao = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo

    def pre_condicoes(self):
        return self.precondicao_set

    def acoes(self):
        return self.acao_set


class PreCondicao(models.Model):
    nome = models.CharField(max_length=255)
    caso_de_teste = models.ForeignKey(CasoDeTeste, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Acao(models.Model):
    acao = models.TextField()
    resultado_esperado = models.TextField(null=True, blank=True)
    caso_de_teste = models.ForeignKey(CasoDeTeste, on_delete=models.CASCADE)

    def __str__(self):
        return self.acao
