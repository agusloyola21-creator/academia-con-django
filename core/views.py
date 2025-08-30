from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,View,CreateView,UpdateView,DeleteView,ListView,DetailView
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate,login
from .forms import RegisterForm,ProfileForm,UserForm,CourseForms, UserCreationForm
from django.utils.decorators import method_decorator
from .models import Course,Registration,Mark,Attendance
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
import os
from django.conf import settings
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth import update_session_auth_hash
from accounts.models import Profile



def plural_to_singular(plural):
    # Diccionario de palablas
    plural_singular = {
        'estudiantes':'estudiante',
        'profesores':'profesor',
        'preceptores':'preceptor',
        'administrativos':'administrativo',
        }
    return plural_singular.get(plural, 'error')

# OBTENER COLOR Y GRUPO DE UN USUARIO
def get_group_and_color(user):
  
  group = user.groups.first()
  group_name = None
  group_name_singular = None
  group_color = None
  group_id = None
  if group:
    if group.name == 'estudiantes':
      group_color = 'bg-primary'
    elif group.name == 'profesores':
      group_color = 'bg-success'
    elif group.name == 'preceptores':
      group_color = 'bg-secondary'
    elif group.name == 'administrativos':
      group_color = 'bg-danger'

    group_id = group.id  
    group_name = group.name
    group_name_singular = plural_to_singular(group.name)
  
  return group_id, group_name, group_color, group_name_singular


def add_group_name_to_context(view_class):
  original_dispatch = view_class.dispatch
  

  def dispatch(self, request, *args, **kwargs):
    
    user = self.request.user
    
    group_id, group_name, group_color, group_name_singular = get_group_and_color(user)

    context = {
      'group_name' : group_name,
      'group_name_singular' : group_name_singular,
      'group_color' : group_color
    }

    self.extra_context = context
    return original_dispatch(self, request, *args, **kwargs)  
  
  view_class.dispatch = dispatch
  return view_class



'''# CUSTOM_TEMPLATEVIEW
# class CustomTemplateView(TemplateView):
#   group_name = None
#   group_name_singular = None
#   group_color = None
#   def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       user = self.request.user
      
#       if user.is_authenticated:
#           group = Group.objects.filter(user=user).first()
#           if group:
#               if group.name == 'estudiantes':
#                 self.group_color = 'bg-primary'
#               elif group.name == 'profesores':
#                 self.group_color = 'bg-success'
#               elif group.name == 'preceptores':
#                 self.group_color = 'bg-secondary'
#               elif group.name == 'administrativos':
#                 self.group_color = 'bg-danger'
#               self.group_name = group.name
#               self.group_name_singular = plural_to_singular(group.name)
#       context['group_name']=self.group_name
#       context['group_name_singular']=self.group_name_singular
#       context['group_color']=self.group_color
#       return context'''

# PAGINA DE INICIO
@add_group_name_to_context
class HomeView(TemplateView):
    template_name = 'home.html'

