from django.db import models
from caso_de_teste.models import CasoDeTeste
from plano_de_teste.models import SistemaOperacional, Navegador, Dispositivo, Operadora
from tarefa_de_teste.models import ExecucaoTeste


class RegistroDeTeste(models.Model):
    TIPOS_REGISTRO_TESTE_CHOICES = (
        (1, 'Aprovado'),
        (2, 'Com Falha'),
    )

    tipo = models.IntegerField(choices=TIPOS_REGISTRO_TESTE_CHOICES)
    descricao_da_falha = models.TextField(null=True, blank=True)
    caso_de_teste = models.OneToOneField(CasoDeTeste, on_delete=models.CASCADE)
    navegador = models.ForeignKey(Navegador, on_delete=models.CASCADE, null=True, blank=True)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, null=True, blank=True)
    operadora = models.ForeignKey(Operadora, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def passos_reproducao_falha(self):
        return self.passoreproducaofalha_set

    def anexos_registro_falha(self):
        return self.anexoregistrofalha_set


class PassoReproducaoFalha(models.Model):
    descricao_passo = models.TextField()
    registro_de_teste = models.ForeignKey(RegistroDeTeste, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao_passo


class AnexoRegistroFalha(models.Model):
    anexo_falha = models.ImageField(upload_to='screen_anexo_registro_falha')
    registro_de_teste = models.ForeignKey(RegistroDeTeste, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
