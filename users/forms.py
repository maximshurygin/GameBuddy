from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm, \
    SetPasswordForm, PasswordChangeForm
from django_countries.widgets import CountrySelectWidget

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class LoginUserForm(StyleFormMixin, AuthenticationForm):
    error_messages = {
        'invalid_login': "Неверный Email или пароль. Пожалуйста, проверьте введённые данные и повторите попытку.",
        'inactive': "Этот аккаунт неактивен.",
    }


class RegisterUserForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'nickname', 'password1', 'password2')


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'nickname',
            'gender',
            'age',
            'country',
        ]
        labels = {
            'email': 'Email',
            'nickname': 'Никнейм',
            'gender': 'Пол',
            'age': 'Возраст',
            'country': 'Страна',
        }

    # def clean_date_of_birth(self):
    #     from django.utils import timezone  # Импорт внутри функции для избежания циклических импортов
    #     date_of_birth = self.cleaned_data.get('date_of_birth')
    #     if date_of_birth and date_of_birth > timezone.now().date():
    #         raise forms.ValidationError('Дата рождения не может быть в будущем.')
    #     return date_of_birth

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True


class PasswordResetCustomForm(StyleFormMixin, PasswordResetForm):
    pass


class SetPasswordCustomForm(StyleFormMixin, SetPasswordForm):
    pass


class UserPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    pass