#DOCUMENTACION
'''
El código que has proporcionado es una **vista basada en clases** en Django, específicamente una vista basada en `TemplateView`.
 A continuación te explico el funcionamiento de la clase `HomeView` y lo que hace en detalle:

### Descripción del código:

1. **`class HomeView(TemplateView)`**:
   - Esta clase hereda de `TemplateView`, que es una vista basada en clases proporcionada por Django para renderizar plantillas.
   - El uso de `TemplateView` es conveniente cuando simplemente deseas mostrar una plantilla y enviar datos adicionales al contexto de la plantilla.

2. **`template_name = 'home.html'`**:
   - Este atributo especifica la plantilla que será renderizada cuando se acceda a esta vista. En este caso, la plantilla es `home.html`.

3. **`get_context_data(self, **kwargs)`**:
   - Este método se utiliza para personalizar el contexto que se enviará a la plantilla.
   - **`context = super().get_context_data(**kwargs)`**:
     - Llama al método `get_context_data` de la clase base (`TemplateView`) para asegurarse de que se mantenga el contexto que ya está definido.
   - **`user = self.request.user`**:
     - Obtiene el usuario que está haciendo la solicitud a la vista a través de `self.request`.
   - **`group_name = None`**:
     - Inicializa la variable `group_name` como `None`. Esto será útil para almacenar el nombre del grupo al que pertenece el usuario.
   - **`if user.is_authenticated:`**:
     - Verifica si el usuario está autenticado. Si no lo está, el bloque de código dentro no se ejecutará.
   - **`group = Group.objects.filter(user=user).first()`**:
     - Realiza una consulta para obtener el primer grupo asociado al usuario que está autenticado. Utiliza el método `filter` para buscar los grupos
       relacionados con el usuario.
     - **`.first()`** se utiliza para obtener solo el primer grupo en el caso de que el usuario pertenezca a más de uno.
   - **`if group:`**:
     - Si se encuentra un grupo para el usuario, se guarda el nombre del grupo en la variable `group_name`.
   - **`context['group_name'] = group_name`**:
     - Se agrega la variable `group_name` al contexto, que será accesible en la plantilla `home.html`.

4. **Retorno del contexto**:
   - Una vez que se ha agregado `group_name` al contexto, este se devuelve para ser utilizado en la plantilla.

### ¿Qué hace este código?

Cuando un usuario accede a la página asociada a la vista `HomeView`:

- Si el usuario está autenticado, el sistema busca el grupo al que pertenece.
- Si el usuario tiene un grupo, su nombre se almacena en la variable `group_name` y se pasa al contexto.
- Si no está autenticado o no pertenece a ningún grupo, `group_name` será `None`.
- Este valor de `group_name` estará disponible en la plantilla `home.html` y se puede utilizar para mostrar el grupo al que pertenece el usuario.

### Ejemplo de uso en la plantilla (`home.html`):

En tu plantilla `home.html`, podrías hacer algo como esto para mostrar el nombre del grupo del usuario:

```html
{% if group_name %}
    <p>Bienvenido, perteneces al grupo: {{ group_name }}</p>
{% else %}
    <p>No perteneces a ningún grupo.</p>
{% endif %}
```

### Resumen:
Este enfoque utiliza una vista basada en clases para mostrar una página con un contexto personalizado que incluye el nombre del grupo del usuario autenticado.
Es útil para proporcionar información específica del usuario en la plantilla. Si el usuario no está autenticado o no pertenece a ningún grupo, la plantilla mostrará un mensaje alternativo.
'''

# PAGINA DE PRECIOS
@add_group_name_to_context
class PricingView(TemplateView):
    template_name = 'pricing.html'


# REGISTRO USUARIO
class RegisterView(View):
  def get(self, request):
    data = {
      'form': RegisterForm()
    }
    return render(request, 'registration/register.html', data)
  
  def post(self,request):
    user_creation_form = RegisterForm(data=request.POST)
    if user_creation_form.is_valid():
      user_creation_form.save()
      user = authenticate(username = user_creation_form.cleaned_data['username'],
                          password = user_creation_form.cleaned_data['password1'] )
      login(request, user)

      # Actualizamos el campo created_by_admin del Modelo Profile
      user.profile.created_by_admin = False
      user.profile.save()
    
      return redirect('home')
    
    data = {
      'form': user_creation_form
    }
    return render(request, 'registration/register.html', data)


