# Generated by Django 2.1 on 2020-01-09 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0001_initial'),
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ItensDoPedido',
            new_name='ItemDoPedido',
        ),
    ]