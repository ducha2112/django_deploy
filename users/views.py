from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, ProfileImageForm, UserUpdateForm, ProfileGenderForm
from  django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username =form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Пользователь {username} был успешно создан, электронная почта {email}')
            return redirect('home')
    else:
        form = UserRegisterForm()
    # form = UserCreationForm()
    return render(
        request,
        'users/registration.html',
        {
            'title':'Страница регистрации',
            'form':form
        }
    )

# проверка авторизации
@login_required
def profile(request):
    if request.method == 'POST':
        profileForm = ProfileImageForm(request.POST,request.FILES,  instance=request.user.profile)
        updateUserForm = UserUpdateForm(request.POST,  instance=request.user)
        genderUser = ProfileGenderForm(request.POST, instance=request.user.profile)

        if profileForm.is_valid() and updateUserForm.is_valid() and genderUser.is_valid():
            updateUserForm.save()
            profileForm.save()
            genderUser.save()
            messages.success(request, f'Ваш аккаунт был успешно обновлен!')
            return redirect('profile')
    else:
        profileForm = ProfileImageForm(instance=request.user.profile)
        updateUserForm = UserUpdateForm(instance=request.user)
        genderUser = ProfileGenderForm( instance=request.user.profile)

    data = {
        'profileForm': profileForm,
        'updateUserForm': updateUserForm,
        'genderUser': genderUser
    }
    return render(
        request,
        'users/profile.html', data)


