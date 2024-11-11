from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    student_list,
    StudentDetailView,
    student_edit,
    student_create,
    delete_student,
)

urlpatterns = [
    # Authentication URLs
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Other URLs
    path("", student_list, name="student-list"),
    path("<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("create/", student_create, name="student-create"),
    path("<int:pk>/edit/", student_edit, name="student-edit"),
    path("<int:pk>/delete/", delete_student, name="student-delete"),
]
