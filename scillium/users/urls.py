from django.urls import path
from .views import (
    SignUpView, 
    DetailView,
    LoginView,
    LogoutView,
    ResetView
)

app_name = 'account'

urlpatterns = [
    path('', DetailView.as_view(), name='detail'),
    path('register', SignUpView.as_view(), name='register'),
    path('reset', ResetView.as_view(), name='reset'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
