from django.urls import path
from .views import SignUp, UserProfile

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('<int:pk>', UserProfile.as_view(), name='profile'),
]