from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CadastroForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': 'true',
            'type': 'text',
            'class': 'input-form',
            'name': 'username',
            'placeholder': 'Username',
            'min_length': '6',
        })
        self.fields['email'].widget.attrs.update({
            'required': 'true',
            'type': 'email',
            'class': 'input-form',
            'name': 'email',
            'placeholder': 'Email (Opcional)',
        })
        self.fields['password1'].widget.attrs.update({
            'required': 'true',
            'type': 'password',
            'class': 'input-form',
            'name': 'password1',
            'placeholder': 'Password',
            'min_length': '6',
        })
        self.fields['password2'].widget.attrs.update({
            'required': 'true',
            'type': 'password',
            'class': 'input-form',
            'name': 'password2',
            'placeholder': 'Confirm password',
            'min_length': '6',
        })
    class Meta:
        model = User
        fields =  ['username', 'email', 'password1', 'password2']



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'required': 'true',
            'type': 'text',
            'class': 'input-form',
            'name': 'username',
            'placeholder': 'Username',
            'min_length': '6',
        })
    )
    password =forms.CharField(
        widget=forms.TextInput(attrs={
            'required': 'true',
            'type': 'password',
            'class': 'input-form',
            'name': 'password',
            'placeholder': 'Password',
            'min_length': '6',
        })
    )
    
# class LoginForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({
#             'required': 'true',
#             'type': 'text',
#             'class': 'input-form',
#             'name': 'username',
#             'placeholder': 'Username',
#             'min_length': '6',
#         })
#         self.fields['password'].widget.attrs.update({
#             'required': 'true',
#             'type': 'password',
#             'class': 'input-form',
#             'name': 'password',
#             'placeholder': 'Password',
#             'min_length': '6',
#         })
#     class Meta:
#         model = User
#         fields = ['username', 'password']

