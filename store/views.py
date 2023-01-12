from itertools import product
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
import json
from .models import Product, User_Cart

class Store(View):

    def get(self, request):
        # cart = {"iPad":["/static/media/book.jpg",9.99,7],"Google watch":["/static/media/watch.jpg",199.99,1],"Beats by Dre":["/static/media/headphones.jpg",299.99,1]}
        products = Product.objects.all()
        # dump = json.dumps(cart)
        # dumps = json.loads(dump)
        return render(request, 'store.html', {'products':products})

class View(View):
    
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, 'view_item.html', {'product':product})

class Cart(View):

    def get(self, request):
        if request.user.is_authenticated:
            cart = User_Cart.objects.get(owner=request.user)
            return render(request, 'cart.html', {'cart':cart})
        else:
            return render(request, 'cart.html')

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
