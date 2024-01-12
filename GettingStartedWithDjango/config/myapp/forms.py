from django.forms import ModelForm
from myapp.models import Booking

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"