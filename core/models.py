from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# CURSOS
class Course(models.Model):

   STATUS_CHOISES = (
      ('I', 'En etapa de inscripción'),
      ('P', 'En progreso'),
      ('F', 'Finalizado'),

   )


   name= models.CharField(max_length=90, verbose_name='Nombre')
   description = models.TextField(blank=True, null=True, verbose_name='Descripción')
   teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'profesores'}, verbose_name='Profesor')
   class_quantity = models.PositiveIntegerField(default=0, verbose_name='Cantidad de clases')
   status = models.CharField(max_length=1, choices=STATUS_CHOISES, default='I', verbose_name = 'Estado')

   def __str__(self):
      return self.name
   
   class Meta:
      verbose_name = 'Curso'
      verbose_name_plural = 'Cursos'
# DOCUMENTACION CURSOS
'''
Este código define un modelo de Django llamado `Course`, que representa los cursos en tu sistema. Aquí está el desglose de cada parte:

### Explicación del modelo `Course`:

1. **Campos**:
   - **`name`**: Un campo de texto que almacena el nombre del curso. Tiene una longitud máxima de 90 caracteres y un título descriptivo ('Nombre') para el panel de administración.
   - **`description`**: Un campo de texto más largo (`TextField`) que puede contener una descripción del curso. Se permite que esté vacío (`blank=True`) y también puede ser `null` en la base de datos (`null=True`).
   - **`teacher`**: Es una relación de tipo `ForeignKey` con el modelo `User`, que permite asignar un profesor al curso. 
     - **`on_delete=models.CASCADE`**: Si se elimina el profesor, el curso asociado también será eliminado.
     - **`limit_choices_to={'groups__name': 'profesores'}`**: Esto limita las opciones en el panel de administración a solo los usuarios que pertenecen al grupo de "profesores". Es útil para asegurar que solo los profesores puedan ser asignados como maestros de los cursos.
   - **`class_quantity`**: Un campo que almacena el número total de clases dentro de un curso como un número entero positivo. Tiene un valor por defecto de `0`.

2. **Métodos**:
   - **`__str__(self)`**: Este método devuelve el nombre del curso cuando se referencia una instancia del modelo. Esto es útil cuando el curso es representado en el panel de administración o en otros contextos donde el curso necesita ser identificado.

3. **Meta opciones**:
   - **`verbose_name = 'Curso'`**: Define cómo se mostrará el nombre del modelo en singular en el panel de administración.
   - **`verbose_name_plural = 'Cursos'`**: Define el nombre plural del modelo en el panel de administración.

### Ejemplo de uso en el panel de administración:
En el panel de administración, cuando crees un nuevo curso, el campo `teacher` solo mostrará a los usuarios que están en el grupo "profesores", facilitando la asignación correcta.

### Posibles mejoras:
- **Validación adicional**: Puedes agregar validaciones adicionales, como asegurarte de que el número de clases (`class_quantity`) no sea negativo, aunque ya se garantiza que sea positivo al usar `PositiveIntegerField`.
  
  ```python
  from django.core.exceptions import ValidationError
  
  def clean(self):
      if self.class_quantity < 1:
          raise ValidationError('El curso debe tener al menos una clase.')
  ```

- **Funciones relacionadas con los estudiantes**: Si los cursos necesitan estar relacionados con estudiantes, podrías agregar un `ManyToManyField` para conectar a los usuarios (estudiantes) con los cursos.

```python
students = models.ManyToManyField(User, related_name='courses', limit_choices_to={'groups__name': 'estudiantes'}, verbose_name='Estudiantes')
```

Esto permitiría asignar estudiantes a cada curso.

¿Te gustaría expandir alguna funcionalidad o agregar más relaciones en este modelo?
'''

