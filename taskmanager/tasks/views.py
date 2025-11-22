from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from datetime import date, timedelta
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from .models import Task
from .forms import TaskForm
from .forms import SignUpForm

# views

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'User created successfully')
            return redirect('task_list')
    else:
        form = SignUpForm()
    # print("signup", form)
    return render(request, "tasks/form.html", {'form':form, 'signup': True})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Login successful')
                return redirect('task_list')
            else:
                messages.add_message(request, messages.SUCCESS, 'Invalid credential')
    else:
        form = AuthenticationForm()
    # print(form)
    return render(request, 'tasks/form.html', {'form': form})

@login_required
def user_logout(request):
    try:
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Logout successful')
    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Something Wrong {e}')

    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(owner = request.user).order_by('-created_at')
    # print(tasks)

    search = request.GET.get('search')
    if (search):
        tasks = tasks.filter(
            Q(title__icontains = search) | Q(description__icontains = search)
        )

    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)
    
    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority = priority)
    
    due_filter = request.GET.get('due')
    if due_filter == 'today':
        tasks = tasks.filter(due_date = date.today())
    elif due_filter == 'week':
        end_date = date.today() + timedelta(days=7)
        tasks = tasks.filter(due_date__range = [date.today(), end_date])
    elif due_filter == 'overdue':
        tasks = tasks.filter(due_date__lt=date.today(), status__in = ['pending', 'in_progress'])

    
    sort = request.GET.get('sort')
    if sort == 'oldest':
        tasks = tasks.order_by('created_at')
    
    paginator = Paginator(tasks, 8)
    page = request.GET.get('page')
    tasks = paginator.get_page(page)

    # print(tasks)

    return render(request, 'tasks/task_list.html', {'tasks':tasks})

@login_required
def user_profile(request):
    user = request.user
    total_task = Task.objects.filter(owner = request.user).count()
    completed_task = Task.objects.filter(owner = request.user, status = "completed").count()
    pending_task = Task.objects.filter(owner = request.user, status = "pending").count()
    in_progress_task = Task.objects.filter(owner = request.user, status = "in_progress").count()

    # print('Profile',user, total_task, completed_task,pending_task, in_progress_task)

    profile_info={
        'user': user,
        'total_task': total_task,
        'completed_task': completed_task,
        'pending_task': pending_task,
        'in_progress_task': in_progress_task,
    }
    return render(request, 'tasks/profile.html', {"profile_info":profile_info})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.add_message(request, messages.SUCCESS, "Task created successfully")
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, "tasks/create_task.html" , {"form":form, 'title': "Create Task"})

@login_required
def update_task(request, id):
    try:
        task = Task.objects.get(id = id, owner=request.user)
        # print("update",task)
    except Exception as e:
        messages.add_message(request, messages.ERROR, f"Something wrong {e}")
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.add_message(request, messages.SUCCESS, "Task updated successfully")
            return redirect('task_list')   
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/create_task.html', {'form':form, "title": "Update Task"})

@login_required
def task_details(request, id):
    try:
        task = Task.objects.get(id = id, owner=request.user)
        # task = get_object_or_404(Task, pk=id, owner=request.user)
        # print(task)
    except Exception as e:
        messages.add_message(request, messages.ERROR, f"Something wrong {e}")

    
    return render(request, 'tasks/task_details.html', {'task': task})


class delete_task(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_confirmation.html'
    pk_url_kwarg = "id"
    success_url = reverse_lazy("task_list")

    def delete(self, request, *args,  **kwargs ):
        messages.add_message(request, messages.SUCCESS, "Student deleted successfully")
        return super().delete(request, *args,  **kwargs )
    