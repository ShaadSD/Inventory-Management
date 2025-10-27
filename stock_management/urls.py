from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('product/', include('product.urls')),
    path('', lambda request: redirect('user_login')),
]