from django.shortcuts import render,redirect
from .forms import RegisterForm,PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, 'create complete your account please wait for admin approve and send')
            
    else:
        register_form = RegisterForm()

    return render(request, 'register.html', {
        'form': register_form,
    })


# class EmailVerificationView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None

#         if user and default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.success(request, 'Email verification successful. You can now log in.')
#         else:
#             messages.error(request, 'Email verification failed.')
#         return redirect('register')


class Loginview(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('dashboard')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.warning(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    
def user_logout(request):
    logout(request)
    messages.success(request,'Logged Out Successfully')
    return redirect('user_login')



def password_reset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                
             
                send_mail(
                    'Password Changed',
                    'Your password has been successfully changed.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                messages.success(request, 'Password changed successfully. Check your email.')
                return redirect('user_login')
            except User.DoesNotExist:
                messages.error(request, 'Email not found.')
    else:
        form = PasswordChangeForm()
    return render(request, 'password_resett.html', {'form': form})