from Accounts.models import Account, Role
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SchoolInfo
class NewSetupUser(UserCreationForm):
    email = forms.EmailField(required=True, label="Почта")
    class Meta:
        model = Account
        fields = (
        "username", "email", "second_name", "first_name", "middle_name", "password1", "password2")
        labels = {
            "username": "Имя пользователя",
            "second_name": "Фамилия",
            "first_name": "Имя",
            "middle_name": "Отчество",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }
        widgets = {
            'username': forms.TextInput(),
        }

    def save(self, commit=True):
        user = super(NewSetupUser, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        user.role.add(Role.objects.get(label="admin"))
        user.save()
        return user

class SchoolInfoForm(forms.ModelForm):
    class Meta:
        model = SchoolInfo
        # Описываем поля, которые будем заполнять в форме
        fields = ('name','short_name','number','token','mos_ru_auth')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Полное название школы'}),
            'short_name': forms.TextInput(attrs={'placeholder': 'Краткое название школы в МЭШ(если используется)'}),
            'number': forms.TextInput(attrs={'placeholder': 'Номер школы'}),
            'token': forms.TextInput(attrs={'placeholder':"Токен школы"})
        }