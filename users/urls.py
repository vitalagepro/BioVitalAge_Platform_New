"""
Url users mapping configuration
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginTokenView


urlpatterns = [
    path('token/', LoginTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
