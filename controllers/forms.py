from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from controllers.models import *

import datetime

TIP_REL_CHOICES = (("","Follow"),("me nofollow","Me nofollow"),("nofollow","Nofollow"))


#wall user login
class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(UserLoginForm, self).clean()
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            self._errors['username'] = self.error_class(["Your username and/or password were incorrect."])
        elif not user.is_active:
            self._errors['username'] = self.error_class(["Account is not active"])

        self.cleaned_data['user'] = user

        return self.cleaned_data

class ProfileModelForm(forms.ModelForm):
    describe = forms.CharField(label="Descriere",widget=forms.Textarea)


class UserModelForm(forms.ModelForm):
    first_name = forms.CharField(label="Nume de familie",max_length=128)
    last_name = forms.CharField(label="Prenume",max_length=128)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label="Parola veche",max_length=100,widget=forms.PasswordInput())
    password1 = forms.CharField(label="Parola noua",max_length=100,widget=forms.PasswordInput())
    password2 = forms.CharField(label="Din nou parola noua",max_length=100,widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password2' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if(password1 == password2):
                return password2
        raise forms.ValidationError('Parole nu concid, te rog sa recompletezi')


class AddUserForm(forms.Form):
    username = forms.CharField(max_length=128)
    email  = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username mai exista in baza')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email mai exista in baza')


class SetPasswordForm(forms.Form):
    password1 = forms.CharField(label="Parola noua",max_length=100,widget=forms.PasswordInput())
    password2 = forms.CharField(label="Din nou parola noua",max_length=100,widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password2' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if(password1 == password2):
                return password2
        raise forms.ValidationError('Parole nu concid, te rog sa recompletezi')


class AddLinksForm(forms.Form):
    url = forms.URLField()
    value = forms.CharField(max_length=300)
    rel = forms.ChoiceField(required=False,choices = TIP_REL_CHOICES)  

    def clean_url(self):
        url = self.cleaned_data['url']
        try:
            Links.objects.get(url=url)
        except Links.DoesNotExist:
            return url
        raise forms.ValidationError('Url mai exista in baza')


class EditLinksModelForm(forms.ModelForm):
    url = forms.URLField()
    value = forms.CharField(max_length=300)
    rel = forms.ChoiceField(required=False,choices = TIP_REL_CHOICES)  


class AddMenuForm(forms.Form):
    menu  = forms.CharField(label="Meniu",max_length=50)
    url = forms.CharField(max_length=50)


class AddUnderMenuForm(forms.Form):
    undermenu  = forms.CharField(label="Submeniu",max_length=50)
    url = forms.CharField(max_length=50)


class AddMenuModelForm(forms.ModelForm):
    menu  = forms.CharField(label="Meniu",max_length=50)
    url = forms.CharField(max_length=50)


class AddUnderMenuModelForm(forms.ModelForm):
    undermenu  = forms.CharField(label="Submeniu",max_length=50)
    url = forms.CharField(max_length=50)

class AddPageForm(forms.Form):
    title = forms.CharField(label="Titlu",max_length = 200)
    body = forms.CharField(label="Continut",widget=forms.Textarea)

    class Media:
        js = ('/static/javascript/tiny_mce/tiny_mce.js', '/static/javascript/textareas.js')


class EditPageModelForm(forms.ModelForm):
    title = forms.CharField(label="Titlu",max_length = 200)
    body = forms.CharField(label="Continut",widget=forms.Textarea)

    class Media:
        js = ('/static/javascript/tiny_mce/tiny_mce.js', '/static/javascript/textareas.js')

class AddArticlesForm(forms.Form):
    title = forms.CharField(label="Titlu",max_length = 200)
    describe = forms.CharField(label="Descriere",max_length=500)
    body = forms.CharField(label="Continut",widget=forms.Textarea)
    data = forms.DateField()
    image = forms.ImageField(label="Imaginea articolului",widget=forms.FileInput)

    def clean_data(self):
        if 'data' in self.cleaned_data:
            data = self.cleaned_data['data']

            if data >= datetime.date.today():
                return data
            else:
                raise forms.ValidationError('Alege o data din viitor')

    class Media:
        js = ('/static/javascript/tiny_mce/tiny_mce.js', '/static/javascript/textareas.js')


class EditArticlesModelForm(forms.ModelForm):
    title = forms.CharField(label="Titlu",max_length = 200)
    describe = forms.CharField(label="Descriere",max_length=500)
    body = forms.CharField(label="Continut",widget=forms.Textarea)
    data = forms.DateField()

    class Media:
        js = ('/static/javascript/tiny_mce/tiny_mce.js', '/static/javascript/textareas.js')


class AddTagForm (forms.Form):
    name = forms.CharField( max_length=64 )

class FileForm(forms.Form):
    file  = forms.FileField(label="Adauga un fisier")

    def clean_file(self):
        if 'file' in self.cleaned_data:
            file = self.cleaned_data['file']
            if file._size > 10*1024*1024:
                raise forms.ValidationError("File file too large ( > 10mb )")
            return file

class AddEmailForm(forms.Form):
    email = forms.EmailField()

