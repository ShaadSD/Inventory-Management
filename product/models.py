from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=255, default="Unknown")

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SalesRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sold_by = models.CharField(max_length=255,null=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity_sold} sold to {self.customer.name}"


class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = (
        ('In', 'In'),
        ('Out', 'Out'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    reason = models.CharField(max_length=255)
    date = models.DateField()
    actioned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} - {self.quantity}"



