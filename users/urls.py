from django.urls import path,include
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('profile/<int:pk>/',ProfileView.as_view()),
    path('account/',include('django.contrib.auth.urls')),
]