# PAGINA DE PERFIL
@add_group_name_to_context
class ProfileView(TemplateView):

  """
  Clase ProfileView que gestiona la visualización y actualización del perfil de usuario.

  Esta vista basada en clases hereda de CustomTemplateView (que a su vez hereda de TemplateView),
  y permite mostrar y actualizar los datos del usuario autenticado, incluyendo información 
  tanto de la cuenta de usuario como del perfil adicional.

  Atributos:
  - template_name (str): Especifica el archivo de plantilla que será renderizado ('profile/profile.html').

  Métodos:
  - get_context_data(self, **kwargs): Sobrescribe el contexto para incluir los formularios de usuario y perfil.
  - post(self, request, *args, **kwargs): Maneja la lógica de la actualización de los datos cuando se envían los formularios.
  """

  template_name =  'profile/profile.html'

  def get_context_data(self, **kwargs):

    """
    Sobrescribe el método get_context_data para incluir los formularios de actualización de usuario
    y perfil en el contexto de la plantilla.

    Parámetros:
    - kwargs: Diccionario de parámetros adicionales.

    Retorna:
    - context (dict): Contexto actualizado con los formularios 'user_form' y 'profile_form'.
    """
    # Llama al método get_context_data de la clase base para obtener el contexto inicial
    context =  super().get_context_data(**kwargs)
    # Obtiene el usuario autenticado que está haciendo la solicitud
    user = self.request.user
    
    # Agrega los formularios al contexto con los datos del usuario y perfil
    '''
    Agregar los formularios al contexto en una vista basada en clases tiene un propósito muy importante: **permitir que los formularios se muestren y se gestionen dentro de la plantilla HTML**. En este caso específico, los formularios de usuario (`UserForm`) y perfil (`ProfileForm`) se agregan al contexto para que sean accesibles desde la plantilla `profile/profile.html`, permitiendo al usuario interactuar con ellos.

### Explicación detallada:

#### 1. **Incluir formularios en la plantilla**:
   Django utiliza un mecanismo de contexto para pasar datos desde la vista a la plantilla HTML. Al agregar los formularios `UserForm` y `ProfileForm` al contexto, se asegura que estos objetos puedan ser referenciados y renderizados dentro de la plantilla HTML.

   ```python
   context['user_form'] = UserForm(instance=user)
   context['profile_form'] = ProfileForm(instance=user.profile)
   ```

   - **`context['user_form']`**: Se asocia al formulario `UserForm`, que contiene los datos actuales del usuario (`instance=user`).
   - **`context['profile_form']`**: Se asocia al formulario `ProfileForm`, que contiene los datos actuales del perfil del usuario (`instance=user.profile`).

   Estos formularios son enviados al HTML como parte del contexto, y pueden ser utilizados para mostrar campos de entrada pre-rellenados con los datos del usuario y su perfil.

#### 2. **Renderizar formularios en el HTML**:
   Cuando los formularios se agregan al contexto, puedes acceder a ellos en la plantilla y mostrarlos de forma interactiva. En el archivo `profile.html`, puedes usar algo como:

   ```html
   <form method="post" enctype="multipart/form-data">
       {% csrf_token %}
       {{ user_form.as_p }}
       {{ profile_form.as_p }}
       <button type="submit">Actualizar perfil</button>
   </form>
   ```

   - **`{{ user_form.as_p }}`**: Renderiza el formulario de usuario en formato HTML (`<input>`, `<textarea>`, etc.) con los datos actuales del usuario.
   - **`{{ profile_form.as_p }}`**: Hace lo mismo, pero para el formulario de perfil, mostrando los campos del perfil (como dirección, teléfono, imagen, etc.).

#### 3. **Enviar datos desde la plantilla hacia la vista**:
   Al agregar estos formularios al contexto, puedes capturar los datos ingresados por el usuario cuando este envía el formulario. Es decir, cuando el usuario actualiza su información y presiona "Guardar" en el navegador, los datos ingresados son enviados de vuelta al servidor como parte de la solicitud POST.

#### 4. **Reutilización del contexto en la vista POST**:
   Si el usuario envía datos inválidos, debes mostrar el formulario de nuevo con los errores indicados. Aquí también es necesario volver a pasar los formularios al contexto:

   ```python
   context = self.get_context_data()
   context['user_form'] = user_form
   context['profile_form'] = profile_form
   ```

   Esto permite que, si el formulario tiene errores, los datos ingresados y los mensajes de error se muestren nuevamente en la misma página, para que el usuario pueda corregirlos.

### Resumen:

- **Agregar los formularios al contexto** es esencial para que puedas:
  - Mostrar los formularios en la plantilla HTML.
  - Rellenar los formularios con los datos existentes del usuario.
  - Permitir que el usuario modifique su información.
  - Enviar los datos modificados de vuelta al servidor y mostrar errores si es necesario.

Sin esta inclusión en el contexto, los formularios no se mostrarían ni funcionarían correctamente en la página web.
    
    '''


    context['user_form'] = UserForm(instance=user)
    context['profile_form'] = ProfileForm(instance=user.profile)

    if user.groups.first().name == 'profesores':
      #obtener todos los cursos asignados al profesor
      assigned_courses = Course.objects.filter(teacher = user).order_by('-id')
      inscription_courses = assigned_courses.filter(status='I')
      progress_courses = assigned_courses.filter(status='P')
      finalized_courses = assigned_courses.filter(status='F')


      context['assigned_courses'] = assigned_courses
      context['inscription_courses'] = inscription_courses
      context['progress_courses'] = progress_courses
      context['finalized_courses'] = finalized_courses



    elif user.groups.first().name == 'estudiantes'  :
      registrations = Registration.objects.filter(student=user)
      
      student_id = user.id
      enrolled_course = []
      inscription_courses = []
      progress_courses = []
      finalized_courses = []

      for registration in registrations:
        course = registration.course
        enrolled_course.append(course)

        if course.status == 'I':
          inscription_courses.append(course)
        elif course.status == 'P':
          progress_courses.append(course)
        elif course.status == 'F':
          finalized_courses.append(course)

      context['enrolled_course'] = enrolled_course
      context['inscription_courses'] = inscription_courses
      context['progress_courses'] = progress_courses
      context['finalized_courses'] = finalized_courses
      context['student_id'] = student_id
    
    elif user.groups.first().name == 'preceptores'  :
      all_courses = Course.objects.all()
      inscription_courses = all_courses.filter(status='I')
      progress_courses = all_courses.filter(status='P')
      finalized_courses = all_courses.filter(status='F')


      
      context['all_courses'] = all_courses
      context['inscription_courses'] = inscription_courses
      context['progress_courses'] = progress_courses
      context['finalized_courses'] = finalized_courses
    
    
    
    elif user.groups.first().name == 'administrativos':
      #Obtengo todos los usuarios que no pertenecen al grupo administrativo
      admin_group = Group.objects.get(name='administrativos')
      all_user = User.objects.exclude(groups__in=[admin_group])

      #obtengo todos los grupos
      all_groups = Group.objects.all()

      # Obtengo cada prfil de usuario
      user_profiles = []
      for user in all_user:
        profile = user.profile
        user_groups = user.groups.all()
        processed_groups = [plural_to_singular(group.name) for group in user_groups]
        user_profiles.append({
          'user': user,
          'groups': processed_groups,
          'profile': profile
        })

        context['user_profiles'] = user_profiles

        # Obtener todos los cursos
        all_courses = Course.objects.all()
        inscription_courses = all_courses.filter(status='I')
        progress_courses = all_courses.filter(status='P')
        finalized_courses = all_courses.filter(status='F')

        
        context['inscription_courses'] = inscription_courses
        context['progress_courses'] = progress_courses
        context['finalized_courses'] = finalized_courses


      
    # Retorna el contexto actualizado
    return context

  def post(self,request,*args, **kwargs):

    """
    Maneja la lógica del formulario cuando el usuario envía una solicitud POST para actualizar 
    los datos de perfil.

    Parámetros:
    - request: Objeto HttpRequest que contiene los datos de la solicitud.
    - args, kwargs: Argumentos adicionales.

    Retorna:
    - Redirección a la página de perfil si los formularios son válidos.
    - Renderizado de la página con los formularios y los errores si los datos son inválidos.
    """
    user = self.request.user
    # Crea instancias de los formularios con los datos enviados en POST, asociadas al usuario
    user_form = UserForm(request.POST, instance=user)
    profile_form = ProfileForm(request.POST,request.FILES, instance=user.profile)

    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      # Rediracciona a la pagina de perfil con los datos actualizados
      redirect('profile')
    
    # Si alguno de los datos no es valido
    context = self.get_context_data()
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    return render(request,'profile/profile.html', context)


# MOSTRAR TODOS LOS CURSOS
@add_group_name_to_context
class CoursesView(TemplateView):
  template_name = 'courses.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    courses = Course.objects.all().order_by('-id')
    student = self.request.user if self.request.user.is_authenticated else None

    for item in courses:
      if student:
        registration = Registration.objects.filter(course=item, student=student).first()
        item.is_enrolled = registration is not None
      else:
        item.is_enrolled = False
      
      enrollment_count = Registration.objects.filter(course=item).count()
      item.enrollment_count = enrollment_count

    context['courses'] = courses
    # print(f"""CURSOS: {courses} ESTUDIANTES: {student} CONTEXTO:{context} 
    # registration:{registration}
    # enrollment_count: {enrollment_count}
    # """)
    return context

# PAGINA DE ERROR PARA LOS QUE NOS SON ADMINISTRATIVOS
@add_group_name_to_context
class ErrorView(TemplateView):
  template_name = 'error.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    error_image_path = os.path.join(settings.MEDIA_URL, 'error.png')
    context['error_image_path'] = error_image_path
    return context

# CREAR UN NUEVO CURSO    
@add_group_name_to_context
class CourseCreateView(UserPassesTestMixin,CreateView):
  model = Course
  form_class= CourseForms
  template_name = 'create_course.html'
  success_url = reverse_lazy('courses')

  def test_func(self):
    return self.request.user.groups.filter(name='administrativos').exists()

  def handle_no_permission(self):
    return redirect('error_page')

  def form_valid(self, form):
    messages.success(self.request, 'El registro se ha guardado correctamente' )
    return super().form_valid(form)
  
  def form_invalid(self, form):
    messages.error(self.request, 'Ha ocurrido un error al guardar el registro')
    return self.render_to_response(self.get_context_data(form=form))

