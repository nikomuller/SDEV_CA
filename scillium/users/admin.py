from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, UserClass

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ['email', 'username', 'credits', 'is_staff',]
    list_filter = ('is_staff', 'is_active', 'credits',)

    filter_vertical = ('user_class',)

admin.site.register(User, CustomUserAdmin)


class UserClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(UserClass, UserClassAdmin)
