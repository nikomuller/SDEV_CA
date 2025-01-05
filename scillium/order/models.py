from django.db import models
from users.models import User
import uuid

class Order(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key = True, 
        editable = False
    )
    
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, 
        verbose_name='Euro Order Total')
    emailAddress = models.EmailField(max_length=250, blank=True, 
        verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'Order'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)

    def get_items(self):
        return self.orderitem_set.all()


class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Euro Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'OrderItem'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product