# INSCRIPCIONES
class  Registration(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
   student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students_registration', limit_choices_to={'groups__name':'estudiantes'}, verbose_name='Estudiante')
   enabled = models.BooleanField(default=True, verbose_name='Alumno Regular')

   def __str__(self):
      return f'{self.student.username} - {self.course.name}' 

   class Meta:
      verbose_name = 'Inscripción'
      verbose_name_plural = 'Inscripciones'
# DOCUMENTACION INSCRIPCIONES
'''
Este código define el modelo `Registration` en Django, el cual representa una inscripción de un estudiante en un curso. Aquí te explico los elementos clave de este modelo:

### Explicación del modelo `Registration`:

1. **Campos**:
   - **`course`**:
     - Es una relación de tipo `ForeignKey` con el modelo `Course`, lo que significa que una inscripción está asociada a un curso específico.
     - **`on_delete=models.CASCADE`**: Si se elimina un curso, todas las inscripciones relacionadas también se eliminarán.
     - **`verbose_name='Curso'`**: Proporciona un nombre más descriptivo para el campo en el panel de administración.
   
   - **`student`**:
     - Es una relación de tipo `ForeignKey` con el modelo `User`, representando al estudiante que se inscribe en el curso.
     - **`related_name='students_registration'`**: Define un nombre personalizado para acceder a las inscripciones desde el usuario. En lugar de acceder a las inscripciones de un usuario con `user.registration_set.all()`, podrás hacerlo con `user.students_registration.all()`.
     - **`limit_choices_to={'groups__name':'estudiantes'}`**: Limita las opciones en el panel de administración para que solo se puedan seleccionar usuarios que pertenezcan al grupo de "estudiantes".
     - **`verbose_name='Estudiante'`**: Un nombre más amigable para este campo en el panel de administración.

   - **`enabled`**:
     - Es un campo de tipo BooleanField, lo que significa que puede almacenar valores True o False.
     - **`default=True`**: El valor predeterminado es True, lo que implica que por defecto todos los estudiantes serán considerados alumnos regulares cuando se cree una nueva inscripción.
     - **`verbose_name='Alumno Regular'`**: Este es el nombre descriptivo que se mostrará en el panel de administración para este campo.

2. **Método `__str__(self)`**:
   - Este método convierte el objeto `Registration` en una cadena que será mostrada en el panel de administración y otros contextos. En este caso, la cadena incluye el nombre de usuario del estudiante y el nombre del curso, lo que facilita la identificación de la inscripción.

   Ejemplo de la representación en cadena:
   ```
   juan.perez - Matemáticas Avanzadas
   ```

3. **Meta opciones**:
   - **`verbose_name = 'Estudiante'`**: Define cómo se mostrará el nombre del modelo en singular en el panel de administración (para inscripciones individuales).
   - **`verbose_name_plural = 'Estudiantes'`**: Define el nombre plural del modelo en el panel de administración.

### Posibles mejoras:

1. **Evitar inscripciones duplicadas**:
   Puedes añadir una restricción única para evitar que un estudiante se inscriba más de una vez en el mismo curso:

   ```python
   class Meta:
       unique_together = ('course', 'student')
       verbose_name = 'Estudiante'
       verbose_name_plural = 'Estudiantes'
   ```

   Esto asegura que no pueda haber inscripciones duplicadas de un mismo estudiante en el mismo curso.

2. **Validación personalizada**:
   Si quieres realizar validaciones adicionales, puedes sobrescribir el método `clean()` para verificar reglas personalizadas. Por ejemplo, verificar si el curso está lleno o si el estudiante cumple con ciertos requisitos.

   ```python
   from django.core.exceptions import ValidationError

   def clean(self):
       # Ejemplo: Verificar si el curso tiene cupos disponibles
       if self.course.class_quantity < Registration.objects.filter(course=self.course).count():
           raise ValidationError('Este curso ya está lleno.')
   ```

3. **Añadir fecha de inscripción**:
   Podrías añadir un campo `DateTimeField` para registrar cuándo se realizó la inscripción:

   ```python
   created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de inscripción')
   ```

Esto sería útil para ordenar inscripciones o para mostrar cuándo un estudiante se inscribió.

### Ejemplo en el panel de administración:

Puedes registrar este modelo en el panel de administración para manejar las inscripciones desde la interfaz administrativa:

```python
from django.contrib import admin
from .models import Registration

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')
    list_filter = ('course',)
    search_fields = ('student__username', 'course__name')

admin.site.register(Registration, RegistrationAdmin)
```

En este caso, se mostrarían las inscripciones con los campos `student` y `course`, permitiendo filtrar por curso y buscar por nombre de estudiante o curso.

### Resumen:

Este modelo `Registration` te permite gestionar inscripciones de estudiantes en cursos, asegurando que solo los usuarios del grupo "estudiantes" puedan ser seleccionados. Puedes mejorar la funcionalidad añadiendo validaciones, restricciones para evitar duplicados y más información, como la fecha de inscripción.

¿Te gustaría añadir alguna de estas mejoras o ajustes?
'''

# ASISTENCIAS
class Attendance(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
   student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances', limit_choices_to={'groups__name':'estudiantes'}, verbose_name='Estudiante')
   date = models.DateTimeField(null=True, blank=True, verbose_name='Fechaa')
   present = models.BooleanField(default=False, blank=True, null=True, verbose_name='Presente')
   

   def __str__(self):
      return f'Asistencia {self.id}'

   ##########################################
   ##### Lógica para generar el enabled #####
   ##########################################
   # total-clases => class_quantity del modelo Course
   # total-inasistencias => attendance => present = false
   # Porcentaje de inacistencias = (total-inasistencias / total-clases)* 100 ----------> > 20 (>20%)=> alumno es irregular => enabled = False
   
   def update_registration_enabled_status(self):
      course_instance = Course.objects.get(id = self.course.id)
      total_classes = course_instance.class_quantity
      total_absences = Attendance.objects.filter(student=self.student, course=self.course, present=False).count()
      absences_percent = (total_absences / total_classes) * 100

      registration = Registration.objects.get(course = self.course, student = self.student)

      if absences_percent > 20:
         registration.enabled = False
      else:
         registration.enabled = True

      registration.save()

   class Meta:
      verbose_name = 'Asistencia'
      verbose_name_plural = 'Asistencias'
# DOCUMENTACION ASISTENCIA
'''
Aquí tienes una documentación detallada y bien estructurada para tu código del modelo `Attendance` en Django. Está diseñada para facilitar la comprensión del código a otros desarrolladores o a ti mismo en el futuro.

---

### Modelo `Attendance`

Este modelo representa la asistencia de un estudiante en un curso específico. Incluye la fecha de asistencia y un indicador de si el estudiante estuvo presente o ausente. Además, el modelo contiene lógica para actualizar el estado de "alumno regular" del estudiante (campo `enabled` del modelo `Registration`) en función de su porcentaje de inasistencias.

#### Campos:

- **`course`** (`ForeignKey`): Relación con el modelo `Course`, indicando el curso al que pertenece esta asistencia. Si se elimina el curso, las asistencias asociadas también serán eliminadas debido a `on_delete=models.CASCADE`.
  
- **`student`** (`ForeignKey`): Relación con el modelo `User` que representa al estudiante cuya asistencia se está registrando. El `related_name='attendances'` permite acceder a las asistencias del estudiante desde el modelo `User`, y el `limit_choices_to={'groups__name':'estudiantes'}` limita la selección de estudiantes solo a aquellos que pertenecen al grupo "estudiantes".

- **`date`** (`DateTimeField`): Fecha de la asistencia. Puede ser nula (`null=True`) o estar en blanco (`blank=True`), lo que significa que este campo es opcional.

- **`present`** (`BooleanField`): Indica si el estudiante estuvo presente (`True`) o ausente (`False`). Por defecto, se inicializa como `False`.

#### Métodos:

- **`__str__(self)`**:
  - Retorna una representación en cadena del objeto `Attendance`. En este caso, devuelve `Asistencia {id}`, donde `{id}` es el identificador único de la asistencia en la base de datos.

- **`update_registration_enabled_status(self)`**:
  - Este método actualiza el estado del campo `enabled` en el modelo `Registration`, que indica si el estudiante es considerado un "alumno regular".
  
  ##### Proceso:
  1. **Obtener el curso asociado**: Recupera la instancia del curso correspondiente a la asistencia actual.
  2. **Total de clases**: Recupera la cantidad total de clases (`class_quantity`) del curso, que está definida en el modelo `Course`.
  3. **Total de inasistencias**: Cuenta cuántas asistencias en este curso están marcadas como "ausente" (`present=False`) para el estudiante en cuestión.
  4. **Calcular el porcentaje de inasistencias**: Calcula el porcentaje de inasistencias dividiendo el total de inasistencias por el total de clases, y multiplicando por 100.
  5. **Actualizar el estado `enabled`**: Si el porcentaje de inasistencias es mayor al 20%, se marca al estudiante como "irregular" (`enabled=False`). De lo contrario, sigue siendo un "alumno regular" (`enabled=True`).
  6. **Guardar cambios**: Se guardan los cambios en el registro correspondiente del modelo `Registration`.

#### Meta:

- **`verbose_name`**: Define el nombre singular del modelo que se mostrará en la interfaz de administración de Django como "Asistencia".
  
- **`verbose_name_plural`**: Define el nombre plural que se mostrará en la interfaz de administración como "Asistencias".

---

### Ejemplo de uso:

1. **Registrar una asistencia**:
   - Cuando un estudiante asiste o falta a una clase, se crea una instancia de `Attendance` y se asignan los valores correspondientes para `course`, `student`, `date`, y `present`.

2. **Actualizar el estado de alumno regular**:
   - Después de registrar la asistencia, el método `update_registration_enabled_status()` puede ser llamado para verificar el porcentaje de inasistencias del estudiante. Si el estudiante acumula más del 20% de inasistencias, se marcará como "irregular" en el modelo `Registration`.

---

### Posibles mejoras:

1. **Automatización de la actualización del estado**:
   - El método `update_registration_enabled_status()` podría integrarse en el método `save()` de `Attendance` para que se ejecute automáticamente cada vez que se registre o actualice una asistencia. De esta forma, no sería necesario llamarlo manualmente.

   ```python
   def save(self, *args, **kwargs):
       super().save(*args, **kwargs)  # Llama al método save original
       self.update_registration_enabled_status()  # Actualiza el estado después de guardar
   ```

2. **Optimización de consultas**:
   - Para mejorar el rendimiento, podrías reducir el número de consultas a la base de datos al obtener el curso y las inasistencias en una sola consulta con `select_related` o `prefetch_related`.

---

### Conclusión:

El modelo `Attendance` no solo gestiona el registro de asistencias, sino que también incorpora una lógica que evalúa el porcentaje de inasistencias de un estudiante y actualiza su estado en el sistema, determinando si sigue siendo un "alumno regular". Esta funcionalidad es clave para realizar un seguimiento efectivo del desempeño y asistencia de los estudiantes en cada curso.

---

Este formato de documentación te ayudará a mantener tu código bien organizado y comprensible para otros desarrolladores. ¿Te gustaría añadir más funcionalidades o realizar ajustes a este código?
'''

# NOTAS
class Mark(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student = models.ForeignKey(User, on_delete=models.CASCADE,  limit_choices_to={'groups__name':'estudiantes'}, verbose_name='Estudiante')
    mark_1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 1')
    mark_2 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 2')
    mark_3 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 3')
    average = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='Promedio')

    def __str__(self):
        return str(self.course)

    # Calcular el promedio (llamo a una función)
    def calculate_average(self):
        marks = [self.mark_1, self.mark_2, self.mark_3]
        valid_marks = [mark for mark in marks if mark is not None] #comprensión de listas en Python
        if valid_marks:
            return sum(valid_marks)/len(valid_marks)
        return None
    
    def save(self, *args, **kwargs):
        # Verifico si alguna nota cambio
        if self.mark_1 or self.mark_2 or self.mark_3:
            self.average = self.calculate_average()
        super().save(*args,**kwargs)
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
# DOCUMENTACION NOTAS
'''
Este modelo `Mark` en Django representa las calificaciones de un estudiante en un curso, y contiene un mecanismo para calcular automáticamente el promedio de las notas. Vamos a explicar el código en detalle, incluyendo el método `save()` y el uso de `super()`.

### Explicación del modelo `Mark`:

1. **Campos**:
   - **`course`**: Relación con el modelo `Course` (el curso en el que se está evaluando al estudiante).
   - **`student`**: Relación con el modelo `User`, que hace referencia al estudiante que pertenece al grupo de "estudiantes".
   - **`mark_1`, `mark_2`, `mark_3`**: Campos opcionales (`null=True`, `blank=True`) que almacenan las notas. Son enteros positivos (`PositiveIntegerField`).
   - **`average`**: Campo `DecimalField` que almacena el promedio de las tres notas. Se permite un máximo de 3 dígitos y un decimal.

2. **Método `calculate_average(self)`**:
   - Este método calcula el promedio de las notas del estudiante (siempre que haya al menos una nota válida). Si no hay notas válidas, devuelve `None`.
   - Utiliza una lista `marks` que contiene las tres notas y luego filtra las que no son `None` (notas válidas).
   - Si existen notas válidas, las suma y divide por el número de notas para calcular el promedio.

3. **Método `save(self, *args, **kwargs)`**:
   - Sobrescribe el método `save()` de Django para agregar lógica personalizada antes de guardar el objeto en la base de datos. En este caso, se utiliza para calcular y asignar automáticamente el promedio antes de guardar la instancia.
   - **Verificación de las notas**: Si alguna de las notas (`mark_1`, `mark_2`, `mark_3`) ha sido asignada, se calcula el promedio llamando a `self.calculate_average()` y se guarda el resultado en `self.average`.
   - **`super().save(*args, **kwargs)`**: Llama al método `save()` original de Django para completar el proceso de guardado en la base de datos.

### Explicación de `save(self, *args, **kwargs)` y `super()`:

- **`save(self, *args, **kwargs)`**:
   - Este método en Django es responsable de guardar una instancia del modelo en la base de datos.
   - **Sobrescribirlo** te permite ejecutar lógica adicional antes o después del guardado, como en este caso, donde se calcula el promedio antes de guardar la instancia.
   - Los parámetros `*args` y `**kwargs` se incluyen para capturar argumentos posicionales y de palabra clave adicionales que puedan pasarse cuando se llama al método. Estos argumentos se pasan automáticamente por Django cuando se ejecuta el guardado, y tú no necesitas preocuparte por ellos en la mayoría de los casos.

- **`super().save(*args, **kwargs)`**:
   - El uso de `super()` llama al método `save()` del modelo base (`models.Model`) para ejecutar la lógica predeterminada de Django que efectivamente guarda el objeto en la base de datos.
   - Es crucial utilizar `super()` para asegurarse de que el proceso de guardado estándar no se interrumpa. Después de ejecutar la lógica personalizada (en este caso, calcular el promedio), `super()` garantiza que la instancia se guarde correctamente en la base de datos.

### Flujo del método `save()`:

1. Cuando intentas guardar una instancia del modelo `Mark`:
   - Primero verifica si alguna de las notas (`mark_1`, `mark_2`, `mark_3`) tiene un valor asignado.
   - Si hay notas, se llama al método `calculate_average()` para calcular el promedio y se almacena en el campo `average`.
   
2. Después de calcular el promedio (si corresponde), el método `super().save()` se ejecuta, lo que garantiza que los cambios (incluido el promedio) se guarden en la base de datos.

### Resumen:
El método `save()` sobrescrito permite calcular automáticamente el promedio de las notas antes de guardar la calificación. Al usar `super()`, te aseguras de que la lógica original de Django para guardar el modelo en la base de datos se ejecute correctamente después de tu lógica personalizada.

¿Te gustaría agregar más lógica al método `save()` o realizar alguna mejora?
'''


# SIGNALS (SEÑALES)
@receiver(post_save, sender = Attendance)
# @receiver(post_delete, sender = Attendance)
def update_registration_enabled_status(sender, instance, **kwargs):
   instance.update_registration_enabled_status()
#DOCUMENTACION
'''
Este bloque de código utiliza los **receptores de señales** (`@receiver`) de Django para ejecutar automáticamente el método `update_registration_enabled_status()` cada vez que se crea, actualiza o elimina una instancia del modelo `Attendance`. Vamos a detallar qué hace y cómo funciona.

### Explicación del código:

1. **Decoradores `@receiver(post_save, sender=Attendance)` y `@receiver(post_delete, sender=Attendance)`**:
   - Los decoradores `@receiver` se utilizan para conectar una función a una señal en Django. En este caso, estamos conectando la función `update_registration_enabled_status` a dos señales diferentes:
     - **`post_save`**: Se emite después de que una instancia de `Attendance` se haya guardado (tanto en creaciones como en actualizaciones).
     - **`post_delete`**: Se emite después de que una instancia de `Attendance` haya sido eliminada.
   - **`sender=Attendance`**: Especifica que estas señales se activan solo cuando el remitente es el modelo `Attendance`.

2. **Función `update_registration_enabled_status`**:
   - La función se ejecuta automáticamente cada vez que una asistencia se guarda o elimina.
   - **`sender`**: Es el modelo que envía la señal, en este caso, `Attendance`.
   - **`instance`**: Es la instancia de `Attendance` que fue guardada o eliminada.
   - La función simplemente llama al método `update_registration_enabled_status()` de la instancia de `Attendance`, que se encarga de recalcular el estado `enabled` del estudiante en el modelo `Registration`.

### Flujo del código:

- **Cuando se guarda o se elimina una asistencia**:
  1. Se activa la señal `post_save` o `post_delete`.
  2. La función `update_registration_enabled_status()` es llamada automáticamente.
  3. Esta función recalcula el porcentaje de inasistencias del estudiante para el curso asociado, y actualiza el campo `enabled` en el modelo `Registration` dependiendo del porcentaje de inasistencias.

### Ventajas:

1. **Automatización completa**:
   - No necesitas recordar llamar manualmente al método `update_registration_enabled_status()` después de crear, actualizar o eliminar una asistencia. Esto asegura que el estado del estudiante en el curso (si es regular o no) se mantenga siempre actualizado.

2. **Manejo de todas las modificaciones**:
   - Al conectar tanto la señal `post_save` como `post_delete`, cubres todos los casos posibles de cambios en las asistencias (creación, actualización y eliminación).

### Ejemplo de uso:

Cuando un estudiante falta a una clase y se registra una inasistencia en el sistema:
1. Se guarda la instancia de `Attendance`.
2. Automáticamente se recalcula el porcentaje de inasistencias del estudiante y se determina si sigue siendo un alumno regular (`enabled=True`) o si pasa a ser irregular (`enabled=False`).

Cuando se elimina una asistencia (por ejemplo, porque fue un error):
1. Se recalcula nuevamente el porcentaje de inasistencias, y el estado del estudiante se actualiza si es necesario.

### Código completo con señales:

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Attendance

@receiver(post_save, sender=Attendance)
@receiver(post_delete, sender=Attendance)
def update_registration_enabled_status(sender, instance, **kwargs):
    instance.update_registration_enabled_status()
```

### Resumen:
Este enfoque basado en señales garantiza que el estado del estudiante (`enabled`) en el modelo `Registration` se mantenga siempre coherente y actualizado, sin necesidad de intervención manual. Las señales de Django son útiles para ejecutar lógica automáticamente en respuesta a eventos en los modelos. 

¿Te gustaría profundizar en algún otro aspecto o mejorar alguna parte de esta lógica?
'''