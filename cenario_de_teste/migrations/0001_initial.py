# Generated by Django 3.1.1 on 2020-09-15 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plano_de_teste', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CenarioDeTeste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('plano_de_teste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plano_de_teste.planodeteste')),
            ],
        ),
    ]
