from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile
from .models import  Course
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import  Layout, Field, Submit

class LoginForm(AuthenticationForm):
    """
    Clase LoginForm que hereda de AuthenticationForm de Django.
    
    Se utiliza para manejar el formulario de autenticación (login) de usuarios.
    Actualmente no modifica ninguna funcionalidad de la clase base, pero puede
    ser extendida o personalizada en el futuro si se requiere agregar nuevos campos
    o lógica de validación adicional.
    """
    pass

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    first_name= forms.CharField(label='Nombre')
    last_name= forms.CharField(label='Apellido')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email_field = self.cleaned_data['email']
        if User.objects.filter(email = email_field).exists():
            raise forms.ValidationError('Este correo electronico ya está registrado')
        return email_field
        #############################
        ### AGREGAR DOCUMENTACION ###
        #############################

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'address', 'location', 'telephone']

class CourseForms(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='profesores'), label='Profesor')
    status = forms.ChoiceField(choices=Course.STATUS_CHOISES, initial='I', label = 'Estado')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), label='Descripción')
    class Meta:
        model = Course
        fields = ['name','description','teacher','class_quantity','status']

    helper = FormHelper()
    helper.layout = Layout(
        Field('name'),
        Field('description'),
        Field('teacher'),
        Field('class_quantity'),
        Field('status'),
        Submit('submit', 'Submit')
    )

# FORMULARIO DE NUEVO USUARIO
class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']