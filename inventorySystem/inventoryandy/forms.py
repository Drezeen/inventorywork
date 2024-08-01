from django.forms import ModelForm
from .models import Inventoryandy

class AddInventoryForm(ModelForm):
    class Meta:
        model = Inventoryandy
        fields = ['barcode', 'name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']

class UpdateInventoryForm(ModelForm):
    class Meta:
        model = Inventoryandy
        fields = ['barcode', 'name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']
