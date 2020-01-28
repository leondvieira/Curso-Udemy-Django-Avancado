from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from clientes.models import Person
from produtos.models import Produto
from vendas.managers import VendaManager


class Venda(models.Model):
    numero = models.CharField(max_length=7)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    impostos = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pessoa = models.ForeignKey(Person, null=True, blank=True, on_delete=models.PROTECT)
    nfe_emitida = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('setar_nfe', 'Alterar status NFE'),
            ('ver_dashboard', 'Visualizar Dashboard'),
        )

    # def get_total(self):
    #     total = 0
    #     for produto in self.produtos.all():
    #         total += produto.preco
    #
    #     return (total - self.desconto) - self.impostos

    objects = VendaManager()

    def calcular_total(self):
        total = self.itemdopedido_set.all().aggregate(
            total_pedido=Sum((F('quantidade') * F('produto__preco')) - F('desconto'), output_field=FloatField())
        )['total_pedido'] or 0

        total = total - float(self.impostos) - float(self.desconto)
        self.valor = total
        Venda.objects.filter(id=self.id).update(valor=total)

    def __str__(self):
        return self.numero


class ItemDoPedido(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()
    desconto = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.venda.numero + ' - ' + self.produto.descricao


@receiver(post_save, sender=ItemDoPedido)
def update_vendas_total(sender, instance, **kwargs):
    instance.venda.calcular_total()


@receiver(post_save, sender=Venda)
def update_vendas_total2(sender, instance, **kwargs):
    instance.calcular_total()
