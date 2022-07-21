import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from accounts.forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, EditProfileForm
from accounts.models import OtpCode, User
from utils import send_otp_code
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'full_name': form.cleaned_data['full_name'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'we send code to your phone number', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegistrationCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_session = request.session['user_registration_info']
            code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
            if form.cleaned_data['code'] == code_instance.code:
                if not code_instance.created_time.minute + 2 >= datetime.datetime.now().minute:
                    User.objects.create_user(phone_number=user_session['phone_number'],
                                             email=user_session['email'],
                                             full_name=user_session['full_name'],
                                             password=user_session['password'])
                    code_instance.delete()
                    messages.success(request, 'you register successfully', 'success')
                    return redirect('home:home')
            else:
                messages.error(request, 'this code is wrong ', 'danger')
                return redirect('accounts:verify_code')
            messages.error(request, 'this code is expired ', 'danger')
            code_instance.delete()
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'you login successfully', 'success')
                    return redirect('home:home')

            except User.DoesNotExist:
                messages.error(request, 'User Not Exit', 'danger')
                return redirect('accounts:user_login')

        messages.error(request, 'invalid input', 'danger')
        return redirect('accounts:user_login')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logout successfully', 'success')
        return redirect('home:home')


class EditProfileView(LoginRequiredMixin, View):
    form_class = EditProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        user = self.request.user
        return render(request, 'accounts/edit_profile.html', {'form': form, 'user': user})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'your profile edit successfully', 'success')
            return redirect('homa:home')




