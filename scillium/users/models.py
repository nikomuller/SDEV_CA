from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class UserClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    
# Create your models here.
class User(AbstractUser):
    
    credits = models.IntegerField(
        default = 0,
        validators = [
            MinValueValidator(0)
        ]
    )

    user_class = models.ManyToManyField(
        UserClass,
    )


    def __str__(self):
        return self.username 

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
