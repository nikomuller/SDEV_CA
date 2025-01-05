import uuid
from django.db import models
from django.urls import reverse
from scillium.image_upload import rename
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class ServerRequirements(models.Model): 
    name = models.CharField(max_length=50)

    # CPU 1-8
    cpu = models.IntegerField(
        default = 1,
        validators = [
            MinValueValidator(1),
            MaxValueValidator(8)
        ]
    )

    # RAM 1-32
    ram = models.IntegerField(
        default = 1,
        validators = [
            MinValueValidator(1),
            MaxValueValidator(32)
        ]
    )

    # GPU 1-4
    gpu = models.IntegerField(
        default = 0,
        validators = [
            MinValueValidator(0),
            MaxValueValidator(4)
        ]
    )


    def get_cpu_list(self):
        items = []

        for i in range(1, 9):
            items.append({
                'value': i,
                'filled': i <= self.cpu,
            })

        return items

    def get_ram_list(self):
        items = []

        for i in range(0, 17):
            items.append({
                'value': i,
                'filled': i <= self.ram // 2,
            })

        return items

    def get_gpu_list(self):
        items = []

        for i in range(1, 5):
            items.append({
                'value': i,
                'filled': i <= self.gpu,
            })

        return items



class Product(models.Model):
    # UUID ID for the product
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key = True, 
        editable = False
    )

    name = models.CharField(max_length=50)
    description = models.TextField()
    available = models.BooleanField(default=True)
    max_quantity = models.IntegerField(
        default = -1,
        validators = [
            MinValueValidator(-1)
        ]
    )
    price = models.DecimalField(
        max_digits = 6, 
        decimal_places = 2
    )

    category = models.ManyToManyField(
        'Category',
        related_name = 'products'
    )

    # One to one relationship with the server
    # requirements for the product (optional)
    server_requirements = models.OneToOneField(
        ServerRequirements,
        on_delete = models.SET_NULL,
        null = True,
        blank = True
    )


    # Stock, either a number or unlimited
    # where -1 is unlimited
    stock = models.IntegerField(
        default = -1,
        validators = [
            MinValueValidator(-1)
        ]
    )

    card_image = models.ImageField(
        upload_to = rename('products/card')
    )

    splash_image = models.ImageField(
        upload_to = rename('products/splash')
    )

    # Time limit, either a number or unlimited
    # E.g. 30 days, where -1 is unlimited
    time_limit = models.IntegerField(
        default = -1,
        validators = [
            MinValueValidator(-1)
        ]
    )

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse(
            'product:product_detail', 
            kwargs = {
                'pid': self.id
            }
        )

    def get_card_image(self):
        return settings.MEDIA_URL + str(self.card_image)
    
    def get_splash_image(self):
        return settings.MEDIA_URL + str(self.splash_image)



class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(default="")
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_search_url(self):
        return reverse(
            'product:products_by_category', 
            kwargs = {
                'category': self.slug
            }
        )


class Discount(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    description = models.TextField()
    discount = models.IntegerField(
        default = 0,
        validators = [
            MinValueValidator(0)
        ]
    )


    # Number of times the discount can be used
    # -1 is unlimited
    uses = models.IntegerField(
        default = -1,
        validators = [
            MinValueValidator(-1)
        ]
    )

    # Number of times the discount has been used
    uses_used = models.IntegerField(
        default = 0,
        validators = [
            MinValueValidator(0)
        ]
    )

    # max per user
    max_per_user = models.IntegerField(
        default = -1,
        validators = [
            MinValueValidator(-1)
        ]
    )


    # Two options, whitelist or blacklist
    product_list_selector = models.CharField(
        max_length = 10,
        choices = [
            ('whitelist', 'Whitelist'),
            ('blacklist', 'Blacklist')
        ],
        default = 'whitelist'
    )

    # The products that the list applies to
    products = models.ManyToManyField(
        Product,
        related_name = 'discounts',
        blank=True
    )



    # two options, whitelist or blacklist
    category_list_selector = models.CharField(
        max_length = 10,
        choices = [
            ('whitelist', 'Whitelist'),
            ('blacklist', 'Blacklist')
        ],
        default = 'whitelist'
    )

    # The categories that the list applies to
    categories = models.ManyToManyField(
        Category,
        related_name = 'discounts',
        blank=True
    )

