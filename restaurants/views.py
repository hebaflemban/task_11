from django.shortcuts import render, redirect
from .models import Restaurant, Item
from .forms import RestaurantForm, ItemForm, SignupForm, SigninForm
from django.contrib.auth import login, authenticate, logout
from django.http import Http404

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("restaurant-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('restaurant-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")

def no_access(request):
    context = {
        "msg" : 'you have no access!'
    }
    return render(request, 'no_access.html', context)

def restaurant_list(request):
    context = {
        "restaurants":Restaurant.objects.all()
    }
    return render(request, 'list.html', context)


def restaurant_detail(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    items = Item.objects.filter(restaurant=restaurant)
    context = {
        "restaurant": restaurant,
        "items": items,
    }
    return render(request, 'detail.html', context)

def restaurant_create(request):
    if request.user.is_authenticated:
        form = RestaurantForm()
        if request.method == "POST":
            form = RestaurantForm(request.POST, request.FILES)
            if form.is_valid():
                restaurant = form.save(commit=False)
                restaurant.owner = request.user
                restaurant.save()
                return redirect('restaurant-list')
    else:
        return redirect('signin')

    context = {
        "form":form,
    }
    return render(request, 'create.html', context)

def item_create(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if request.user.is_staff or restaurant.owner == request.user:
        form = ItemForm()
        if request.method == "POST":
            form = ItemForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.restaurant = restaurant
                item.save()
                return redirect('restaurant-detail', restaurant_id)
    else:
        return redirect ('no_access')

    context = {
        "form":form,
        "restaurant": restaurant,
    }
    return render(request, 'item_create.html', context)

def restaurant_update(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)

    if request.user.is_staff or restaurant_obj.owner == request.user:
        restaurant_obj = Restaurant.objects.get(id=restaurant_id)
        form = RestaurantForm(instance=restaurant_obj)
        if request.method == "POST":
            form = RestaurantForm(request.POST, request.FILES, instance=restaurant_obj)
            if form.is_valid():
                form.save()
                return redirect('restaurant-list')
    else:
        return redirect ('no_access')

    context = {
        "restaurant_obj": restaurant_obj,
        "form":form,
    }
    return render(request, 'update.html', context)

def restaurant_delete(request, restaurant_id):
    if request.user.is_staff:
        restaurant_obj = Restaurant.objects.get(id=restaurant_id)
        restaurant_obj.delete()
        return redirect('restaurant-list')
    else:
        return redirect ('no_access')
