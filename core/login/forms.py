import requests
from django import forms
from django.contrib.auth import authenticate

from core.user.models import User


class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese un password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def get_or_create_user_api(self, username, password):
        response = {'resp': False}
        try:
            payload = {'username': username, 'password': password}
            headers = {'Authorization': 'Token 7b031fe594f0ca2fb34708e9109c5f9ea89008f7'}
            r = requests.post('http://192.168.20.62:8000/api/login/', data=payload, headers=headers)
            if r.status_code == 200:
                response = r.json()
                if response['resp']:
                    search = User.objects.filter(username=response['user']['username'])
                    if not search.exists():
                        user = User()
                        user.username = response['user']['username']
                        user.first_name = response['user']['first_name']
                        user.last_name = response['user']['last_name']
                        user.email = response['user']['email']
                        user.set_password(user.username)
                        user.is_superuser = True
                        user.is_staff = True
                        user.save()
            else:
                response['msg'] = r.text
        except Exception as e:
            response = {'resp': False, 'msg': str(e)}
        return response

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username', '')
        password = cleaned.get('password', '')
        if len(username) == 0:
            raise forms.ValidationError('Ingrese un username')
        elif len(password) == 0:
            raise forms.ValidationError('Ingrese un password')
        # response_api = self.get_or_create_user_api(username, password)
        # if not response_api.get('resp'):
        #     raise forms.ValidationError(response_api['msg'])
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Por favor introduzca el nombre de usuario y la clave correctos para una cuenta de personal')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese un password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita el password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned
