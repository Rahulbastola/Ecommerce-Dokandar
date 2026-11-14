
from django.db import models
from django.conf import settings


class Cetegory(models.Model):
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendor_categories",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class products(models.Model):
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendor_products",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    images = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    cetegory = models.ForeignKey(
        Cetegory,
        on_delete=models.CASCADE,
        related_name="products"
    )

    def __str__(self):
        return self.name
