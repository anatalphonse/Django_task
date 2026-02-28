from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User

# Create your views here.

def login_view(request):
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
  
    user = authenticate(request, username=username, password=password)

    if user:
      login(request, user)
      return redirect("dashboard")
    
  return render(request, "login.html")

def logout_view(request):
  logout(request)
  return redirect("login")

@login_required
def dashboard(request):
  user = request.user

  if user.role == "superadmin":
    return render(request, "dashboard.html", {"type": "superadmin"})
  
  elif user.role == "admin":
    return render(request, "dashboard.html", {"type": "admin"})
  
  else: 
    return  render(request, "dashboard.html", {"type": "user"})
  
@login_required
def manage_users(request):

  if request.user.role != "superadmin":
    return redirect("dashboard")
  
  if request.method == "POST":
    action = request.POST.get("action")

    if action == "create":
      username = request.POST.get("username")
      password = request.POST.get("password")
      role = request.POST.get("role", "user")
      admin_id = request.POST.get("admin_id")

      if username and password:
        admin_user = None
        if admin_id:
          admin_user = get_object_or_404(User, id=admin_id)
        user = User.objects.create_user(
          username=username,
          password=password,
          role=role,
          admin=admin_user if role == "user" else None,
        )
    elif action == "update":
      user_id = request.POST.get("user_id")
      role = request.POST.get("role")
      admin_id = request.POST.get("admin_id")
      user = get_object_or_404(User, id=user_id)

      user.role = role
      if role == "user" and admin_id:
        admin_user = get_object_or_404(User, id=admin_id)
        user.admin = admin_user
      else:
        user.admin = None
      user.save()

    elif action == "delete":
      user_id = request.POST.get("user_id")
      user = get_object_or_404(User, id=user_id)
      if user != request.user:
        user.delete()

    return redirect("manage_users")

  users = User.objects.all()
  admins = User.objects.filter(role="admin")

  return render(request, "users.html", {"users": users, "admins": admins})

