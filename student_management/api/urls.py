from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    StudentListView,
    StudentDetailView,
    student_edit,
    student_create,
)

urlpatterns = [
    # Authentication URLs
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Other URLs
    path("students/", StudentListView.as_view(), name="student-list"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("students/create/", student_create, name="student-create"),
    path("students/<int:pk>/edit/", student_edit, name="student-edit"),
]
