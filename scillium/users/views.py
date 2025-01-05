from django.views.generic.edit import CreateView, FormView
from .forms import UserCreationForm, UserChangeForm
from ui_elements.views import render_nav, def_config, render_footer
from .forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.http import JsonResponse
from order.models import Order, OrderItem
from .models import User
import json
import re

def validate_password(password):
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')

    if password.islower():
        raise ValidationError('Password must contain at least one uppercase letter.')

    if password.isupper():
        raise ValidationError('Password must contain at least one lowercase letter.')

    if not re.search(r'\d', password
    ):
        raise ValidationError('Password must contain at least one number.')
    
    if not re.search(r'\W', password):
        raise ValidationError('Password must contain at least one special character.')


    return password
    

# Possible errors
errors = {
    'singed_in': JsonResponse({'status': 'success', 'message': 'User is already logged in.'}),
    'no_username': JsonResponse({'status': 'error', 'message': 'Username is required.'}),
    'no_email': JsonResponse({'status': 'error', 'message': 'Email is required.'}),

    'username_email_not_found': JsonResponse({'status': 'error', 'message': 'Username or Email not found.'}),

    'no_password': JsonResponse({'status': 'error', 'message': 'Password is required.'}),
    'invalid_password': JsonResponse({'status': 'error', 'message': 'Password is invalid.'}),
    'no_confirm_password': JsonResponse({'status': 'error', 'message': 'Confirm Password is required.'}),
    'password_not_strong_enough': JsonResponse({'status': 'error', 'message': 'Password is not strong enough.'}),

    'email_already_exists': JsonResponse({'status': 'error', 'message': 'Email already exists.'}),
    'username_already_exists': JsonResponse({'status': 'error', 'message': 'Username already exists.'}),

    'invalid_details': JsonResponse({'status': 'error', 'message': 'Invalid username or password.'}),

    'missing_old_password': JsonResponse({'status': 'error', 'message': 'Old password is required.'}),
    'missing_new_password': JsonResponse({'status': 'error', 'message': 'New password is required.'}),
    'missing_confirm_password': JsonResponse({'status': 'error', 'message': 'Confirm password is required.'}),
    'passwords_do_not_match': JsonResponse({'status': 'error', 'message': 'Passwords do not match.'}),
}

# 
# This function is used check if the user is already logged in
# than redirect them to the account detail page, otherwise
# render the template provided.
# 
def redirect_if_logged_in(self, request):
    # Check if the user is logged in
    if request.user.is_authenticated:
        return redirect('account:detail')

    # Get the nav bar
    nav_bar = None
    footer = None
    try:
        ui_config = def_config()
        if ui_config is None: return
        nav_bar = render_nav(ui_config)
        footer = render_footer(ui_config)

    except: pass

    return render(
        request,
        self.template_name,
        {
            'nav_bar': nav_bar,
            'footer': footer,
        }
    )



# 
# This function is used to get a key from a dictionary
# if the key does not exist, return None
# 
def get_key_or_none(object, key):
    try: return object[key]
    except: return None



class LoginView(FormView):
    form_class = UserCreationForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('account:detail')

    def post(self, request, *args, **kwargs):
        # Get the data
        data = json.loads(request.body)
        eou = get_key_or_none(data, 'emailorusername')
        password = get_key_or_none(data, 'password')


        # Return any errors if theres any issues
        if request.user.is_authenticated: return errors['singed_in']
        if eou is None: return errors['username_email_not_found']
        if password is None: errors['no_password']



        # Check if the user has provided an email or a username
        is_email = False

        # Check if the email is valid
        try: validate_email(eou)
        except ValidationError: pass

                

        # Get the user
        user = None

        # Since the user can provide either an email or a username
        # we need to check if the user has provided an email or a username
        # and then get the user based on that
        if is_email:
            try: user = User.objects.get(email=eou)
            except User.DoesNotExist: return errors['invalid_details']
        else:
            try: user = User.objects.get(username=eou)
            except User.DoesNotExist: return errors['invalid_details']

        
        
        # Check if the password is correct
        if not user.check_password(password): return errors['invalid_details']


        # Log the user in
        login(request, user)
        return JsonResponse({
            'status': 'success', 
            'message': 'User logged in successfully.'
        })
        
    
    def get(self, request, *args, **kwargs):
        return redirect_if_logged_in(self, request)
        


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'account/register.html'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        username         = get_key_or_none(data, 'username')
        email            = get_key_or_none(data, 'email')
        password         = get_key_or_none(data, 'password')
        confirm_password = get_key_or_none(data, 'password2')


        # Check if all the required fields are provided
        if request.user.is_authenticated: return errors['singed_in']
        if username is None: return errors['no_username']
        if email is None: return errors['no_email']


        # Password validation
        if password is None: return errors['no_password']
        if confirm_password is None: return errors['no_confirm_password']
        if password != confirm_password: return errors['passwords_do_not_match']

        try: validate_password(password)
        except ValidationError: return errors['password_not_strong_enough']

        # Check if the user already exists
        if User.objects.filter(username=username).exists(): return errors['username_already_exists']
        if User.objects.filter(email=email).exists(): return errors['email_already_exists']



        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )


        # Add the user to the default group
        try:
            default_group = Group.objects.get(name='default')
            user.groups.add(default_group)
        except: pass


        # Log the user in
        login(request, user)


        return JsonResponse({
            'status': 'success', 
            'message': 'User created',
            'redirect': reverse_lazy('account:detail')
        })
        
        
    def get(self, request, *args, **kwargs):
        return redirect_if_logged_in(self, request)
        



