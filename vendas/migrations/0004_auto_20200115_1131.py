# Generated by Django 2.1 on 2020-01-15 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0003_auto_20200115_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venda',
            options={'permissions': (('setar_nfe', 'Alterar status NFE'), ('permissao_2', 'permissao 2'))},
        ),
    ]
