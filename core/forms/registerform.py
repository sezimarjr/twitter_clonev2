

from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.validators import UnicodeUsernameValidator


class RegisterForm(UserCreationForm):
    """ Form used to register a new user """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove as classes de erro que fazem as mensagens aparecerem
        self.error_css_class = ''
        self.required_css_class = ''

        # Configura placeholders e classes CSS
        placeholders = {
            'email': 'Digite seu e-mail',
            'username': 'Escolha um nome de usuário',
            'password1': 'Crie uma senha',
            'password2': 'Repita a senha'
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name, ''),
                'class': 'form-control'
            })
            # Remove a validação inicial
            field.required = False
            # Remove todos os validadores dos campos de senha

    email = forms.EmailField(
        min_length=3,
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Senha",
        min_length=5,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirmar Senha",
        min_length=5,
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()

        # Só valida se o formulário foi submetido (tem dados POST)
        if not self.data:
            return cleaned_data

        # # Validação dos campos obrigatórios
        # required_fields = ['email', 'username', 'password1', 'password2']
        # for field_name in required_fields:
        #     if not cleaned_data.get(field_name):
        #         self.add_error(field_name, "Este campo é obrigatório.")

        # Validações específicas
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "As senhas não coincidem.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Só valida se o formulário foi submetido
        if not self.data:
            return email

        if User.objects.filter(email=email).exists():
            raise ValidationError('Já existe este e-mail', code='invalid')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Só valida se o formulário foi submetido
        if not self.data:
            return username

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                'Este nome de usuário já está em uso.', code='invalid')
        return username
