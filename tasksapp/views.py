from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.db import IntegrityError
from .form import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html', {'title': 'Pagina Principal'})


def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html', {'title': 'Crear usuario', 'form': UserCreationForm})
    else:
        if request.POST["username"] == "" or request.POST['password1'] == "" or request.POST['password2'] == "":
            return render(request, 'signup.html', {'title': 'Crear usuario', 'form': UserCreationForm, 'error': 'Data emty'})
        if request.POST["username"] != "" and request.POST['password1'] == request.POST['password2']:
            try:
                # registrar usuarios
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST['password1'])
                user.save()
                # para que el navegador cree una cookie con los datos!!
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {'title': 'Crear usuario', 'form': UserCreationForm, 'error': 'Username already exists'})

        return render(request, 'signup.html', {'title': 'Crear usuario', 'form': UserCreationForm, 'error': 'Password do not match'})


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'title': "Login",
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'title': "Login",
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')


@login_required
def singout(request):
    logout(request)
    return redirect('home')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'title': 'Tareas Pendientes', 'tasks': tasks})

@login_required
def tasks_create(request):
    if request.method == "GET":
        return render(request, 'tasks_create.html', {'title': 'Crear una tarea', "form": TaskForm})
    else:
        try:
            # TaskForm usamos el form de el formulario que se hizo en el form.py
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks_create.html', {'title': 'Crear una tarea', "form": TaskForm, "error": "Error creating task."})

# ?Lista de tareas completadas
@login_required
def tasks_comlete(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'title': 'Tareas completadas','tasks': tasks})


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'tasks_detail.html', {'title': 'Detalles de la tarea', 'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'title': 'Detalles de la tarea','task': task, 'form': form, 'error': "Error updating task"})

# ?Completar tarea
@login_required
def complete_tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
