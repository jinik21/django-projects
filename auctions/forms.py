from django import forms
from .models import Category, Listing


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('Title', 'Description', 'Starting_Bid', 'Category', 'Image_Link')
        widgets = {'Category' : forms.Select(choices=Category.objects.all(), attrs={'class' : 'form-control'}),
                   'Title': forms.TextInput(attrs={'class': 'form-control'}),
                   'Description': forms.TextInput(attrs={'class': 'form-control'}),
                   'Starting_Bid': forms.NumberInput(attrs={'class': 'form-control'})} 

