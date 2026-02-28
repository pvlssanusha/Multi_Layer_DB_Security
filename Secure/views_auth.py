from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from .models import UserRole
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        print(user,"username")

        if user:
            try:
                user_role = UserRole.objects.get(user=user).role
                print("role",user_role)
            except UserRole.DoesNotExist:
                messages.error(request, "No role assigned.")
                return redirect("login")

            # 🔐 IP Restriction Check
            print("ip")
            client_ip = get_client_ip(request)
            print(client_ip,"ip")

            print(user,"entered here")

            if user_role.allowed_ip and client_ip != user_role.allowed_ip:
                messages.error(request, "Login blocked: Unauthorized IP address.")
                return redirect("login")

            # 🔐 Time Restriction Check
            current_time = timezone.localtime().time()
            print("time",current_time)

            if user_role.login_start_time and user_role.login_end_time:
                if not (user_role.login_start_time <= current_time <= user_role.login_end_time):
                    print("till here came")
                    messages.error(request, "Login blocked: Outside allowed login hours.")
                    return redirect("login")

            login(request, user)
            return redirect("records")

        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("/login/")
