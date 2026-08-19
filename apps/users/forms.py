from django import forms

from .models import User


class SettingsForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "avatar",
            "notifications_enabled",
        ]

        widgets = {
            "avatar": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                }
            ),

            "notifications_enabled": forms.CheckboxInput(
                attrs={
                    "class": "settings-toggle-input",
                }
            ),
        }