from email.policy import default
from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, default="000")

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 100)
    
    @property
    def no_of_products(self):
        products = self.product_set.all()
        return products.count()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 100, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    description = models.TextField(null = True,
        validators=[
            MaxLengthValidator(150, 'Describe the item in less than 150 characters')
            ],
        )
    image = models.ImageField(upload_to='item_images')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.price = round(self.price, 2)
        super(Product, self).save(*args, **kwargs)

    @property
    def getImageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length = 200)

    def __str__(self):
        return self.transaction_id

    @property
    def getCartTotal(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.getTotal for item in orderitems])
        return total

    @property 
    def getItemTotal(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add = True)

    @property
    def getTotal(self):
        return self.product.price*self.quantity.__round__(2)

class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 90)
    state = models.CharField(max_length = 200)
    country = models.CharField(max_length = 200, blank=False)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.address