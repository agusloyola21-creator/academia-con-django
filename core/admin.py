from django.contrib import admin
from .models import Course, Registration,Attendance,Mark

# CURSOS
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'class_quantity')
    list_filter = ('teacher',)

admin.site.register(Course,CourseAdmin) 
# DOCUMENTACION 
'''
Este código registra el modelo `Course` en el panel de administración de Django y personaliza su presentación mediante la clase `CourseAdmin`. Aquí te explico los elementos clave:

### Explicación del código:

1. **`CourseAdmin`**:
   - **`list_display = ('name', 'teacher', 'class_quantity')`**:
     - Este atributo define qué campos se mostrarán en la lista de cursos en el panel de administración.
     - En este caso, se mostrarán el nombre del curso, el profesor asignado y la cantidad de clases.

   - **`list_filter = ('teacher',)`**:
     - Este atributo agrega un filtro en la barra lateral para que los administradores puedan filtrar los cursos por profesor.
     - Esto es útil si hay muchos cursos y deseas ver solo aquellos que están asociados a un profesor específico.

2. **`admin.site.register(Course, CourseAdmin)`**:
   - Esta línea registra el modelo `Course` en el panel de administración utilizando la configuración personalizada de `CourseAdmin`. Ahora, cuando accedas a la sección de "Cursos" en el panel de administración, verás la lista de cursos con las columnas `name`, `teacher` y `class_quantity`, y tendrás la opción de filtrar por profesor.

### Posibles mejoras:

1. **Añadir búsqueda**:
   Si quieres facilitar la búsqueda de cursos por nombre o profesor, puedes añadir el atributo `search_fields`:

   ```python
   search_fields = ('name', 'teacher__username')
   ```

   Esto permite buscar cursos por el nombre del curso o por el nombre del profesor.

2. **Añadir ordenación**:
   Puedes añadir la opción de ordenar los cursos de manera predeterminada por cualquier campo, por ejemplo, por el nombre del curso:

   ```python
   ordering = ('name',)
   ```

3. **Mostrar más información sobre el profesor**:
   Si deseas mostrar más información sobre el profesor, podrías extender el método `list_display` para incluir detalles adicionales, como el nombre completo del profesor:

   ```python
   def teacher_name(self, obj):
       return obj.teacher.get_full_name()
   
   teacher_name.short_description = 'Nombre del Profesor'
   ```

4. **Paginación en el panel de administración**:
   Si tienes muchos cursos, podrías configurar la paginación para mostrar un número específico de cursos por página:

   ```python
   list_per_page = 20
   ```

Con estas configuraciones, la administración de cursos sería más eficiente y fácil de navegar.

¿Te gustaría aplicar alguna de estas mejoras o añadir algo más a la configuración de administración de los cursos?

'''

# INSCRIPCIONES
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('course','student', 'enabled')
    list_filter = ('course','student', 'enabled')

admin.site.register(Registration,RegistrationAdmin)
# DOCUMENTACION
'''

Este código registra el modelo `Registration` en el panel de administración de Django con una configuración personalizada a través de la clase `RegistrationAdmin`. Aquí está la descripción:

1. **`list_display = ('course', 'student')`**:
   - Esto especifica que en la lista de inscripciones en el panel de administración se mostrarán las columnas correspondientes al curso y al estudiante.

2. **`list_filter = ('course', 'student')`**:
   - Esto agrega opciones de filtrado en la barra lateral para que los administradores puedan filtrar las inscripciones por curso o por estudiante.

3. **`admin.site.register(Registration, RegistrationAdmin)`**:
   - Registra el modelo `Registration` en el panel de administración utilizando la configuración definida en `RegistrationAdmin`.

En resumen, este código facilita la gestión de inscripciones al mostrar la información relevante y permite filtrar por curso y estudiante en el panel de administración.
'''

# ASiSTENCIA
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'date', 'present')
    list_filter = ('course', 'student', 'date', 'present')
admin.site.register(Attendance,AttendanceAdmin)
# DOCUMENTACION
'''
Este código registra el modelo `Attendance` en el panel de administración de Django utilizando la clase personalizada `AttendanceAdmin`. A continuación te explico brevemente los elementos clave:

### Explicación del código:

1. **`list_display = ('course', 'student', 'date', 'present')`**:
   - Define las columnas que se mostrarán en la lista de asistencias en el panel de administración. En este caso, se mostrarán el curso, el estudiante, la fecha de la asistencia y si el estudiante estuvo presente o no.

2. **`list_filter = ('course', 'student', 'date', 'present')`**:
   - Añade opciones de filtrado en la barra lateral del panel de administración para que los administradores puedan filtrar las asistencias por curso, estudiante, fecha y estado de presencia (presente o ausente).

3. **`admin.site.register(Attendance, AttendanceAdmin)`**:
   - Registra el modelo `Attendance` en el panel de administración utilizando la configuración definida en `AttendanceAdmin`.

### Resumen:
Este código personaliza la visualización de los registros de asistencia en el panel de administración, facilitando la búsqueda, el filtrado y la gestión de asistencias según el curso, estudiante, fecha y presencia.
'''

#NOTAS
class MarkAdmin(admin.ModelAdmin):
    list_display = ('course','student','mark_1','mark_2','mark_3','average')
    list_filter = ('course',)
admin.site.register(Mark,MarkAdmin)