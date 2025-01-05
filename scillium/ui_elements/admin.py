from django.contrib import admin
from django.utils.html import mark_safe 
from .models import (
    TermsOfService, 
    PrivacyPolicy, 
    Configuration, 
    AboutUs, 
    Contact,
    Footer, 
    Link, 
    Nav, 
)


# 
# Navbar
# 
class NavAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

    filter_vertical = ('links',)

admin.site.register(Nav, NavAdmin)


#
# Footer
#
class FooterAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

    filter_vertical = ('links',)

admin.site.register(Footer, FooterAdmin)


#
# Links
#
class LinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    list_filter = ['name']

    search_fields = [
        'name',
        'url',
        'description',
    ]

admin.site.register(Link, LinkAdmin)


#
# Terms of Service
#
class TermsOfServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_updated']
    list_filter = ['name']

    search_fields = [
        'name',
        'content',
    ]

admin.site.register(TermsOfService, TermsOfServiceAdmin)


#
# Privacy Policy
#
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_updated']
    list_filter = ['name']

    search_fields = [
        'name',
        'content',
    ]

admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)


#
# About Us
#
class AboutUsAdmin(admin.ModelAdmin):
    # Lets actually show the photo
    # as a little thumbnail
    def photo_tag(self, obj):
        return mark_safe(
            """
                <img src="{0}" style="width: 3rem; height: 3rem;" />
            """.format(obj.photo.url)
        )

    photo_tag.allow_tags = True
    photo_tag.short_description = 'Image'
    
    list_display = ['name', 'photo_tag']

    list_filter = ['name']
    search_fields = ['name']

    filter_horizontal = ('socials', )
    
admin.site.register(AboutUs, AboutUsAdmin)


#
# Contact
#
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Contact, ContactAdmin)

#
# Configuration
#
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

    filter_horizontal = (
        'contacts',
        'about_us',
    )

admin.site.register(Configuration, ConfigurationAdmin)