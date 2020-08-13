from django.shortcuts import render, redirect
from .models import Task, Project
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required()
def home(request):
    user = request.user
    projects = Project.objects.filter(owner=user)
    return render(request, 'Application.html', {"projects": projects})


@login_required()
def add_project(request):
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["description"]
        p = Project()
        p.title = title
        p.description = desc
        p.owner = request.user
        p.save()

        proj = Project.objects.filter(owner=request.user)
        return render(request, 'Application.html', {"projects": proj})


@login_required()
def add_task(request, project_id):
    if request.method == "POST":
        title = request.POST["title"]

        t = Task()
        p = Project.objects.get(id=project_id)

        t.title = title
        t.project = p
        t.save()

        p = Project.objects.get(id=project_id)
        t = Task.objects.filter(project=p)

        user = request.user
        projects = Project.objects.filter(owner=user)
        return render(request, 'Application.html', {"tasks": t, "curr_project": p, "projects": projects})


@login_required()
def show_project(request, project_id):
    p = Project.objects.get(id=project_id)
    t = Task.objects.filter(project=p)

    user = request.user
    projects = Project.objects.filter(owner=user)
    return render(request, 'Application.html', {"tasks": t, "curr_project": p, "projects": projects})


@login_required()
def task_status(request, project_id, task_id):
    t = Task.objects.get(id=task_id)
    print(t.completion_status)
    if t.completion_status:
        t.completion_status = False
        t.save()
    else:
        t.completion_status = True
        t.save()

    p = Project.objects.get(id=project_id)
    t = Task.objects.filter(project=p)

    user = request.user
    projects = Project.objects.filter(owner=user)
    return render(request, 'Application.html', {"tasks": t, "curr_project": p, "projects": projects})


@login_required()
def task_delete(request, project_id, task_id):
    t = Task.objects.get(id=task_id)
    t.delete()
    p = Project.objects.get(id=project_id)
    t = Task.objects.filter(project=p)

    user = request.user
    projects = Project.objects.filter(owner=user)
    return render(request, 'Application.html', {"tasks": t, "curr_project": p, "projects": projects})


def delete_project(request, project_id):
    p = Project.objects.get(id=project_id)
    p.delete()

    return redirect(home)