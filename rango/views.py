from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.
from django.http import HttpResponse


# chap3
'''
def index(request):
    return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")
'''
# chap4
'''
def index(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/index.html', context=context_dict)
'''
# chap6
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    return render(request, 'rango/index.html', context=context_dict)

# chap3
'''
def about(request):
    return HttpResponse("Rango says here is the about page.<a href='/rango/'>Index</a>")
'''

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')

# chap7 categoryform
# restrict
@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

# chap 7 pageform
# restrict
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', 
                                kwargs={'category_name_slug': 
                                        category_name_slug}))
        
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}

    return render(request, 'rango/add_page.html', context=context_dict)


# chap 9
def register(request):
    # True when registration succeeds.
    registered = False

    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # hash the password with the set_password method
            user.set_password(user.password)
            user.save()

            # set commit=False. This delays saving the model
            profile = profile_form.save(commit=False)
            profile.user = user
            
            # if user provide a profile picture, get it from the input form, put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            # registration was successful
            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, forms will be blank
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


# chap9
def user_login(request):
    # If the request is a HTTP POST
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # a User object is returned if it is
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                # looks up the URL patterns in Rango’surls.pymodule to find a URL calledrango:index, and substitutes in the corresponding pattern
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        # No context variables to pass to the template system
        return render(request, 'rango/login.html')


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))



'''
# Decorator test (restrict)
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
'''

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


