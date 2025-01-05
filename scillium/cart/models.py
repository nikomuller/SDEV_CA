from django.db import models
from product.models import Product



class Cart(models.Model):
    cart_id = models.CharField(
        max_length = 250, 
        blank = True
    )

    date_added = models.DateField(
        auto_now_add = True
    )

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id

    def get_item_qty(self, product_id):
        try:
            cart_item = CartItem.objects.get(
                product = product_id,
                cart = self
            )
            return cart_item.quantity

        except CartItem.DoesNotExist:
            return 0



class CartItem(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete = models.CASCADE
    )

    cart = models.ForeignKey(
        Cart, 
        on_delete = models.CASCADE
    )
    
    quantity = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product


