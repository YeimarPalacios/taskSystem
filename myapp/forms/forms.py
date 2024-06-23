# En usuarios/forms.py

from django import forms
from myapp.models import Usuario

class LoginForm(forms.Form):
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico', 'required': True}),
        error_messages={'required': 'El correo electrónico es obligatorio', 'invalid': 'Ingrese un correo válido'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'required': True}),
        error_messages={'required': 'La contraseña es obligatoria'}
    )

class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'required': True}),
        error_messages={'required': 'La contraseña es obligatoria'}
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña', 'required': True}),
        error_messages={'required': 'La confirmación de la contraseña es obligatoria'}
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'required': True}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido', 'required': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico', 'required': True}),
        }
        error_messages = {
            'nombre': {'required': 'El nombre es obligatorio'},
            'apellido': {'required': 'El apellido es obligatorio'},
            'correo': {'required': 'El correo electrónico es obligatorio', 'invalid': 'Ingrese un correo válido'},
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