class DetailView(FormView):
    form_class = UserChangeForm
    template_name = 'account/detail.html'
    success_url = reverse_lazy('account:detail')


    def get(self, request, *args, **kwargs):
        # Check if the user is logged in
        if not request.user.is_authenticated:
            return redirect('account:login')


        # Get the nav bar
        nav_bar = None
        footer = None
        try:
            ui_config = def_config()
            if ui_config is None: return
            nav_bar = render_nav(ui_config)
            footer = render_footer(ui_config)
        except: pass


        orders = None
        try: orders = Order.objects.filter(user=request.user)
        except: pass

        
        user = User.objects.get(username=request.user.username)
        form = UserChangeForm(instance=user)
        return render(
            request,
            self.template_name,
            {
                'form' : form,
                'footer': footer,
                'nav_bar': nav_bar,
                'orders': orders,
            }
        )


# 
# LOGOUT
# 
class LogoutView(FormView):
    form_class = UserCreationForm
    template_name = 'account/logout.html'
    success_url = reverse_lazy('account:detail')

    def post(self, request, *args, **kwargs):
        # De authenticate the user
        logout(request)

        # Redirect to the login page
        return redirect('account:login')


    def get(self, request, *args, **kwargs):
        # Check if the user is logged in
        if not request.user.is_authenticated:
            return redirect('account:login')

        # Get the nav bar
        nav_bar = None
        footer = None
        try:
            ui_config = def_config()
            if ui_config is None: return
            nav_bar = render_nav(ui_config)
            footer = render_footer(ui_config)
        except: pass

        return render(
            request,
            self.template_name,
            {
                'nav_bar': nav_bar,
                'footer': footer,
            }
        )



# 
# RESET
# 
class ResetView(FormView):
    form_class = UserCreationForm
    template_name = 'account/reset.html'
    success_url = reverse_lazy('account:detail')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        old_password     = get_key_or_none(data, 'old_password')
        new_password     = get_key_or_none(data, 'new_password')
        new_password2    = get_key_or_none(data, 'new_password2')


        # Check if the user is logged in
        if not request.user.is_authenticated:
            return redirect('account:login')


        # Check if all the required fields are provided
        if old_password is None: return errors['missing_old_password']
        if new_password is None: return errors['missing_new_password']
        if new_password2 is None: return errors['missing_confirm_password']
        if new_password != new_password2: return errors['passwords_do_not_match']


        # Check if the old password is correct
        if not request.user.check_password(old_password): return errors['invalid_password']


        # Check if the new password is strong enough
        try: validate_password(new_password)
        except ValidationError: return errors['password_not_strong_enough']


        # Change the password
        request.user.set_password(new_password)
        request.user.save()

        # Log the user out
        logout(request)

        # Redirect to the login page
        return JsonResponse({
            'status': 'success', 
            'message': 'Password changed'
        })


    def get(self, request, *args, **kwargs):
        # Check if the user is logged in
        if not request.user.is_authenticated:
            return redirect('account:login')

        # Get the nav bar
        nav_bar = None
        footer = None
        try:
            ui_config = def_config()
            if ui_config is None: return
            nav_bar = render_nav(ui_config)
            footer = render_footer(ui_config)
        except: pass

        return render(
            request,
            self.template_name,
            {
                'nav_bar': nav_bar,
                'footer': footer,
            }
        )


