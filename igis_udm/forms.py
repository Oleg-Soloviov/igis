from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w3-input w3-border',
                                                         'pattern': '[а-яА-Я]{0,100}',
                                                         'placeholder': 'иванов (только фамилия)'}),
                           label='Фамилия')
    polis = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'w3-input w3-border',
                                                              'maxlength': '16',
                                                              'pattern': '[0-9]{16}',
                                                              'placeholder': '0001 0002 0003 0004'}),
                                label='Номер мед полиса (12 цифр)')


class DateOfSignForm(forms.Form):
    date = forms.IntegerField(widget=forms.HiddenInput())
    obj = forms.IntegerField(widget=forms.HiddenInput())


class TimePersonForm(forms.Form):
    id = forms.IntegerField()


class SignInForm(forms.Form):
    specialist_id = forms.RegexField(regex=r'^[0-9]+$')
    date = forms.RegexField(regex=r'^[0-9]{6,8}$')
    time = forms.RegexField(regex=r'^[0-9]{2}:[0-9]{2}$')


class SignOutForm(forms.Form):
    specialist_id = forms.RegexField(regex=r'^[0-9]+$')
    date = forms.RegexField(regex=r'^[0-9]{6,8}$')
    time = forms.RegexField(regex=r'^[0-9]{2}:[0-9]{2}$')