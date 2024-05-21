from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')


def receipe(request):
    if request.method == "POST":
        data = request.POST

        receipe_image = request.FILES['receipe_image']
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        # print(receipe_name)

        receipe = Receipe(receipe_name = receipe_name, receipe_description = receipe_description, receipe_image = receipe_image)
        receipe.save()

        return redirect('/receipe')
    

    return render(request, 'receipes.html')

# def details(request):
#     receipe = Receipe.objects.all()
#     print(receipe)
#     return render(request, 'receipe_detail.html', context = {'receipe': receipe})


def details(request):
    queryset = Receipe.objects.all()
    context = {'receipe': queryset }
    # print(context)
    return render(request, 'receipe_detail.html', context)


def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    print(id)
    queryset.delete()
    print(queryset)
    return redirect('details')