from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'receipes.html')


def receipe(request):
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        print(receipe_name)

    return render(request, 'receipes.html')