from django.db import models
from django.contrib.auth.models import User


class TipoProduto(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

    def plano_de_teste(self):
        return PlanoDeTeste.objects.filter(tipo_produto_id=self.id)


class PlanoDeTeste(models.Model):
    tipo_produto = models.ForeignKey(TipoProduto, on_delete=models.CASCADE)
    nome_produto = models.CharField(max_length=255)
    url_acesso = models.CharField(max_length=255)
    descricao = models.TextField()
    detalhes_autenticacao = models.TextField()
    versao_produto = models.CharField(max_length=50)
    estado_lancamento_produto = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_produto

    def dispositivos(self):
        return Dispositivo.objects.filter(plano_de_teste_id=self.id)

    def navegadores(self):
        return Navegador.objects.filter(plano_de_teste_id=self.id)

    def operadoras(self):
        return Operadora.objects.filter(plano_de_teste_id=self.id)

    def cenarios_de_teste(self):
        return self.cenariodeteste_set


class Operadora(models.Model):
    nome = models.CharField(max_length=100)
    plano_de_teste = models.ForeignKey(PlanoDeTeste, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class SistemaOperacional(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Dispositivo(models.Model):
    nome = models.CharField(max_length=150)
    sistema_operacional = models.ForeignKey(SistemaOperacional, on_delete=models.CASCADE)
    plano_de_teste = models.ForeignKey(PlanoDeTeste, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Navegador(models.Model):
    nome = models.CharField(max_length=150)
    versao = models.CharField(max_length=50)
    plano_de_teste = models.ForeignKey(PlanoDeTeste, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
