from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from authapp.models import Player, PlayerProfile
from datetime import datetime
import pytz
from django.conf import settings
import hashlib


class PlayerLoginForm(AuthenticationForm):

    class Meta:
        model = Player
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class PlayerRegisterForm(UserCreationForm):

    class Meta:
        model = Player
        fields = ('username', 'nickname', 'age', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_nickname(self):
        data = self.cleaned_data['nickname']
        if 'fuck' in data:
            raise forms.ValidationError('Restricted words in your nickname')
        return data

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.activation_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
        user.activation_key_expires = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()

        return user


class PlayerEditForm(UserChangeForm):

    class Meta:
        model = Player
        fields = ('username', 'nickname', 'age', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_nickname(self):
        data = self.cleaned_data['nickname']
        if 'fuck' in data:
            raise forms.ValidationError('Restricted words in your nickname')
        return data


class PlayerProfileEditForm(forms.ModelForm):

    class Meta:
        model = PlayerProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
