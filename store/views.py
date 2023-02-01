from ast import Or
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from .models import *
import json, uuid

class Store(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'store.html', {'products':products})

class UpdateCart(View):
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        if created:
            order.transaction_id = uuid.uuid4()
            order.save()
        items_in_cart = order.getItemTotal
        cart_total = order.getCartTotal.__round__(2)
        context = {'items':items_in_cart, 'total':cart_total}
        return JsonResponse(json.dumps(context), safe=False)
    def post(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        product = Product.objects.get(id=productId)
        customer = request.user.customer
        order = Order.objects.get(customer=customer, complete = False)
        order_item, created = OrderItem.objects.get_or_create(product=product, order=order)

        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            order_item.quantity -= 1
        
        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()
        
        item_quantity = order_item.quantity
        total = order_item.getTotal.__round__(2)

        context = {'item_qnty':item_quantity, 'item_total':total}

        return JsonResponse(json.dumps(context), safe=False)

class View(View):
    
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, 'view_item.html', {'product':product})

    def post(self, request, id):
        
        product = Product.objects.get(id=id)
        order = Order.objects.get(customer = request.user.customer, complete=False)
        order_item, created = OrderItem.objects.get_or_create(order = order, product = product)
        
        order_item.quantity = int(request.body)
        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()

        return JsonResponse("Item added to cart successfully", safe=False)

class Cart(View):

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete = False)
            items = order.orderitem_set.all()
        else:
            try:
                cart = json.loads(request.COOKIES['cart'])
            except:
                cart = {}
            items = []
            cartTotal = 0
            itemTotal = 0
            for key in cart:
                product = Product.objects.get(id=key)
                total = product.price * cart[key]['quantity']
                item = {
                    'product' : {
                        'id' : product.id,
                        'name' : product.name,
                        'price' : product.price,
                        'getImageUrl' : product.getImageUrl
                    },
                    'quantity' : cart[key]['quantity'],
                    'getTotal' : total
                }
                items.append(item)
                cartTotal += total
                itemTotal += cart[key]['quantity']
            order = {'getCartTotal':cartTotal, 'getItemTotal':itemTotal}
        context = {'cart':items, 'cartDetails':order}
        return render(request, 'cart.html', context)

class Checkout(View):

    def post(self, request):
        data = json.loads(request.body)
        shippingInfo = data['shippingInfo']
        address = shippingInfo['address']
        city = shippingInfo['city']
        state = shippingInfo['state']
        country = shippingInfo['country']
        if request.user.is_authenticated:
            customer = request.user.customer
            order = Order.objects.filter(customer=customer)
            order = order[order.count()-1]
        else:
            userInfo = data['userInfo']
            name = userInfo['name']
            phone = userInfo['phone']
            customer = Customer(name = name, phone = phone)
            customer.save()
        
        shipping = Shipping(customer=customer, order=order, address=address, city=city, state=state, country=country)
        shipping.save()
        
        if float(data['userInfo']['total']) != order.getCartTotal or order.getCartTotal == 0:
            return JsonResponse('Order could not be processed. Try again', safe=False)    
        order.complete = True
        order.save()
        return JsonResponse('Order processed. Payment made', safe=False)

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete = False)
            if created:
                order.transaction_id = uuid.uuid4()
                order.save()
            items = order.orderitem_set.all()
            if Shipping.objects.filter(customer=customer).exists and Shipping.objects.filter(customer=customer).count() > 0:
                shipping = Shipping.objects.filter(customer=customer)
                shipping = shipping[shipping.count()-1]
            else:
                shipping = ""
        else:
            items = []
            order = {'getCartTotal':0, 'getItemTotal':0}
            shipping=""
        context = {'cart':items, 'cartDetails':order, 'shippingDetails':shipping}
        return render(request, 'checkout.html', context)

class Register(View):
    
    template_name = 'registration/register.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if len(password) < 8:
                messages = '* password must be greater than 8 characters'
                return render(request, self.template_name, {'password_error':messages})

            if User.objects.filter(username=username).exists():
                messages = '* username already exists try another one'
                return render(request, self.template_name, {'username_error':messages})

            if User.objects.filter(email = email).exists():
                messages = '* email already in used'
                return render(request, self.template_name, {'email_error':messages})
                
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            customer = Customer(user=user, name=username, phone = phone)
            customer.save()
            return redirect('login?next=/')
                
        else:
            messages = '* password mismatch'
            return render(request, self.template_name, {'password_error':messages})