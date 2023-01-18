from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .models import *

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
        context = {'cart':items, 'cartDetails':order}
        return render(request, 'cart.html', context)

class Checkout(View):

    def get(self, request):
        return render(request, 'checkout.html')

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
