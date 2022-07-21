from django.urls import path
from accounts.views import UserRegisterView, UserRegistrationCodeView, UserLoginView, UserLogoutView, EditProfileView

app_name = 'accounts'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('verify/', UserRegistrationCodeView.as_view(), name='verify_code'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('edit/profile/', EditProfileView.as_view(), name='edit_profile'),
]