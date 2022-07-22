from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from accounts.models import User


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories '

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug])


class Product(models.Model):
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to='image/')
    description = RichTextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug])
