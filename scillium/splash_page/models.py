from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from product.models import Product


# 
# This model will hold the games that will
# be displayed on the splash page's carousel
# 
class ShowcaseCarousel(models.Model):
    
    # Name of the carousel, this will be used
    # to identify the carousel in the admin panel
    # eg "Featured Games", "New Games", etc.
    name = models.CharField(
        max_length = 100,
        unique = True
    )

    # Description of the carousel,
    # eg "Featured Games", "New Games", etc.
    description = models.TextField(
        max_length = 100,
    )

    # The games that will be displayed in the carousel
    products = models.ManyToManyField(
        Product
    )

    loop_every_ms = models.IntegerField(
        default = 5000,
        validators = [
            MinValueValidator(1000)
        ]
    )

    animation_time_ms = models.IntegerField(
        default = 750,
        validators = [
            MinValueValidator(500)
        ]
    )

    max_images = models.IntegerField(
        default = 5,
        validators = [
            MinValueValidator(2)
        ]
    )

    # The background color of the carousel


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Display Carousel"
        verbose_name_plural = "Display Carousels"


# 
# This class will hold banner setups,
# such as sales, warnings, etc.
# 
class Banner(models.Model):

    # The title of the banner
    title = models.CharField(
        max_length = 100,
        unique = True
    )

    # The description of the banner
    description = models.TextField(
        max_length = 100,
    )

    # The color of the banner
    color = ColorField(
        default = '#000000'
    )

    # The link that the banner will redirect to
    link = models.URLField(
        max_length = 100,
        null = True,
        blank = True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"





class Configuration(models.Model):
    name = models.CharField(
        max_length = 100,
        unique=True
    )

    # We can live without a banner
    active_banner = models.ForeignKey(
        Banner,
        on_delete = models.DO_NOTHING,
        null = True,
        blank = True
    )


    # But, we can't live without a carousel
    # as its the main feature of the splash page
    active_carousel = models.ForeignKey(
        ShowcaseCarousel,
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return "Configuration"

    def get_active_banner(self):
        match self.active_banner:
            case None: return None
            case banner: return banner

    def get_active_carousel(self):
        return self.active_carousel

    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"

