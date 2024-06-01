from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Product, Customer, Transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'store/login.html', {'error': 'Invalid credentials'})
    return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        customer_name = request.POST.get('customer_name')
        quantity = int(request.POST['quantity'])

        if customer_id:
            customer = get_object_or_404(Customer, pk=customer_id)
        elif customer_name:
            first_name, last_name = customer_name.split(' ', 1)
            customer = Customer.objects.create(first_name=first_name, last_name=last_name)
        else:
            # Handle error case where neither customer_id nor customer_name is provided
            return render(request, 'store/buy_product.html', {
                'product': product,
                'customers': Customer.objects.all(),
                'error': 'Please select a customer or enter a new customer name.'
            })
        
        Transaction.objects.create(product=product, customer=customer, quantity=quantity)
        product.stock -= quantity
        product.save()
        return redirect('index')
    
    customers = Customer.objects.all()
    return render(request, 'store/buy_product.html', {'product': product, 'customers': customers})




@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        stock = request.POST['stock']
        Product.objects.create(name=name, price=price, stock=stock)
        return redirect('index')
    return render(request, 'store/add_product.html')

@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.save()
        return redirect('index')
    return render(request, 'store/update_product.html', {'product': product})

