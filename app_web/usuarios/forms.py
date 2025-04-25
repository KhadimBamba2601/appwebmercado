from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from analisis_mercado.models import Habilidad

class RegistroUsuarioForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(required=False)
    rol = forms.ChoiceField(choices=Usuario.Rol.choices)
    telefono = forms.CharField(max_length=15, required=False)

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'fecha_nacimiento', 'rol', 'telefono', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.rol = self.cleaned_data['rol']
        if commit:
            user.save()
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