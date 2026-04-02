from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    class Meta:
        abstract = True


class Category(Timestamp):
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/', null=True)

    @property
    def normalize_category(self):
        return self.category.replace(' ', '').lower()

    def __str__(self):
        return self.category


class Product(Timestamp):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    views = models.IntegerField(default=0)
    mid_rate = models.FloatField(default=0)
    description = models.TextField()

    def __str__(self):
        return f'{self.id} | {self.name}'

    @property
    def image_url(self):
        first_image = self.product_image.first()
        if first_image and first_image.image:
            return first_image.image.url
        return '/static/img/latest-product/lp-1.jpg'

    @property
    def get_mid_rate(self):
        rates = self.rate_set.all()
        mid = 0
        try:
            mid = sum([i.rate for i in rates]) / rates.count()
        except ZeroDivisionError:
            pass
        self.mid_rate = mid
        self.save()
        return mid


class ProductImage(Timestamp):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return f'image of {self.product}'


class Rate(Timestamp):
    RATE = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATE, default=0)

    def __str__(self):
        username = self.user.username if self.user else 'deleted-user'
        return f'rate of {username}'
