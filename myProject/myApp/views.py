from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Catergory, Customer
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm

from payment.forms import ShippingForm
from payment.models import ShippingAdd, Order

from django import forms


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, "myapps/product.html", {'product': product} )

def category(request, category_id):
    # Get the category
    category = get_object_or_404(Catergory, id=category_id)
    
    # Filter products by category
    products = Product.objects.filter(catergory=category)
    
    # Paginate the products
    paginator = Paginator(products, 8)  # Display 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "myapps/category.html", {
        'category': category,
        'page_obj': page_obj
    })

def myaccount(request):
    user = request.user

    customer = Customer.objects.all()
    orders = Order.objects.filter(user=user)
    return render(request, "myapps/myaccount.html",  {'customer': customer, 'orders': orders } )


def home(request):
    products = Product.objects.all()
    category = Catergory.objects.all()

    paginator = Paginator(products, 8)  # Show 12 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get products for the current page
    return render(request, "myapps/home.html", {'products': products, 'category' : category, 'page_obj': page_obj} )


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request. POST['password']
        user = authenticate(request, username=username, password=password )
        if user is not None:
            login(request, user)
            messages.success(request, "You have sucessfully logged in !!!")
            return redirect('index')
        else:
            messages.success(request, "Couldnt Log you In, Please try again !!!")
            return redirect('login')
    else:
        return render(request, 'myapps/login.html', {})
        


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out "))
    return(redirect('index'))

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Log in the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Your Account has been Created Successfully!")
                return redirect('index')
            else:
                messages.error(request, "Authentication failed. Please try logging in.")
                return redirect('login')
        else:
            messages.error(request, "Failed to Create Account. Try Again.")
    else:
        form = SignUpForm()  # Only initialize an empty form for GET requests

    return render(request, 'myapps/register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        shipping_user = ShippingAdd.objects.get(user=request.user)
        ship_form = ShippingForm(request.POST or None, instance=shipping_user)

        if user_form.is_valid() or ship_form.is_valid():
            user_form.save()
            ship_form.save()
            login(request, current_user)
            messages.success(request, "Your Profile has updated Successfully ")
            return redirect('index')
        return render(request, 'myapps/update_user.html', {'user_form': user_form, 'ship_form': ship_form })
    else:
        messages.success(request, "You need to Login to Access this Page ")
        return redirect('index')


def order_detail(request):
    return render(request, 'myapps/order_detail.html', )

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']

        results = Product.objects.filter(name__icontains=searched)

        return render(request, 'myapps/search.html', {'searched': searched, 'results': results } )



def chatbot_response(request):
    if request.method == "POST":
        data = request.json()
        user_message = data.get('message')

        # Send the user's message to the chatbot microservice
        chatbot_url = "http://127.0.0.1:5000/predict"  # Adjust based on your Flask service
        response = request.post(chatbot_url, json={'message': user_message})
        
        if response.status_code == 200:
            bot_message = response.json().get('answer')
            return JsonResponse({'answer': bot_message})
        else:
            return JsonResponse({'error': 'Failed to get a response from the chatbot'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)