from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Signup(models.Model):
    username = models.CharField(max_length=20)
    email_address = models.EmailField()
    password = models.CharField(max_length=50)
    phone_number = models.IntegerField(max_length=14)
    home_address = models.CharField(max_length=500)
    city = models.CharField(max_length=25)
    age = models.IntegerField(max_length=2)

    def __str__(self):
        template = '{0.username} | {0.email_address}'
        return template.format(self)

class ManagerSignUp(models.Model):
    username = models.CharField(max_length=20)
    qualification = models.CharField(max_length=100)
    email_address = models.EmailField()
    password = models.CharField(max_length=50)
    phone_number = models.IntegerField(max_length=14)
    home_address = models.CharField(max_length=500)
    city = models.CharField(max_length=25)
    age = models.IntegerField(max_length=2)

    def __str__(self):
        template = '{0.username} | {0.email_address}'
        return template.format(self)

class Category(models.Model):
    name =models.CharField(max_length=50)

    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class Area(models.Model):
    area = models.CharField(max_length=30)
    delivery_charges = models.IntegerField()

    def __str__(self):
        template = '{0.area} | {0.delivery_charges}'
        return template.format(self)

class OrderList(models.Model):
    food_name = models.CharField(max_length=100)
    price = models.IntegerField()
    user = models.ForeignKey(Signup,on_delete=models.CASCADE)

    def __str__(self):
        template = '{0.user} | {0.food_name} | {0.price}'
        return template.format(self)


class Food(models.Model):
    name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = "static/img/")
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    num_ratings = models.IntegerField()
    avg_rating = models.IntegerField()
    tags = models.CharField(max_length=30)

    def __str__(self):
        template = '{0.name} | {0.price} | {0.category}'
        return template.format(self)

class OrderItem(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    food = models.ForeignKey(Food, on_delete= models.CASCADE)

    def __str__(self):
        template = '{0.user} | {0.food} | {0.quantity} | {0.total_price}'
        return template.format(self)

