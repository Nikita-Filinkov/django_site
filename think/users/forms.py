from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.forms import ModelForm


class LoginUserForms(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторение пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-male',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    # def clean_password_2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password_2']:
    #         raise forms.ValidationError("Пароли не совпадают")
    #     return cd['password']
    #
    def clean_email(self):
        cd = self.cleaned_data
        email = cd['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такая почта уже есть')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    email = forms.CharField(disabled=True, label='Email', widget=forms.TextInput(attrs={'class': 'form_input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form_input'}),
            'last_name': forms.TextInput(attrs={'class': 'form_input'})
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Подтверждение нового пароля', widget=forms.PasswordInput())


# class UserPasswordReset(PasswordResetForm):
#     tem
