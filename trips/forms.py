from django import forms

from trips.models import TripRequest


class TripRequestForm(forms.ModelForm):
    class Meta:
        model = TripRequest
        fields = ['location_a', 'location_b', 'comments',]
