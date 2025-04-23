from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from analisis_mercado.models import Habilidad

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    rol = forms.ChoiceField(choices=Usuario.ROL_CHOICES)
    habilidades = forms.ModelMultipleChoiceField(
        queryset=Habilidad.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol', 'habilidades')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.rol = self.cleaned_data['rol']
        if commit:
            user.save()
            user.habilidades.set(self.cleaned_data['habilidades'])
        return user

class PerfilForm(forms.ModelForm):
    habilidades = forms.ModelMultipleChoiceField(
        queryset=Habilidad.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'habilidades')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['habilidades'].initial = self.instance.habilidades.all() 