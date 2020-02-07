# use django library specifically for authentication of users
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MenuItem, Topping, Address, OrderHeader, OrderLines, Type


# Create your views here.
def index(request):
# .is_authenticated is built-in method
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    items = MenuItem.objects.all()
    context = {
        # get user information
        "user": request.user,
        "items": items,
        "type": False
    }
    # display welcome user page
    return render(request, "orders/index.html", context)

def indexf(request, type_id):
# .is_authenticated is built-in method
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    type = Type.objects.get(pk=type_id)
    if (type.description == 'Sicilian' or type.description=='Regular'):
        type = {
            "id": 0,
            "description": 'Pizza',
        }
        items = MenuItem.objects.filter(type_new__in=[1,6])
    else:
        items = MenuItem.objects.filter(type_new = type_id)
    context = {
        # get user information
        "user": request.user,
        "items": items,
        "type": type
    }
    # display welcome user page
    return render(request, "orders/index.html", context)

def item(request, item_id):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    current_user = request.user
    try:
        order_id = request.session['order_id']
    except:
        order_id = False
    if order_id:
        order = OrderHeader.objects.get(pk=order_id)
    else:
        order = OrderHeader(user_id = current_user)
        order.save()
        request.session['order_id'] = order.id
    item = MenuItem.objects.get(pk = item_id)
    if ((item.type_new.description=="Sicilian" or item.type_new.description=="Regular") and
            item.number_of_toppings != 0):
        context = {
            "image": item.type_new.image_name,
            "order": order,
            "toppings": Topping.objects.exclude(valid_for='S'),
            "item": item,
        }
    elif (item.type_new.description=="Subs" and item.options != 'C'):
        context ={
            "image": item.type_new.image_name,
            "order": order,
            "toppings": Topping.objects.exclude(valid_for='P'),
            "item": item,
        }
    elif (item.type_new.description=="Subs" and item.options == 'C'):
        context ={
            "image": item.type_new.image_name,
            "order": order,
            "item": item,
            "cheese": True,
            "toppings": Topping.objects.filter(name='Cheese')

        }
    else:
        context={
            "image": item.type_new.image_name,
            "order": order,
            "item": item,
        }
    return render(request, "orders/customize.html", context)

def selected_toppings(request, order_id, item_id):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    current_user = request.user
    order = OrderHeader.objects.get(pk = order_id)
    item = MenuItem.objects.get(pk = item_id)
    ol = OrderLines(order_id = order)
    ol.item = item
    ol.save()
    if request.method == 'POST':
        toppings=request.POST.getlist('toppings')
        for each in toppings:
            topping = Topping.objects.get(pk = each)
            if topping.name == 'Cheese':
                ol.extra_cheese = True
            ol.options.add(topping)

        ol.save()
        order.save()
    return HttpResponseRedirect(reverse('index'))

def review_order(request):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    try:
        order_id = request.session['order_id']
    except:
        order_id = False
    print(order_id)
    if order_id == False:
        return render(request, "orders/error.html", {"message": "You have no items in cart"})

    order = OrderHeader.objects.get(pk = order_id)
    lines = OrderLines.objects.filter(order_id = order)
    context ={
        "header": order,
        "lines": lines
    }
    return render(request, "orders/review_order.html", context)

def delete_line(request, line_id):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    try:
        order_id = request.session['order_id']
    except:
        order_id = False
    ol = OrderLines.objects.get(pk=line_id)
    order = OrderHeader.objects.get(pk = order_id)
    ol.delete()
    order.save()
    return HttpResponseRedirect(reverse('review_order'))

def delete_order(request):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    try:
        order_id = request.session['order_id']
    except:
        order_id = False
    order = OrderHeader.objects.get(pk = order_id)
    order.delete()
    del request.session['order_id']

    return HttpResponseRedirect(reverse('index'))




def cancel_item(request):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    return HttpResponseRedirect(reverse('index'))


def profile(request, user_id):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    return render(request, "orders/index.html")



def login_view(request):
    """ Receives login form submission """
    # Get username and password as posted to login page
    username = request.POST["username"]
    password = request.POST["password"]
    print(username, password)
    # call built-in method to authenicate user
    user = authenticate(request, username=username, password=password)
    # if authenicated user
    if user is not None:
        # call built-in login function
        login(request, user)
        # go to main page
        return HttpResponseRedirect(reverse("index"))
    else:
        # Invalid error
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def add_user(request):
    """ Receives info to add a user """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.save()
        login(request, user)
        context = {
            # get user information
            "user": request.user
        }
        # display welcome user page
        return render(request, "users/user.html", context)

def new_user(request):
        return render(request, "users/new_user.html")


def logout_view(request):
    if not request.user.is_authenticated:
        # display login form
        return render(request, "users/login.html", {"message": None})
    logout(request)
    return render(request, "users/login.html")
