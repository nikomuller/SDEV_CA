from django.contrib import admin
from .models import Product, Category, Discount, ServerRequirements
from django.utils.html import mark_safe 

class ProductAdmin(admin.ModelAdmin):
    # Lets add a copy UUID button,
    # makes things easier to debug
    def copy_uuid(self, obj):
        return mark_safe("""
            <a onclick="navigator.clipboard.writeText('{0}')"
            >Copy UUID</a>
        """.format(obj.id))
        
    copy_uuid.allow_tags = True
    copy_uuid.short_description = 'Copy UUID'


    # A button to actually view the product
    def view_product(self, obj):
        return mark_safe("""
            <button onclick="window.open('{0}', '_blank')"
            >View Product</button>
        """.format(obj.get_absolute_url()))

    view_product.allow_tags = True
    view_product.short_description = 'View Product'


    # A Nice visual demonstration if 
    # the product is available or not
    def available_disp(self, obj):
        base_str = """
            <p style="
                width: 100%;
                height: 100%;
                background-color: {0};
                color: #000;
                border-radius: 5px;
                padding: 0;
                margin: 0;
                text-align: center;
            ">{1}</p>
            """

        # If the product is available
        if obj.available:
            return mark_safe(base_str.format('#00ff00', 'Available'))

        # If the product is not available
        return mark_safe(base_str.format('#ff0000', 'Unavailable'))

    available_disp.allow_tags = True
    available_disp.short_description = 'Available'

    list_display = [
        'available_disp',
        'available',
        'name', 
        'price', 
        'stock',
        'view_product',
        'copy_uuid',
        'server_requirements'
    ] 
    
    filter_horizontal = ('category',)

    list_editable = [
        'price', 
        'stock',
        'available',
    ] 
    list_per_page = 20
    
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)



class DiscountAdmin(admin.ModelAdmin):
    # Lets display a formatted view of the ammoutn
    # of available discounts
    def discount_elm(self, obj):
        if obj.uses == -1:
            return mark_safe("""
                <p style="
                    text-align: center;
                ">{0}/Inf</p>
                """.format(obj.uses_used))

        return mark_safe("""
            <p style="
                text-align: center;
            ">{0}/{1}</p>
            """.format(obj.uses_used, obj.uses))

    discount_elm.allow_tags = True
    discount_elm.short_description = 'Discounts used'
    

    list_display = ['name', 'description', 'discount', 'code', 'discount_elm']
    readonly_fields = ('uses_used', )
    filter_horizontal = ('products', 'categories')
    list_editable = ['discount', 'code']

admin.site.register(Discount, DiscountAdmin)


class ServerRequirementsAdmin(admin.ModelAdmin):
    list_display = ['name', 'cpu', 'ram', 'gpu']
    
    

admin.site.register(ServerRequirements, ServerRequirementsAdmin)