# EDICION DE UN CURSO
@add_group_name_to_context
class CourseEditView(UserPassesTestMixin,UpdateView):
  model = Course
  form_class = CourseForms
  template_name = 'edit_course.html'
  success_url = reverse_lazy('courses')

  def test_func(self):
    return self.request.user.groups.filter(name='administrativos').exists()
  
  def handle_no_permission(self):
    return redirect('error_page')

  def form_valid(self, form):
    form.save()
    messages.success(self.request, 'El registro se ha actualizado satisfactoriamente')
    return redirect(self.success_url)

  def form_invalid(self, form):
    messages.error(self.request, 'Ha ocurrido un erro al actualizar el registro')
    return self.render_to_response(self.get_context_data(form=form))

# ELIMINACION DE UN CURSO
@add_group_name_to_context
class CourseDeleteView(UserPassesTestMixin,DeleteView):
  model = Course
  template_name = 'delete_course.html'
  success_url = reverse_lazy('courses')

  def test_func(self):
    return self.request.user.groups.filter(name='administrativos').exists()
  
  def handle_no_permission(self):
    return redirect('error_page')

  def form_valid(self, form):
    messages.success(self.request, 'El registro se ha eliminado correctamente')
    return super().form_valid(form)


# REGISTRO DE UN USUARIO AL CUROS
@add_group_name_to_context
class CourseEnrollmentView(TemplateView):
  def get(self, request, course_id):
    course = get_object_or_404(Course, id = course_id)

    if request.user.is_authenticated and request.user.groups.first().name == 'estudiantes':
      student = request.user

      # Crear un registro de inscripción asociado al estudiante y el curso
      registration = Registration(course=course, student=student)
      registration.save()

      messages.success(request, 'Inscripción existosa')
    else:
      messages.error(request, 'No se pudo completar la inscripción')
    
    return redirect('courses')

