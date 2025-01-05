from django.urls import path
from .views import (
    PrivacyPolicyView,
    TermsView,
    AboutUsView
)

app_name = 'extra'

urlpatterns = [
    path('policy', 
        PrivacyPolicyView.as_view(),
        name = 'privacy_policy'
    ),

    path('terms',
        TermsView.as_view(),
        name = 'terms_of_service'
    ),

    path('about',
        AboutUsView.as_view(),
        name = 'about_us'
    )
]