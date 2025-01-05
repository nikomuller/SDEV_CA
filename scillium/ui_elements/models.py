from django.db import models
from scillium.image_upload import rename
from django.urls import reverse
from django.core.validators import URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class Link(models.Model):
    name = models.CharField(
        max_length = 100
    )

    description = models.CharField(
        max_length = 250,
        null = True,
        blank = True
    )

    # now, a link can be multiple things
    # - URL
    # - Reverseable URL
    # - Email
    # - Phone
    # So we need to add a field to specify
    # what type of link it is
    link_type = models.CharField(
        max_length = 50,
        choices = [
            ('url', 'URL'),
            ('reverseable_url', 'Reverseable URL'),
            ('email', 'Email'),
            ('phone', 'Phone')
        ],
        default = 'url'
    )

    # We cant use URLField because we need to be able to
    # use relative links
    url = models.CharField(
        max_length = 250
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    def save(self, *args, **kwargs):
        
        match self.link_type:
            case 'url':
                validate = URLValidator()
                try: validate(self.url)
                except BaseException: 
                    raise ValidationError('Invalid URL')
                
            case 'reverseable_url':
                try: reverse(self.url)
                except BaseException: 
                    raise ValidationError('Invalid URL')

            case 'email':
                validate = EmailValidator()
                try: validate(self.url)
                except BaseException: 
                    raise ValidationError('Invalid Email')

            case 'phone':
                # TODO: Validate phone number
                pass
        
        super().save(*args, **kwargs)

    
    
    def get_url(self):
        match self.link_type:
            case 'url':
                return self.url

            case 'reverseable_url':
                return reverse(self.url)

            case 'email':
                return 'mailto:' + self.url

            case 'phone':
                return 'tel:' + self.url

# 
# Nav and Footer
# 

class Nav(models.Model):
    name = models.CharField(max_length=100)
    links = models.ManyToManyField(Link)

    def __str__(self): 
        return self.name

    class Meta:
        verbose_name = 'Nav'
        verbose_name_plural = 'Navs'


class Footer(models.Model):
    name = models.CharField(max_length=100)
    links = models.ManyToManyField(Link)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Footer'
        verbose_name_plural = 'Footers'



# 
# Details, such as contact info, 
# about us, etc.
# 

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    
class AboutUs(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    socials = models.ManyToManyField(Link)
    photo = models.ImageField(
        upload_to = rename('about_us'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def get_photo_url(self):
        return settings.MEDIA_URL + str(self.photo)

    def get_all_socials(self):
        return self.socials.all()

# 
# TOS / Privacy
# 
# We need to provide a last updated date 
# for the TOS and Privacy Policy pages
# so the user knows when the page was last updated
# 
class TermsOfService(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()

    last_updated = models.DateTimeField(
        auto_now = True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Terms of Service'
        verbose_name_plural = 'Terms of Service'

class PrivacyPolicy(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()

    last_updated = models.DateTimeField(
        auto_now = True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policy'



# 
# Configuration
# 
class Configuration(models.Model):
    name = models.CharField(
        max_length = 100
    )
    
    active_privacy_policy = models.ForeignKey(
        PrivacyPolicy,
        on_delete = models.CASCADE,
    )

    active_terms_of_service = models.ForeignKey(
        TermsOfService,
        on_delete = models.CASCADE,
    )

    nav_bar = models.ForeignKey(
        Nav,
        on_delete = models.CASCADE,
    )

    footer = models.ForeignKey(
        Footer,
        on_delete = models.CASCADE,
    )

    contacts = models.ManyToManyField(
        Contact,
        blank = True,
    )

    about_us = models.ManyToManyField(
        AboutUs,
        blank = True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configurations'

