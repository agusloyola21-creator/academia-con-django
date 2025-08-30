from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# PERFIL DE USUARIO
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Usuario')
    image = models.ImageField(default='usuario_defecto.jpg', upload_to='users/', verbose_name='Imagen de perfil')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    location = models.CharField(max_length=150, null=True, blank=True, verbose_name='Localidad')
    telephone = models.CharField(max_length=150, null=True, blank=True, verbose_name='Teléfono')
    created_by_admin = models.BooleanField(default=True, blank=True, null=True, verbose_name='Creado por Admin')
    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        ordering = ['-id']
    
    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile,sender=User)



#Expicacion de las señales
'''
En Django, las señales son una forma de permitir que ciertos emisores (como modelos o vistas) envíen notificaciones cuando ocurre un evento específico, como la creación, actualización o eliminación de objetos en la base de datos. 
Esto facilita que otras partes del sistema reaccionen automáticamente a esos eventos sin necesidad de modificar el código del emisor original.

Concepto básico:
Las señales permiten "escuchar" eventos que ocurren en tu aplicación y ejecutar funciones en respuesta a esos eventos. Hay dos componentes clave en el uso de señales:

El emisor: Es la entidad que genera el evento. En este caso, el emisor es el modelo User.
El receptor: Es la función que se ejecuta cuando el emisor "envía" una señal. En este caso, las funciones create_user_profile y save_user_profile son los receptores.
Proceso de uso de señales:
Crear una función receptora (handler): Esta función define lo que se debe hacer cuando ocurre un evento. En tu código, tienes dos funciones que actúan como receptores:

python
Copiar código
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
Esta función:

sender: Es el modelo que envía la señal (en este caso, User).
instance: Es la instancia del modelo que activó la señal (el objeto del usuario que se acaba de crear).
created: Es un booleano que indica si la instancia fue creada (si es True, significa que el objeto acaba de ser creado).
kwargs: Son parámetros adicionales (se suelen pasar vacíos en este caso).
Si un nuevo usuario fue creado (created == True), la función crea un perfil asociado para ese usuario.

Conectar la señal: Django necesita saber qué función debe ejecutar cuando se emite la señal. Esto se hace con la función connect(), que vincula el evento (en este caso, la creación o el guardado de un User) con el receptor (la función que hemos definido):

python
Copiar código
post_save.connect(create_user_profile, sender=User)
Esto le dice a Django que después de que un usuario sea guardado (después del evento post_save), debe ejecutar la función create_user_profile. Aquí, sender=User indica que estamos interesados en el evento que ocurre sobre el modelo User.

Señales en tu código:
create_user_profile:

Se conecta al evento post_save del modelo User.
Cuando un nuevo usuario es creado, esta función crea automáticamente un perfil para ese usuario.
python
Copiar código
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
save_user_profile:

También está conectada al evento post_save del modelo User.
Esta función asegura que cada vez que se guarde un usuario, su perfil asociado se guarde también.
python
Copiar código
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
post_save.connect(save_user_profile, sender=User)
Flujo de trabajo:
Se crea un nuevo usuario (User).
Después de que el usuario se guarda en la base de datos, se activa el evento post_save.
Django envía la señal post_save para que las funciones conectadas a ese evento se ejecuten.
La función create_user_profile se ejecuta y crea un perfil para el nuevo usuario.
Si el usuario se actualiza, save_user_profile se asegura de que los cambios en el perfil se guarden también.
¿Por qué usar señales?
Automatización: Las señales son útiles cuando quieres que ciertas tareas ocurran automáticamente sin necesidad de incluirlas en el flujo principal de tu código.
Desacoplamiento: Permiten que diferentes partes del sistema estén menos acopladas. Por ejemplo, el modelo User no necesita saber cómo crear o guardar un Profile, pero gracias a las señales, se puede lograr esa interacción fácilmente.
Si necesitas más detalles o ejemplos sobre cómo trabajar con señales en Django, estaré encantado de ayudarte.


'''