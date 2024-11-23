

from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class RegisterForm(UserCreationForm):
    """" Form used to register a new user """

    email = forms.EmailField(
        required=True,
        min_length=3,
    )
    # Remove a validação de senha padrão e permite qualquer senha
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
        fields = (
            'email',
            'username',
            'password1',
            'password2',
        )

    def clean_password2(self):
        # Verifica se as senhas coincidem
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            print('Email ja existe')
            self.add_error(
                'email',
                ValidationError('Já existe este e-mail', code='invalid')
            )

        return email
