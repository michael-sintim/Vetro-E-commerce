from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here


class Promotion(models.Model):
     description = models.CharField(max_length=255)
     discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+' #tells django not to create a reverse realtionship 
    )

    def __str__(self):
        return self.title


class Product(models.Model): 
    title = models.CharField(max_length=225)
    description = models.TextField()
    price =  models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey(Collection , on_delete=models.CASCADE)
    promotion = models.ManyToManyField(Promotion,related_name='products')




class Customer(models.Model):
    class MEMBERSHIP_CHOICES(models.TextChoices):
        bronze = 'B',"Bronze"
        silver = 'S',"Silver"
        gold = 'G',"Gold"

    id = models.UUIDField(default=uuid.uuid4,primary_key=True,)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField(null=True,blank=True)
    mem = models.CharField(choices=MEMBERSHIP_CHOICES.choices,max_length=1,default=MEMBERSHIP_CHOICES.bronze)

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'Store_customer'
        indexes = [
            models.Index(fields=['phone_number'])
        ]
    

class Order(models.Model):
    class PAYMENT(models.TextChoices):
        pending = 'P','Pending '
        complete = 'C','Complete '
        failed = 'F','Failed '


    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(choices=PAYMENT.choices,max_length=1, default=PAYMENT.pending)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.PROTECT)
    product= models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Address(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=260)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)



class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
