from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Profile

@receiver(post_save, sender=Profile)
def add_user_to_students_group(sender, instance, created, **kwargs):
    if created:
        try:
            group1 = Group.objects.get(name='estudiantes')
        except Group.DoesNotExist:
            group1 = Group.objects.create(name='estudiantes')
            group2 = Group.objects.create(name='profesores')
            group3 = Group.objects.create(name='preceptores')
            group4 = Group.objects.create(name='administrativos')
        
        instance.user.groups.add(group1)



#DOCUMENTACION 
'''
Este código utiliza una señal para agregar automáticamente a los usuarios que tienen un perfil (modelo `Profile`) al grupo de "estudiantes" (`estudiantes`) cuando se crea su perfil.

### Detalles clave:

1. **Señal `post_save` y el decorador `@receiver`**:
   - `@receiver(post_save, sender=Profile)` indica que esta función (`add_user_to_students_group`) se ejecutará después de que se guarde una instancia del modelo `Profile`. Específicamente, cuando se cree un nuevo perfil, esta señal será activada.
   - `sender=Profile` significa que esta señal responde a eventos relacionados con el modelo `Profile`.

2. **Función `add_user_to_students_group`**:
   Esta función tiene como objetivo añadir el usuario asociado al perfil recién creado al grupo de "estudiantes".

   - **`instance`**: Es la instancia del perfil que se acaba de crear.
   - **`created`**: Es un booleano que indica si el perfil fue creado o solo actualizado. La función solo actúa si el perfil fue recién creado (`if created:`).
   - **`Group.objects.get(name='estudiantes')`**: Intenta obtener el grupo con el nombre "estudiantes".
   - **`Group.DoesNotExist`**: Si el grupo "estudiantes" no existe, lo crea mediante `Group.objects.create(name='estudiantes')`.
   - **`instance.user.groups.add(students)`**: Añade el usuario asociado al perfil (a través de `instance.user`) al grupo de "estudiantes".

### Flujo de trabajo:
1. Cuando se crea un nuevo perfil (`Profile`), se activa la señal `post_save` para el modelo `Profile`.
2. La función `add_user_to_students_group` se ejecuta.
3. La función verifica si existe un grupo llamado "estudiantes". Si no existe, lo crea.
4. Luego, el usuario asociado al perfil recién creado se añade a este grupo.

### ¿Cuándo es útil este enfoque?
Este tipo de lógica es útil cuando:
- Quieres asignar permisos o roles a los usuarios automáticamente basándote en ciertos criterios, como si tienen un perfil.
- Tienes diferentes grupos de usuarios (por ejemplo, estudiantes, profesores) y quieres categorizarlos automáticamente.

### ¿Qué podrías agregar o modificar?
- **Manejo de errores**: Si quisieras una capa extra de seguridad, podrías agregar un bloque `try-except` para manejar posibles fallos inesperados, como problemas de conexión a la base de datos o problemas al agregar el usuario al grupo.
- **Asignación a múltiples grupos**: Si en el futuro necesitas asignar al usuario a varios grupos automáticamente, podrías adaptar esta función para manejar más de un grupo.
  
¿Te gustaría añadir alguna funcionalidad extra o tienes alguna duda sobre el funcionamiento?
'''