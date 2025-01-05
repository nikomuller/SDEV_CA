from django.contrib import admin
from .models import ShowcaseCarousel, Banner, Configuration
from django.utils.html import mark_safe 

class ShowcaseCarouselAdmin(admin.ModelAdmin):
    # The fields that will be displayed in the admin panel
    fields = [
        'name', 
        'description', 
        'products',
        'animation_time_ms',
        'loop_every_ms',
        'max_images',
    ]

    # The fields that will be displayed in the admin panel
    # as a list
    list_display = ('name', 'description')

    # The fields that will be used to filter the list
    # of carousels
    list_filter = ['name']

    # The fields that will be used to search for a
    # carousel
    search_fields = ['name']

    filter_horizontal = ('products',)

admin.site.register(ShowcaseCarousel, ShowcaseCarouselAdmin)


class BannerAdmin(admin.ModelAdmin):
    fileds = ['title', 'description', 'color', 'link']



    # Lets display the color of the banner 
    # in the admin panel, in its own column
    def color_elm(self, obj):
        return mark_safe(
            """
                <div style="    
                    width: 100%; 
                    height: 100%; 
                    background-color: {0};
                    color: #00000000;
                    border-radius: 5px;
                ">
                .
                </div>
            """.format(obj.color)            
        )

    color_elm.allow_tags = True
    color_elm.short_description = 'Color'
    


    # We also want to display the link of the banner
    # but, we don't want to display the whole link
    # as it might be too long, so we will display
    # only the first x characters of the link
    def link_elm(self, obj):
        match obj.link:
            case None:
                return 'No link'
            
            case _: return mark_safe(
                """
                    <a href="{0}" target="_blank">
                        {1}
                    </a>
                """.format(
                    obj.link,
                    obj.link[:20] + '...'
                )
            )

    link_elm.allow_tags = True
    link_elm.short_description = 'Link'


    list_display = (
        'title', 
        'description', 
        'color_elm', 
        'link_elm'
    )
    list_filter = ['title']
    search_fields = ['title']

admin.site.register(Banner, BannerAdmin)



class ConfigurationAdmin(admin.ModelAdmin):
    fields = ['name', 'active_carousel', 'active_banner']
    
    # we want to display the name of the active carousel
    # and the active banner, not the id
    def active_carousel_elm(self, obj):
        return obj.active_carousel.name
    
    active_carousel_elm.short_description = 'Active Carousel'

    def active_banner_elm(self, obj):
        match obj.active_banner:
            case None: return mark_safe(
                # We want to change the color to red to signify
                # that there is no active banner, so theres no
                # confusion
                """<span style="color: #ff0000;">No active banner</span>"""
            )
            case _: return obj.active_banner.title
    
    active_banner_elm.allow_tags = True
    active_banner_elm.short_description = 'Active Banner'

    list_display = (
        'name',
        'active_carousel_elm',
        'active_banner_elm'
    )



admin.site.register(Configuration, ConfigurationAdmin)