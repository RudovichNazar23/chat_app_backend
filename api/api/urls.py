from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_profile/', include('user_profile.urls')),
    path('auth/token/pair/', TokenObtainPairView.as_view(), name='token_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
]