# MOSTRAR LISTA DE ALUMNOS Y NOTAS A LOS PROFESORES
@add_group_name_to_context
class StudentListMarkView(TemplateView):
  template_name = 'student_list_mark.html'
  def get_context_data(self, **kwargs):
    
    context =  super().get_context_data(**kwargs)
    course_id = self.kwargs['course_id']
    course = get_object_or_404(Course, id = course_id)
    marks = Mark.objects.filter(course = course)

    student_data = []
    for mark in marks:
      student = get_object_or_404(User, id = mark.student_id)
      student_data.append({
        'mark_id':mark.id,
        'name':student.get_full_name(),
        'mark_1':mark.mark_1,
        'mark_2':mark.mark_2,
        'mark_3':mark.mark_3,
        'average':mark.average,
      })

    context['course'] = course
    context['student_data'] = student_data
    return context

# ACTUALIZAR NOTAS DE ALUMNOS
@add_group_name_to_context
class UpdateMarkView(UpdateView):
  model = Mark
  fields = ['mark_1', 'mark_2', 'mark_3']
  template_name = 'update_mark.html'

  def get_success_url(self):
    return reverse_lazy('student_list_mark', kwargs = {'course_id': self.object.course.id})
  
  def form_valid(self, form):
    response = super().form_valid(form)
    return redirect(self.get_success_url())
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    mark = self.get_object()
    context['course_name'] = mark.course.name
    return context

# VISTA PARA VER ASISTENCIAS
@add_group_name_to_context
class AttendanceListView(ListView):
  model = Attendance
  template_name = 'attendance_list.html'

  def get_queryset(self):
    course_id = self.kwargs['course_id']
    return Attendance.objects.filter(course_id=course_id, date__isnull=False).order_by('date')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    course = Course.objects.get(id=self.kwargs['course_id'])
    students = Registration.objects.filter(course=course).values('student__id','student__first_name','student__last_name','enabled')

    all_dates = Attendance.objects.filter(course=course, date__isnull=False).values_list('date', flat=True).distinct().order_by('date')
    # formatted_dates = []
    # for date in all_dates:
    #   formatted_dates.append(date.strftime("%Y-%m-%d")) 
    # #print(formatted_dates)

    remaining_classes = course.class_quantity - all_dates.count()

    attendance_data = []

    for date in all_dates:
        attendance_dict = {
          'date': date,
          'attendance_data':[]
        }
        
        for student in students:
            try:
              attendance = Attendance.objects.get(course=course, student_id=student['student__id'], date=date)
              attendance_status = attendance.present         
            except Attendance.DoesNotExist:
              attendance_status = False

            student_data = {
              'student': student,
              'attendance_status': attendance_status,
              'enabled': student['enabled'] 
            }

            attendance_dict['attendance_data'].append(student_data)
            
        attendance_data.append(attendance_dict)
        


    context['course'] = course
    context['students'] = students
    context['attendance_data'] = attendance_data
    context['remaining_classes'] = remaining_classes

    return context

