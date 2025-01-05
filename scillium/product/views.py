from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage 
from cart.views import cart_list
from ui_elements.views import render_nav, def_config, render_footer
from django.db.models import Q


def get_def(
    request,
    param,
    default
):
    try : return request.GET.get(param, default)
    except: return default



def prod_list(
    request, 
    category = None
):
    # Variables
    if category is None:
        category = str(get_def(request, 'category', ''))
    page = int(get_def(request, 'page', 1))
    nav_bar = None
    footer = None

    search_query = get_def(request, 'q', None)
    search_url = reverse_lazy('product:search')


    # Get the products
    products = Product.objects.filter(
        available = True
    )

    if search_query:
        products = products.filter(
            Q(name__icontains = search_query) |
            Q(description__icontains = search_query)
        )
    


    if category:
        try:
            category = Category.objects.get(
                slug = category
            )

            products = Product.objects.filter(
                category = category, 
                available = True
            )

            search_url = reverse_lazy(
                'product:search_with_category',
                kwargs = { 'category': 
                    category.slug
                }
            )

        except: pass

    paginator = Paginator(products, 6)


    # This handles the products
    # that correspond to the page number
    try: products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)


    # This get the active UI elements
    try:
        # Get the active 
        ui_config = def_config()
        if ui_config is None: return

        # Get the active nav
        nav_bar = render_nav(ui_config)
        footer = render_footer(ui_config)

        
    except: pass
        

    # Get the cart
    cart_items = []
    try: cart_items = cart_list(request)
    except: pass

    item_ids = []   
    for item in cart_items:
        item_ids.append(item.product.id)



    # Reconfigure the product objects
    # and supply them with details about
    # the cart
    for product in products:
        if product.id in item_ids:
            product.in_cart = True
        else: product.in_cart = False

        product.qty = 0

        for item in cart_items:
            if item.product.id == product.id:
                product.qty = item.quantity


    # Jumbotron text
    override_jumbotron = False
    jumbotron_text = ''

    if category and search_query is not None:
        override_jumbotron = True
        jumbotron_text = 'Search results for: ' + str(search_query) + ' in ' + str(category)

    elif search_query is not None:
        override_jumbotron = True
        jumbotron_text = 'Search results for: ' + str(search_query)

    elif category:
        override_jumbotron = True
        jumbotron_text = 'Category: ' + str(category)

    jumbo = {
        'text': jumbotron_text,
        'override': override_jumbotron
    }

    return render(
        request, 
        'product/list.html',
        {
            'category': category,
            'search_url': search_url,
            'categorys': Category.objects.all(),
            'products': products,
            'nav_bar': nav_bar,
            'footer': footer,
            'cart_items': cart_items,
            'jumbotron': jumbo
        }
    )




def product_detail(request, pid):
    product = Product.objects.get(
        id = pid
    )

    # Get the cart
    cart_items = []
    try: cart_items = cart_list(request)
    except: pass

    # Try to get the product
    # from the cart
    product.in_cart = False
    product.qty = 0

    for item in cart_items:
        if item.product.id == product.id:
            product.in_cart = True
            product.qty = item.quantity
            break


    # This get the active UI elements
    try:
        # Get the active 
        ui_config = def_config()
        if ui_config is None: return

        # Get the active nav
        nav_bar = render_nav(ui_config)
        footer = render_footer(ui_config)
        
    except: pass


    return render(
        request, 
        'product/detail.html', 
        {
            'product': product,
            'nav_bar': nav_bar,
            'cart_items': cart_items,
            'footer': footer
        }
    )
    

