from django import forms
from django.contrib.auth.forms import AuthenticationForm

from core.forms.widgets import (
    CalciteInputWidget,
    CalcitePasswordWidget,
)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=CalciteInputWidget(
            attrs={
                "placeholder": "Username",
            }
        )
    )

    password = forms.CharField(
        widget=CalcitePasswordWidget(
            attrs={
                "placeholder": "Password",
            }
        )
    )