# VISTA PARA AGREGAR ASISTENCIAS
@add_group_name_to_context
class AddAttendanceView(TemplateView):
  template_name = 'add_attendance.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    course_id = self.kwargs['course_id']
    course = Course.objects.get(id=course_id)
    registrations = Registration.objects.filter(course = course)
    context['course'] = course
    context['registrations'] = registrations
    return context

  def post(self, request, course_id):
    date = request.POST.get('date')
    course = Course.objects.get(id=course_id)
    registrations = Registration.objects.filter(course = course)

    if Attendance.objects.filter(course=course, date=date).exists:
      messages.error(request, 'La fecha ya existe para este curso')
      return redirect('add_attendance', course_id=course_id)
    else:  
      for registration in registrations:
        
        present = request.POST.get('attendance_' + str(registration.student.id))
        attendance = Attendance.objects.filter(student=registration.student, course=course, date=None).first()
        
        if attendance:
          attendance.date = date
          attendance.present = bool(present)
          attendance.save()
          attendance.update_registration_enabled_status()


    return redirect('list_attendance', course_id=course_id)

# VISTA MODAL EVOLUCION DEL ESTUDIANTE
def evolution(request, course_id,student_id):
  course = get_object_or_404(Course, id = course_id)
  course_status = course.status
  teacher = course.teacher.get_full_name()
  class_quantity = course.class_quantity
  student = student_id
  registration_status = Registration.objects.filter(course = course, student=student).values('enabled').first()
  attendance = Attendance.objects.filter(course = course, student=student)
  marks = Mark.objects.filter(course = course, student = student)

  attendance_data = []
  marks_data = []

  attendance_data = [
    {
      'date': attendance.date.strftime('%d-%m-%Y'),
      'present': attendance.present
    }
    for attendance in attendance if attendance.date is not None
  ]

  marks_data = [
    {
      'mark_1': item.mark_1,
      'mark_2': item.mark_2,
      'mark_3': item.mark_3,
      'average': item.average,
    }
    for item in marks
  ]

  evolution_data = {
    'registration_status':registration_status,
    'course_status': course_status,
    'teacher': teacher,
    'class_quantity': class_quantity,
    'course_name': course.name,
    'attendance_data': attendance_data,
    'marks_data': marks_data,
  }

  return JsonResponse(evolution_data, safe=False)

# CAMBIAR CONTRASEÑA DE USUARIO
@add_group_name_to_context
class ProfilePasswordChangeView(PasswordChangeView):
  template_name = 'profile/change_password.html'
  success_url = reverse_lazy('profile')

  def form_valid(self, form):
    # Actualizar el campo create_by_admin del modelo Profile
    profile = Profile.objects.get(user = self.request.user)
    profile.created_by_admin = False
    profile.save()
    
    
    messages.success(self.request, 'Cambio de contraseña exitoso')
    update_session_auth_hash(self.request, form.user)
    self.request.session['password_changed'] = True
    return super().form_valid(form)
  
  def form_invalid(self, form):
    messages.error(self.request, 'No se pudo cambiar la contraseña, intente nuevamente')
    return super().form_invalid(form)

# AGREGAR UN NUEVO USUARIO DESDE EL ADMIN
@add_group_name_to_context
class AddUserView(UserPassesTestMixin,LoginRequiredMixin,CreateView ):
  model = User
  form_class = UserCreationForm
  template_name = 'add_user.html'
  success_url = reverse_lazy('profile')
  
  
    
  def test_func(self):
      return self.request.user.groups.filter(name='administrativos').exists()

  
  def handle_no_permission(self):
    return redirect('error_page')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    groups = Group.objects.all()
    singular_groups = [plural_to_singular(group.name).capitalize() for group in groups]
    context['groups'] = zip(groups, singular_groups)
    
    return context

  def form_valid(self, form):
    # Obtener el grupo que seleccionó
    group_id = self.request.POST['group']
    group = Group.objects.get(id = group_id)
    
    # Crear usuario sin guardarlo aún
    user = form.save(commit = False)
    
    # Colocamos una contraseña por defecto - Aca podria ir la logica para crear una contraseña aleatoria
    user.set_password('contraseña')

    # Convertir a un usuario al staff
    if group_id != '1':
      user.is_staff = True
    
    # Creamos el usuario
    user.save()

    # Agregamos el usuario al grupo seleccionado
    user.groups.clear() # limpio el grupo por defecto 'estudiante'
    user.groups.add(group)
    
    
    return super().form_valid(form)


