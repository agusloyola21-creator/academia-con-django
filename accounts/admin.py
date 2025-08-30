from django.contrib import admin
from .models import Profile

# PROFILE DETALLADO
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'location', 'telephone', 'user_group')
    search_fields = ('location', 'user__username', 'user__groups__name')
    list_filter = ('user__groups', 'location')

    def user_group(self, obj):
        return " - ".join([t.name for t in obj.user.groups.all().order_by('name')])
    
    user_group.short_description='Grupo'

admin.site.register(Profile, ProfileAdmin)


#DOCUMENTACION
'''
Este código personaliza la administración del modelo `Profile` en el panel de administración de Django mediante la clase `ProfileAdmin`. A continuación te explico los detalles:

### Explicación:

1. **`ProfileAdmin`**:
   Esta clase personaliza cómo se muestra y maneja el modelo `Profile` en el panel de administración de Django.

   - **`list_display`**:
     Especifica las columnas que se mostrarán en la lista de perfiles dentro del panel de administración. En este caso, se mostrarán los campos:
     - `user`: El nombre de usuario asociado al perfil.
     - `address`: La dirección del perfil.
     - `location`: La localidad del perfil.
     - `telephone`: El teléfono del perfil.
     - `user_group`: Un método personalizado que muestra los grupos a los que pertenece el usuario.

   - **`search_fields`**:
     Especifica los campos que se pueden buscar dentro del panel de administración. Se pueden realizar búsquedas por:
     - `location`: Localidad del perfil.
     - `user__username`: Nombre de usuario del perfil (a través de la relación con el modelo `User`).
     - `user__groups__name`: Nombre del grupo al que pertenece el usuario (a través de la relación con el modelo `User` y `Group`).

   - **`list_filter`**:
     Permite filtrar los perfiles en el panel de administración por:
     - `user__groups`: Los grupos a los que pertenece el usuario.
     - `location`: La localidad del perfil.

2. **Método `user_group`**:
   Esta función personalizada devuelve una cadena que representa todos los grupos a los que pertenece el usuario asociado al perfil.

   - **`obj.user.groups.all()`**: Obtiene todos los grupos asociados al usuario.
   - **`order_by('name')`**: Ordena los grupos por nombre.
   - **`" - ".join([...])`**: Combina los nombres de los grupos en una cadena separada por " - ".
   - **`user_group.short_description = 'Grupo'`**: Define el nombre que aparecerá como encabezado de la columna en el panel de administración.

3. **`admin.site.register(Profile)`**:
   Registra el modelo `Profile` junto con la clase `ProfileAdmin` para que sea administrable desde el panel de Django. Esto permite que los usuarios del panel de administración vean y gestionen los perfiles con la personalización establecida.

### Ejemplo de lo que sucederá en el panel de administración:
- En la vista de lista de perfiles, verás los campos del usuario, su dirección, localidad, teléfono, y los grupos a los que pertenece (mostrados en la columna `Grupo`).
- Se podrá buscar perfiles por localidad, nombre de usuario o nombre de grupo.
- Los administradores podrán filtrar los perfiles por el grupo al que pertenece el usuario o la localidad.
  
### ¿Qué más podrías añadir?
- **Acciones personalizadas**: Podrías agregar acciones personalizadas para los administradores, como enviar correos electrónicos a los usuarios seleccionados o reasignarlos a diferentes grupos.
- **Mejorar la visualización de los grupos**: Si un usuario pertenece a muchos grupos, podrías formatear la salida del método `user_group` para mejorar la legibilidad.

¿Te gustaría añadir alguna funcionalidad adicional o mejorar esta configuración de administración?

La expresión:

```python
t.name for t in obj.user.groups.all().order_by('name')
```

es un generador que recorre los grupos asociados a un usuario y obtiene el nombre de cada grupo (`t.name`), donde `t` es una instancia del modelo `Group` que representa cada grupo al que pertenece el usuario.

### Explicación detallada:

1. **`obj.user`**:
   - `obj` es la instancia del modelo `Profile`. Al hacer `obj.user`, accedemos al usuario asociado al perfil mediante la relación `OneToOneField` con el modelo `User`.

2. **`obj.user.groups`**:
   - Django tiene una relación `ManyToMany` predefinida entre `User` y `Group` a través del atributo `groups`. Esto significa que un usuario puede pertenecer a varios grupos, y aquí accedemos a todos los grupos a los que pertenece el usuario.

3. **`obj.user.groups.all()`**:
   - Recupera todos los grupos a los que pertenece el usuario como un conjunto de objetos `Group`.

4. **`order_by('name')`**:
   - Ordena los grupos alfabéticamente por el campo `name` de cada grupo.

5. **`t.name`**:
   - `t` representa cada grupo en la lista de grupos a los que pertenece el usuario. `t.name` devuelve el nombre del grupo.

En resumen, este generador recorre los grupos a los que pertenece el usuario, obtiene el nombre de cada grupo y los ordena alfabéticamente.

### Usualmente en un contexto de unión:
Para que la lista de nombres de grupos sea fácil de leer, se suele utilizar `join()` para unirlos en una cadena. Por ejemplo, en el método `user_group`:

```python
def user_group(self, obj):
    return " - ".join([t.name for t in obj.user.groups.all().order_by('name')])
```

Esta expresión toma la lista de nombres de grupos (`t.name for t in ...`) y los une en una cadena separada por " - ".

### Ejemplo:

Supongamos que un usuario pertenece a los grupos "estudiantes" y "administradores". Entonces, el método devolvería:

```
"administradores - estudiantes"
```

¿Te gustaría alguna explicación adicional o ajuste relacionado con esta expresión?

'''