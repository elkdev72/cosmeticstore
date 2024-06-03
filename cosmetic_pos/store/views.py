from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Customer, Transaction, Store
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    stores = Store.objects.all()
    selected_store = request.GET.get('store')
    if selected_store:
        products = Product.objects.filter(store_id=selected_store)
    else:
        products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products, 'stores': stores, 'selected_store': selected_store})

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
            names = customer_name.split(' ', 1)
            if len(names) == 2:
                first_name, last_name = names
                customer, created = Customer.objects.get_or_create(first_name=first_name, last_name=last_name)
            else:
                return render(request, 'store/buy_product.html', {
                    'product': product,
                    'customers': Customer.objects.all(),
                    'error': 'Please enter a valid full name (First Last).'
                })
        else:
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
        store_id = request.POST['store']
        name = request.POST['name']
        price = request.POST['price']
        stock = request.POST['stock']
        store = get_object_or_404(Store, pk=store_id)
        Product.objects.create(name=name, price=price, stock=stock, store=store)
        return redirect('index')
    stores = Store.objects.all()
    return render(request, 'store/add_product.html', {'stores': stores})

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
