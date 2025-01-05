from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import redirect
from product .models import Product
from .models import Cart, CartItem
from order.models import Order, OrderItem
from ui_elements.views import render_nav, def_config, render_footer
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.generic import TemplateView
import stripe

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


class SetCartItemView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = {
            'product_id': request.data.get('pid'),
            'quantity': request.data.get('quantity'),
            'cart_id': _cart_id(request),
        }

        # Get the cart, and if it 
        # doesn't exist, create it
        try:
            cart = Cart.objects.get(
                cart_id = _cart_id(request)
            )  

        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()

        
        # Get the product
        product = Product.objects.get(
            id = data['product_id']
        )

        # If the quantity is 0, delete the item
        if data['quantity'] == 0:
            try:
                cart_item = CartItem.objects.get(
                    product = product,
                    cart = cart
                )
                cart_item.delete()

            except CartItem.DoesNotExist: pass
            return Response(status=status.HTTP_200_OK)


        elif product.max_quantity > data['quantity']:
            data['quantity'] = product.max_quantity


        # Else, update the quantity
        try:
            cart_item = CartItem.objects.get(
                product = product,
                cart = cart
            )

            # Since this is a /set/ endpoint,
            # we want to set the quantity,
            # not add to it
            cart_item.quantity = int(data['quantity'])

            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product, 
                quantity = data['quantity'],
                cart = cart
            )
            
            cart_item.save()


        return Response(status=status.HTTP_200_OK)
        



def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist: pass

    # GEt the user
    user = request.user
    


    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total*100)
    description = 'Online Shop - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':

        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']

            print(stripe_total)
            # 4453536674908162
            customer = stripe.Customer.create(
                email = str(email),
                description = str(description),
            )

            print('customer: ', customer)
            print('id: ', customer.id)
            print('user: ', user)

            charge = stripe.Charge.create(
                amount = stripe_total,
                currency = 'usd',
                source = token,
                description = description,
            )

            print('charge: ', charge)

            try:
                order = Order.objects.create(
                    token = token,
                    total = total,
                    emailAddress = email,
                    billingName = '',
                    user = user,
                )

                order.save()

                for order_item in cart_items:
                    oi = OrderItem.objects.create(
                        product = order_item.product.name,
                        quantity = order_item.quantity,
                        price = order_item.product.price,
                        order = order
                    )
                    oi.save()

                    # Reduce the quantity of the product
                    product = Product.objects.get(id=order_item.product.id)
                    if product.available != -1:
                        product.stock -= order_item.quantity
                        product.save()

                    
                return redirect('cart:thanks', order.id)
            
            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            print('error: ', e)
            return redirect('cart:cart_detail')

            

    # This get the active UI elements
    try:
        # Get the active 
        ui_config = def_config()
        if ui_config is None: return

        # Get the active nav
        nav_bar = render_nav(ui_config)
        footer = render_footer(ui_config)

        
    except: pass


            
    return render(request, 'cart/cart.html', {
        'cart_items':cart_items, 
        'total':total, 
        'counter':counter,
        'data_key':data_key,
        'stripe_total':stripe_total,
        'description':description,
        'nav_bar':nav_bar,
        'footer':footer,
    })


def cart_remove(request, product_id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


def cart_list(request):
    cart = Cart.objects.get(
        cart_id = _cart_id(request)
    )

    return CartItem.objects.filter(
        cart = cart, 
        active = True
    )


class ThankYouView(TemplateView):
    template_name = 'cart/thank_you.html'

    def get_context_data(self, **kwargs):
        context = super(ThankYouView, self).get_context_data(**kwargs)


        # This get the active UI elements
        try:
            # Get the active 
            ui_config = def_config()
            if ui_config is None: return

            # Get the active nav
            nav_bar = render_nav(ui_config)
            footer = render_footer(ui_config)

            
        except: pass


        context['order'] = Order.objects.get(id=self.kwargs['order_id'])
        context['nav_bar'] = nav_bar
        context['footer'] = footer

        return context