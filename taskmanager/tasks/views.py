from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from .models import Task
from .serializers import TaskSerializar
from accounts.models import User
from accounts.permissions import IsAdminOrSuperAdmin
from .services import TaskServices
from .utils import can_access_task


class MyTasksView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user
    # API spec: only return tasks assigned to the logged-in user
    tasks = Task.objects.filter(assigned_to=user)
    serializar = TaskSerializar(tasks, many=True)
    return Response(serializar.data)


class UpdateTaskView(APIView):
  permission_classes = [IsAuthenticated]

  def put(self, request, pk):
    task = get_object_or_404(Task, pk=pk)

    if not can_access_task(request.user, task):
      return Response({"error": "Not allowed"}, status=403)
    
    status_value = request.data.get("status")
    report = request.data.get("completion_report")
    hours = request.data.get("worked_hours")

    if status_value == "completed":
      try:
        TaskServices.complete_task(task, report, hours)
      except ValueError as e:
        return Response({"error": str(e)}, status=400)
    else:
      task.status = status_value
      task.save()

    return Response({"message": "Task updated successfully"})
  

class TaskReportView(APIView):
  permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

  def get(self, request, pk):
    task = get_object_or_404(Task, pk=pk)

    if not can_access_task(request.user, task):
      return Response({"error": "Not allowed"}, status=403)

    if task.status != "completed":
      return Response({"error": "Task not completed yet"}, status=400)
    
    data = {
      "task": task.title,
      "assigned_to": task.assigned_to.username,
      "completion_report": task.completion_report,
      "worked_hours": task.worked_hours,
    }
    return Response(data)
  

@login_required
def manage_tasks(request):
  user = request.user

  if user.role not in ["admin", "superadmin"]:
    return redirect("dashboard")

  if request.method == "POST":
    action = request.POST.get("action")

    if action == "create":
      title = request.POST.get("title")
      description = request.POST.get("description")
      assigned_to_id = request.POST.get("assigned_to")
      due_date = request.POST.get("due_date")

      if title and assigned_to_id and due_date:
        assigned_to = get_object_or_404(User, id=assigned_to_id)

        # Admins can only assign tasks to their own users
        if user.role == "admin" and assigned_to.admin != user:
          return redirect("dashboard")

        Task.objects.create(
          title=title,
          description=description or "",
          assigned_to=assigned_to,
          due_date=due_date,
        )

    elif action == "update":
      task_id = request.POST.get("task_id")
      status_value = request.POST.get("status")
      report = request.POST.get("completion_report")
      hours = request.POST.get("worked_hours")

      task = get_object_or_404(Task, id=task_id)

      if not can_access_task(user, task):
        return redirect("dashboard")

      if status_value == "completed":
        try:
          TaskServices.complete_task(task, report, hours)
        except ValueError:
          # For the simple admin panel, just ignore invalid submissions
          pass
      else:
        task.status = status_value
        task.save()

    elif action == "delete":
      task_id = request.POST.get("task_id")
      task = get_object_or_404(Task, id=task_id)

      if not can_access_task(user, task):
        return redirect("dashboard")

      task.delete()

    return redirect("tasks")

  if user.role == "superadmin":
    tasks = Task.objects.all()
    assignable_users = User.objects.filter(role__in=["admin", "user"])
  else:  # admin
    tasks = Task.objects.filter(assigned_to__admin=user)
    assignable_users = User.objects.filter(admin=user, role="user")

  context = {
    "tasks": tasks,
    "assignable_users": assignable_users,
  }
  return render(request, "tasks.html", context)


@login_required
def view_reports(request):

  if request.user.role not in ["admin", "superadmin"]:
    return redirect("dashboard")
  
  tasks = Task.objects.filter(status="completed")

  return render(request, "reports.html", {"tasks": tasks})


@login_required
def my_tasks_page(request):
  user = request.user

  if user.role != "user":
    return redirect("dashboard")

  if request.method == "POST":
    action = request.POST.get("action")

    if action == "update":
      task_id = request.POST.get("task_id")
      status_value = request.POST.get("status")
      report = request.POST.get("completion_report")
      hours = request.POST.get("worked_hours")

      task = get_object_or_404(Task, id=task_id)

      if not can_access_task(user, task):
        return redirect("my_tasks")

      if status_value == "completed":
        try:
          TaskServices.complete_task(task, report, hours)
        except ValueError:
          # Ignore invalid submissions for the simple UI
          pass
      else:
        task.status = status_value
        task.save()

    return redirect("my_tasks")

  tasks = Task.objects.filter(assigned_to=user)
  return render(request, "my_tasks.html", {"tasks": tasks})
