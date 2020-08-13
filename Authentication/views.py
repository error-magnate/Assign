from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import send_mail
from .models import Verify
from Application.views import home
from random import sample


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(username=email,password=password)

        try:
            u = User.objects.get(username=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {"message": "Invalid email or password"})

        if user is not None:
            auth.login(request, user=user)
            return redirect(home)
        else:
            return render(request, 'login.html', {"message": "Please verify your account."})


def generatestring(n):
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    res1 = sample(string, n)
    res = "".join(res1)
    return res


def register(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]

        if password == confirm_password:
            try:
                u = User.objects.get(username=email)
                return render(request, 'signup.html', {"message": "User with that message already exists."})
            except User.DoesNotExist:
                u = User()
                u.first_name = name
                u.username = email
                u.set_password(password)
                u.is_active = False
                u.save()

                v = Verify()
                v.user = u
                v.pid = generatestring(20)
                v.uid = generatestring(5)
                v.save()

                msg = 'https://asssign.herokuapp.com/accounts/verify/'+ v.uid + "/" + v.pid
                return render(request, 'signup.html', {"message": "Your account has been succesfully registered \n" + msg})
        else:
            return render(request, 'signup.html', {"message": "Password didn't matched"})


def verify(request, uid, pid):
    try:
        v = Verify.objects.get(uid=uid, pid=pid)
        u = User.objects.get(username=v.user.username)
        u.is_active = True
        v.delete()
        u.save()
        return render(request, 'login.html', {"message": "Your account has been verified. Please login."})
    except Verify.DoesNotExist:
        return render(request, 'index.html')


def reset(request):
    if request.method == "POST":
        uemail = request.POST["email"]
        try:
            user = User.objects.get(username=uemail)
            password = generatestring(10)
            msg = """An Temporary password has been sent to you below. Use that password to Login in your account and then Change Your Password from the Dashboard. Your temporary password is :""" + password
            user.set_password(password)
            user.save()
            send_mail("Password Reset", msg, "sanketvy7@gmail.com", [uemail, ])
            return render(request, "reset.html", {"message": "An temporary password is sent to your email."})
        except User.DoesNotExist:
            return render(request, "reset.html", {"message": "There is no account by such email!"})
    else:
        return render(request, 'reset.html')


def logout(request):
    auth.logout(request)
    return render(request, 'index.html')




