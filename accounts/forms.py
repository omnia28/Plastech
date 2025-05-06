from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 100%; height: 100%; padding: 20px; font-size: 18px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width: 100%; height: 100%; padding: 20px; font-size: 18px;'}))

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'style': 'width: 100%; padding: 8px; font-size: 16px; border: 1px solid #ccc; box-sizing: border-box; margin-top: 5px;'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'style': 'width: 100%; padding: 8px; font-size: 16px; border: 1px solid #ccc; box-sizing: border-box; margin-top: 5px;'})
    )

    class Meta(UserCreationForm.Meta):
        fields = ("username", "first_name", "email") # Include 'email' here if you want it in the base form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'style': 'width: 100%; padding: 8px; font-size: 16px; border: 1px solid #ccc; box-sizing: border-box;'})
        # self.fields['password2'].widget.attrs.update({'style': 'width: 100%; padding: 8px; font-size: 16px; border: 1px solid #ccc; box-sizing: border-box; margin-top: 5px;'})
        # self.fields['password'].widget.attrs.update({'style': 'width: 100%; padding: 8px; font-size: 16px; border: 1px solid #ccc; box-sizing: border-box; margin-top: 5px;'})
