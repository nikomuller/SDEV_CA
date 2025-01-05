from .models import Configuration
from django.views.generic import TemplateView
from django.conf import settings

from ui_elements.views import render_nav, def_config, render_footer


class SplashPageView(TemplateView):
    template_name = 'splash_page/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Try get the active configuration
        # and active ui elements configuration
        try: 
            config = Configuration.objects.get(
                id = settings.ACTIVE_CONFIGURATION_PK
            )

            # Get the active 
            ui_config = def_config()
            if ui_config is None: return

            # Get the active nav
            nav = render_nav(ui_config)
            foot = render_footer(ui_config)

            context['nav_bar'] = nav
            context['footer'] = foot
            context['carousel'] = config.active_carousel
            context['carousel_products'] = config.active_carousel.products.all()
        
        except Configuration.DoesNotExist:
            pass

        return context

