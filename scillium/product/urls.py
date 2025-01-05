from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # Display all products
    path('', 
        views.prod_list, 
        name = 'all_products'
    ),


    # Display all products by category
    path(
        '?category=<str:category>/', 
        views.prod_list, 
        name = 'products_by_category'
    ),


    # Search for products
    path(
        'search/',
        views.prod_list,
        name = 'search'
    ),

    # Search with category
    path(
        'search?category=<str:category>',
        views.prod_list,
        name = 'search_with_category'
    ),


    # Display a specific products
    # details
    path(
        'view/<uuid:pid>/', 
        views.product_detail, 
        name = 'product_detail'
    ),
]