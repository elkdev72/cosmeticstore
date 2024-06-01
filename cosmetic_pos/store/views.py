from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Product, Customer, Transaction
from django.http import HttpResponseRedirect
from django.urls import reverse

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
