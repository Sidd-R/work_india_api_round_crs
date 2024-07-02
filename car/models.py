from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Car(models.Model):
    class Category(models.IntegerChoices):
        HATCHBACK = 0
        SEDAN = 1
        SUV = 2
        LUXURY = 3
    # CATEGORY_CHOICES = [
    #     (0,HATCHBACK),
    #     (1,SEDAN),
    #     (2,SUV),
    #     (3,LUXURY)
    # ]
    model = models.CharField(max_length=100)
    category = models.SmallIntegerField(choices=Category)
    number_plate = models.CharField(max_length=10)
    current_city = models.CharField(max_length=100)
    rent_per_hr = models.SmallIntegerField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id} {self.category} {self.model}"
    
class Transaction(models.Model):
    car_id = models.ForeignKey(Car,on_delete=models.SET_NULL,null=True)
    user_id = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    hours_requirement = models.SmallIntegerField()
    total_payable_amt = models.IntegerField()
    
    def __str__(self) -> str:
        return f"{self.car_id} {self.user_id.user_name} {self.hours_requirement}"
    