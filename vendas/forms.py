from django import forms


class ItemPedidoForm(forms.Form):
    produto_id = forms.CharField(label='ID do Protudo', max_length=100)
    quantidade = forms.IntegerField(label='Quantiade')
    desconto = forms.DecimalField(label='Desconto', max_digits=7, decimal_places=2)

