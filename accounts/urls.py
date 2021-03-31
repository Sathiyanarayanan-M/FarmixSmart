from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.IndexView, name="home"),
    path("login/", views.LoginView, name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("registration/", views.RegistrationView, name="registration"),
    path("dashboard/", views.DashboardView, name="dashboard"),
    path("diseaseDetection/", views.diseaseDetection, name="diseaseDetection"),
    path("yieldPrediction/", views.yieldPrediction, name="yieldPrediction"),
    path("contact/", views.contact, name="contact"),
]
