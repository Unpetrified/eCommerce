from itertools import product
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from .models import *
import json

class Store(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'store.html', {'products':products})

    def post(self, request):
        product_id = request.post['id']
        product = Product.objects.get(id=product_id)
        customer = request.user.customer
        order = Order.objects.get_or_create(customer=customer, complete = False)
        pass

class UpdateCart(View):
    def get(self, request):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items_in_cart = order.getItemTotal
        return JsonResponse(items_in_cart, safe=False)
    def post(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        product = Product.objects.get(id=productId)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        order_item, created = OrderItem.objects.get_or_create(product=product, order=order)

        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            order_item.quantity -= 1
        
        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()
        item_quantity = order_item.quantity
        return JsonResponse(item_quantity, safe=False)

class View(View):
    
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, 'view_item.html', {'product':product})

class Cart(View):

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete = False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'getCartTotal':0, 'getItemTotal':0}
        context = {'cart':items, 'cartDetails':order}
        return render(request, 'cart.html', context)

class Checkout(View):

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete = False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'getCartTotal':0, 'getItemTotal':0}
        context = {'cart':items, 'cartDetails':order}
        return render(request, 'checkout.html', context)

class Register(View):
    
    template_name = 'registration/register.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if len(password) < 8:
                messages = '* password must be greater than 8 characters'
                return render(request, self.template_name, {'password_error':messages})

            if User.objects.filter(username=username).exists():
                messages = '* username already taken'
                return render(request, self.template_name, {'username_error':messages})

            if User.objects.filter(email = email).exists():
                messages = '* email already used'
                return render(request, self.template_name, {'email_error':messages})
                
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login?next=/')
                
        else:
            messages = '* password mismatch'
            return render(request, self.template_name, {'password_error':messages})
