from django import  forms
from django.contrib.auth.models import User
from .models import Profile
from blog.models import Message
# from django.contrib.auth.forms import UserCreationForm

# class UserRegisterForm(UserCreationForm):
class UserRegisterForm(forms.Form):
    username = forms.CharField(
        label='Введите логин',
        required=True,
        help_text='Нельзя вводить символы @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})

    )
    email = forms.EmailField(
        label='Введите Email',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'})
    )
    # some = forms.ModelChoiceField(queryset=User.objects.all())
    password1 = forms.CharField(
        label='Введите пароль',
        required=True,
        help_text='Пароль не должен быть простым',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Введите пароль'})

    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = [ 'username', 'email','password1', 'password2' ]
 # 'password1', 'password2','some'

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label='Введите логин',
        required=True,
        help_text='Нельзя вводить символы @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})

    )
    email = forms.EmailField(
        label='Введите Email',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'})
    )

    class Meta:
        model = User
        fields = [ 'username', 'email' ]


class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label='Загрузить фото',
        required=False,
        widget=forms.FileInput

    )
    class Meta:
        model = Profile
        fields = ['img']

class ProfileGenderForm(forms.ModelForm):
    CHOISES = (('male', 'Мужской пол'), ('femail', 'Женский пол'))
    gender = forms.ChoiceField(
        choices=CHOISES,
        label='Выберите пол',
        required=False,
        widget=forms.Select( attrs={'class': 'form-control'}))
    approv = forms.BooleanField(label='',
        help_text='Соглашение про отправку уведомлений на почту')

    class Meta:
        model = Profile
        fields = ['gender','approv']

class MessageFromUser(forms.ModelForm):
    theme = forms.CharField(
        label='Тема сообщения',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите тему сообщения'})

    )
    email = forms.EmailField(
        label='Ваш Email',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'})
    )
    text = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст сообщения здесь'}), required=True)

    class Meta:
        model = Message
        fields = ['theme','email','text']