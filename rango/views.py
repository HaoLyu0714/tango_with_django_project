from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

# chap3
'''
def index(request):
    return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")
'''

def index(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/index.html', context=context_dict)

# chap3
'''
def about(request):
    return HttpResponse("Rango says here is the about page.<a href='/rango/'>Index</a>")
'''

def about(request):
    return render(request, 'rango/about.html')


