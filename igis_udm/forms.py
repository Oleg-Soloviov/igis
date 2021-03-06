from django import forms
from django.core.mail import send_mail


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


class ContactForm(forms.Form):
    email = forms.EmailField(required=False)
    subject = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea())

    def send_email(self):
        subject = 'from IGIS_UDM: {}'.format(self.cleaned_data['subject'])
        if self.cleaned_data['email']:
            message = 'from {}\n\n {}'.format(self.cleaned_data['email'], self.cleaned_data['message'])
        else:
            message = self.cleaned_data['message']
        send_mail(
            subject,
            message,
             "<postmaster@sandbox075b55521f59465c82d4d87856d6f43c.mailgun.org>",
            ["osoloviov@list.ru"])
