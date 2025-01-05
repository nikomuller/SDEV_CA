from django.template.loader import render_to_string
from .models import Configuration
from django.conf import settings
from django.utils.html import mark_safe 
from django.views.generic import TemplateView

# 
# The reason why im using a function to render the nav
# is because each model view wont have to import the
# nav bar template and render it. 
# 
def render_nav(config = None):
    # -- Get the active nav
    if config is None:
        return None

    nav = config.nav_bar

    # -- render the nav
    return mark_safe(render_to_string(
        'ui_elements/nav_bar.html',
        {
            'links': nav.links.all(),
            'name': nav.name,
        }
    ))

def render_footer(config = None):
    # -- Get the active nav
    if config is None:
        return None

    footer = config.footer

    # -- render the nav
    return mark_safe(render_to_string(
        'ui_elements/footer.html',
        {
            'links': footer.links.all(),
            'name': footer.name,
        }
    ))

def def_config():
    # -- Get the active configuration
    try:
        config = Configuration.objects.get(
            id = settings.ACTIVE_UI_CONFIGURATION_PK
        )

        # return the configuration
        return config


    except Configuration.DoesNotExist:
        return None


    
class PrivacyPolicyView(TemplateView):
    template_name = 'extra/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Try get the active configuration
        # and active ui elements configuration
        try: 
            # Get the active 
            ui_config = def_config()
            if ui_config is None: return

            # Get the active nav
            nav = render_nav(ui_config)
            foot = render_footer(ui_config)

            context['nav_bar'] = nav
            context['footer'] = foot
            context['policy'] = ui_config.active_privacy_policy
        
        except Configuration.DoesNotExist:
            pass

        return context


class TermsView(TemplateView):
    template_name = 'extra/tos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Try get the active configuration
        # and active ui elements configuration
        try: 
            # Get the active 
            ui_config = def_config()
            if ui_config is None: return

            # Get the active nav
            nav = render_nav(ui_config)
            foot = render_footer(ui_config)

            context['nav_bar'] = nav
            context['footer'] = foot
            context['policy'] = ui_config.active_terms_of_service
        
        except Configuration.DoesNotExist:
            pass

        return context


class AboutUsView(TemplateView):
    template_name = 'extra/aboutus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Try get the active configuration
        # and active ui elements configuration
        try: 
            # Get the active 
            ui_config = def_config()
            if ui_config is None: return

            # Get the active nav
            nav = render_nav(ui_config)
            foot = render_footer(ui_config)

            context['nav_bar'] = nav
            context['footer'] = foot
            context['about'] = ui_config.about_us.all()
        
        except Configuration.DoesNotExist:
            pass

        return context