# LOGUIN PERSONALIZADO
@add_group_name_to_context
class CustomLoginView(LoginView):
  def form_valid(self, form) :
    response = super().form_valid(form)
    #Acceder al perfil de usuario
    profile = self.request.user.profile

    #Verificamos el valor del campo created_by_admin
    if profile.created_by_admin:
      messages.info(self.request, 'BIENVENDO, Cambie su contraseña ahora!!!')
      response['Location'] = reverse_lazy('profile_password_change')
      response.status_code = 302

    return response

  def get_success_url(self):
    return super().get_success_url()

# VISUALIZACION DEL PERFIL DE UN USUARIO
@add_group_name_to_context
class UserDetailsView(LoginRequiredMixin,DetailView):
  model = User
  template_name = 'user_details.html'
  context_object_name = 'usuario'

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    user = self.object
    
    group_id, group_name, group_color, group_name_singular = get_group_and_color(user)

    # Obtener todos los grupos
    groups = Group.objects.all()
    singular_names = [plural_to_singular(group.name).capitalize() for group in groups]
    groups_ids = [group.id for group in groups]
    singular_groups = zip(singular_names,groups_ids)

    context['group_id_profile'] = group_id
    context['group_name_profile'] = group_name
    context['group_name_singular_profile'] = group_name_singular
    context['group_color_profile'] = group_color
    context['singular_groups'] = singular_groups
    

    if user.groups.first().name == 'profesores':
      #obtener todos los cursos asignados al profesor
      assigned_courses = Course.objects.filter(teacher = user).order_by('-id')
      inscription_courses = assigned_courses.filter(status='I')
      progress_courses = assigned_courses.filter(status='P')
      finalized_courses = assigned_courses.filter(status='F')


      context['assigned_courses'] = assigned_courses
      context['inscription_courses'] = inscription_courses
      context['progress_courses'] = progress_courses
      context['finalized_courses'] = finalized_courses



    elif user.groups.first().name == 'estudiantes'  :
      registrations = Registration.objects.filter(student=user)
      
      student_id = user.id
      enrolled_course = []
      inscription_courses = []
      progress_courses = []
      finalized_courses = []

      for registration in registrations:
        course = registration.course
        enrolled_course.append(course)

        if course.status == 'I':
          inscription_courses.append(course)
        elif course.status == 'P':
          progress_courses.append(course)
        elif course.status == 'F':
          finalized_courses.append(course)

      context['enrolled_course'] = enrolled_course
      context['inscription_courses'] = inscription_courses
      context['progress_courses'] = progress_courses
      context['finalized_courses'] = finalized_courses
      context['student_id'] = student_id
    
    elif user.groups.first().name == 'preceptores'  :
      all_courses = Course.objects.all()
      inscription_courses = all_courses.filter(status='I')
      progress_courses = all_courses.filter(status='P')
      finalized_courses = all_courses.filter(status='F')


      
      context['all_courses'] = all_courses
      context['inscription_courses'] = inscription_courses
      context['progress_courses'] = progress_courses
      context['finalized_courses'] = finalized_courses

    
  
    
    return context

# GRABACION DE UN USUARIO

def superuser_edit(request,user_id):
  if not request.user.is_superuser:
    return redirect('error')

  user = User.objects.get(pk=user_id)
  if request.method == 'POST':
      user_form = UserForm(request.POST, instance=user)
      profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
      group = request.POST.get('group')

      if user_form.is_valid() and profile_form.is_valid():
          user_form.save()
          profile_form.save()
          user.groups.clear()
          user.groups.add(group)
          return redirect('user_details', pk=user.id)
  else:
      user_form = UserForm(instance=user)
      profile_form = ProfileForm(instance=user.profile)

  context = {
      'user_form': user_form,
      'profile_form': profile_form
  }
  return render(request, 'profile/user_details.html', context)