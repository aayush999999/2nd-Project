from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_protect

# Create your views here.

def home(request):
    return render(request, 'home.html')


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.error(request, "Username Already Exsits...")
            return redirect('/register')

        user = User.objects.create(
            first_name = first_name,
            username = username,
            last_name = last_name,  
            password = password
        )

        user.set_password(password)
        user.save()
        
        messages.success(request, "Account Created Successfully.")

        return redirect('/login')

    return render(request, 'register.html')

# @csrf_protect
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login')
        
        else:
            login(request, user)
            return redirect('/details')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/login')

@login_required(login_url="/login")
def add_receipe(request):
    if request.method == "POST":
        data = request.POST

        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')

        receipe = Receipe(receipe_name = receipe_name, receipe_description = receipe_description, receipe_image = receipe_image)
        receipe.save()

        return redirect('/add-receipe')
    

    return render(request, 'add_receipes.html')

# def details(request):
#     receipe = Receipe.objects.all()
#     print(receipe)
#     return render(request, 'receipe_detail.html', context = {'receipe': receipe})

@login_required(login_url="/login")
def details(request):
    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
    context = {'receipes': queryset }

    return render(request, 'receipe_detail.html', context)


def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('details')


def update_receipe(request, id):
    queryset = Receipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST

        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        
        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()
        return redirect('/details')

    context = {'receipe': queryset }
    
    return render(request, 'update_receipe.html', context )

