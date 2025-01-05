from django.urls import path
from .views import SplashPageView

app_name = 'splash_page'

urlpatterns = [
    path('', SplashPageView.as_view(), name='splash_page'),
]