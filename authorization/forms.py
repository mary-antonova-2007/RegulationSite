from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm
from .models import Profile


class ExtendedUserCreationForm(UserCreationForm):
    # Пример для поля username
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    # Аналогично для password1 и password2
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'})
    )

    def __init__(self, *args, **kwargs):
        super(ExtendedUserCreationForm, self).__init__(*args, **kwargs)
        self.profile_form = ProfileForm()

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Если у формы есть связанная форма профиля, обновляем профиль
            if hasattr(self, 'profile_form'):
                profile_data = self.cleaned_data.get('profile_form')  # Получаем данные из profile_form
                profile, created = Profile.objects.get_or_create(user=user)  # Получаем или создаем профиль
                if not created:
                    # Если профиль уже существует, обновляем его
                    for field, value in profile_data.items():
                        setattr(profile, field, value)
                profile.save()
        return profile, user

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'groups',)


class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Логин'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})


class ProfileForm(ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birth_date', 'avatar', 'user_folder', 'about']
        labels = {
            'first_name': '',  # Установка пустой метки для first_name
            'last_name': '',   # Установка пустой метки для last_name
            'birth_date': 'Дата рождения',
            'avatar': 'Аватар',
            'user_folder': 'Папка пользователя',
            'about': 'О себе'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'user_folder': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'О себе'}),
        }



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []
        # Дополнительно можно настроить виджеты, если это необходимо


class ProfileEditForm(forms.ModelForm):
    labels = {
        'birth_date': 'Дата рождения',
        'avatar': 'Аватар',
        'user_folder': 'Папка пользователя',
        'about': 'О себе'
    }
    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
        'birth_date': forms.DateInput(attrs={'class': 'form-control',
                                             'type': 'date'}),
        'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        'user_folder': forms.TextInput(attrs={'class': 'form-control'}),
        'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'О себе'}),
        # Добавьте другие настройки виджетов здесь
    }
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birth_date', 'avatar', 'user_folder', 'about']
        # Здесь также можно добавить настройки виджетов