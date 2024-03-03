from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import ExtendedUserCreationForm, CustomAuthForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm


def register(request):
    if request.method == 'POST':
        user_form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            profile, user = user_form.save()  # Создаем пользователя

            # Теперь обновляем поля профиля данными из profile_form
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()

            for group in user_form.cleaned_data['groups']:
                group.user_set.add(user)

            login(request, user)
            return redirect('index')
    else:
        user_form = ExtendedUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'authorization/register.html', {'user_form': user_form, 'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Или другой URL
            else:
                messages.error(request, 'Неправильное имя пользователя или пароль')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')
    else:
        form = CustomAuthForm()
    return render(request, 'authorization/login.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Важно, чтобы пользователь оставался в системе после смены пароля
            messages.success(request, 'Ваш пароль был успешно обновлен!')
            return redirect('index')  # Измените на соответствующее имя URL главной страницы
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'authorization/change_password.html', {
        'form': form
    })

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Добавьте сообщение об успешном обновлении или перенаправление
            return redirect('index')  # Или другой URL для перенаправления

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'authorization/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})