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

def buy_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        quantity = int(request.POST['quantity'])
        customer = get_object_or_404(Customer, pk=customer_id)
        Transaction.objects.create(product=product, customer=customer, quantity=quantity)
        product.stock -= quantity
        product.save()
        return HttpResponseRedirect(reverse('index'))
    customers = Customer.objects.all()
    return render(request, 'store/buy_product.html', {'product': product, 'customers': customers})


