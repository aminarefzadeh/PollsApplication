from django import forms
from django.core.validators import MinLengthValidator, RegexValidator


class UserForm(forms.Form):
    username = forms.CharField(label='Enter your username:', max_length=100)
    first_name = forms.CharField(label='Enter your first name:', max_length=100)
    last_name = forms.CharField(label='Enter your last_name:', max_length=100)
    password = forms.CharField(
        label='Enter your password:',
        max_length=100,
        widget=forms.PasswordInput(),
        validators=[
            MinLengthValidator(limit_value=8, message='password should be at least 8 character'),
            RegexValidator(regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]*$",
                           message='password should contain at least one letter and one number')
        ]
    )

    email = forms.EmailField(label='Enter your email:')
