from django import forms


class InputAmountForm(forms.Form):
    """
    Форма, используемая при работе с корзиной
    """
    count = forms.IntegerField(required=False, min_value=1, max_value=100)
    product_id = forms.IntegerField(required=True)
    seller_id = forms.IntegerField(required=True)

    # count - количество товара
