from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class RegistrationForm(UserCreationForm):
    name = forms.CharField(label="Nome", max_length=255)
    email = forms.EmailField(label="Email institucional")
    institution = forms.CharField(label="Instituição", max_length=255)
    user_type = forms.ChoiceField(label="Tipo de usuário", choices=UserProfile.USER_TYPES)

    class Meta:
        model = User
        fields = ("name", "email", "institution", "user_type", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["user_type"].widget.attrs["class"] = "form-select"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email

    def save(self, commit=True):
        name = self.cleaned_data["name"].strip()
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        parts = name.split(maxsplit=1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        if commit:
            user.save()
            profile = user.profile
            profile.institution = self.cleaned_data["institution"].strip()
            profile.user_type = self.cleaned_data["user_type"]
            profile.save(update_fields=["institution", "user_type"])
        return user
