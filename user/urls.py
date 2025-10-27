from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    # path('email_verification/<str:uidb64>/<str:token>/', views.EmailVerificationView.as_view(), name='email_verification'),
    path('login/',views.Loginview.as_view(),name = 'user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
]
