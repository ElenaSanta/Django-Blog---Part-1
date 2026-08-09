"""Περιλαμβάνει όλα τα έτοιμα URLs του Django για Authentication:
login, logout, password_change, password_reset, κλπ.
"""

from . import views
from django.urls import path, include

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
]