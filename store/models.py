from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    status = models.CharField(max_length=250)

    def __str__(self):
        return self.status


class Product(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="dashmain/images",
                              default="dashmain/images/default.png")
    price_sell = models.FloatField()
    price_buy = models.FloatField()
    content = RichTextUploadingField(blank=True, null=True)
    inventory = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    public_day = models.DateTimeField(default=datetime.datetime.now)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Contact(models.Model):

    email = models.EmailField(max_length=400, null=True)
    message = models.TextField()

    def __str__(self):
        return self.email
