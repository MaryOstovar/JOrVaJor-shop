from django import forms

from home.models import Product


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']


class SearchForm(forms.Form):
    search = forms.CharField()
