from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserInfo, DeliveryInfo


class BootstrapForForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control text-dark'})


class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserInfo.ROLE_CHOICES)
    username = forms.CharField(max_length=150, help_text="",
                               widget=forms.TextInput(attrs={'class': 'form-control text-dark'}))
    email = forms.EmailField(help_text="Required. Please enter a valid email address.",
                             required=True, widget=forms.EmailInput(attrs={'class': 'form-control text-dark'}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control text-dark'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control text-dark'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control text-dark'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, help_text="")
    password = forms.CharField(widget=forms.PasswordInput, help_text="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control text-dark'})

    class Meta:
        model = User
        fields = ['username', 'password']


class CheckoutForm(BootstrapForForm, forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        exclude = ['user', ]


class CardPaymentForm(forms.Form):
    cardholder_name = forms.CharField(label='Cardholder Name', max_length=255)
    card_number = forms.CharField(label='Card Number', max_length=16)
    CVV = forms.CharField(label='CVV', max_length=255)
    valid_until = forms.DateField(label='Valid Until', widget=forms.DateInput(attrs={'type': 'date'}))