from django.db import models
from django.core.validators import MaxLengthValidator
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length = 30, null=False)
    price = models.FloatField()
    description = models.TextField(null = True,
        validators=[
            MaxLengthValidator(150, 'Describe the item in less than 150 characters')
            ],
        )
    image = models.ImageField(upload_to='item_images')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.price = round(self.price, 2)
        super(Product, self).save(*args, **kwargs)

class User_Cart(models.Model):
    items = models.TextField
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner+"'s cart"