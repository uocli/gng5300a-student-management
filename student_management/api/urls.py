from django.urls import path

from .views import (
    StudentListView,
    StudentDetailView,
    student_edit,
    student_create,
)

urlpatterns = [
    path("students/", StudentListView.as_view(), name="student-list"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("students/create/", student_create, name="student-create"),
    path("students/<int:pk>/edit/", student_edit, name="student-edit"),
]
