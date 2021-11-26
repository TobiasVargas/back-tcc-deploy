from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='img_user_profile', null=True, blank=True)
    is_analista_de_testes = models.BooleanField(default=False)
    is_tester = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()
