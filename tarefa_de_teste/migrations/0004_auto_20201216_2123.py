# Generated by Django 3.1.1 on 2020-12-16 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plano_de_teste', '0004_auto_20201025_1852'),
        ('tarefa_de_teste', '0003_publicacaodoplanodeteste_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacaodoplanodeteste',
            name='plano_de_teste',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='plano_de_teste.planodeteste'),
        ),
    ]
