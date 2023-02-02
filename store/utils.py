import json, uuid
from .models import *

def cookieCart(request):
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
    return {'order' : {'getCartTotal':cartTotal, 'getItemTotal':itemTotal}, 'items' : items, 'removed' : keys}

def anonymousUser(request, data):
    userInfo = data['userInfo']
    name = userInfo['name']
    phone = userInfo['phone']
    customer = Customer(name = name, phone = phone)
    customer.save()
    order = Order(customer=customer, transaction_id = uuid.uuid4())
    order.save()
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    for key in cart:
        product = Product.objects.get(id=key)
        order_item = OrderItem(product=product, order = order, quantity = cart[key]['quantity'])
        order_item.save()
    return {'order' : order, 'customer' : customer}

def checkDeletedItems(request):
    keys = ''
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    for key in cart:
        if not Product.objects.filter(id=key):
            keys = keys.join(key)
    return keys
    