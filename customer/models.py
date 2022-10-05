from django.db import models

# Create your models here.


class Customer(models.Model):

    customer_name = models.CharField(max_length=200, blank=False)
    username = models.CharField(max_length=200, blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    tel = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100, blank=False)
    confirm_password = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.username
