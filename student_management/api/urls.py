from django.urls import path

from .views import (
    StudentListView,
    StudentCreateView,
    StudentDetailView,
    StudentUpdateView,
)

urlpatterns = [
    path("students/", StudentListView.as_view(), name="student-list"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("students/create/", StudentCreateView.as_view(), name="student-create"),
    path("students/<int:pk>/edit/", StudentUpdateView.as_view(), name="student-edit"),
]
