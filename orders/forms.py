from django import forms
from .models import *


from django.contrib.auth import get_user_model
User = get_user_model()

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['address']
        
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['address'].queryset = Address.objects.filter(user=user, is_archived=False)
        self.fields['address'].empty_label = None
        
        default_address = self.fields['address'].queryset.first()
        if default_address:
            self.fields['address'].initial = default_address

        self.preselected_address_id = self.fields['address'].initial.id if default_address else None
