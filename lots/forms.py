from django import forms

from lots.models import UserLot, UserLotGallery


class UserLotForm(forms.ModelForm):
    class Meta:
        model = UserLot
        fields = ['title', 'description', 'max_price']


class LotGalleryForm(forms.ModelForm):
    class Meta:
        model = UserLotGallery
        fields = ['image', 'main']
