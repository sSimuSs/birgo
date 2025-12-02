from django import forms

from trips.models import TripRequest


class TripRequestForm(forms.ModelForm):
    """ Form for creating/editing trip requests from passenger users """
    class Meta:
        model = TripRequest
        fields = ['location_a', 'location_b', 'comments',]
