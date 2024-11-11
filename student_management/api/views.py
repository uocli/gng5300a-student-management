from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Student


# Display a list of all students
class StudentListView(ListView):
    model = Student
    template_name = "student_list.html"
    context_object_name = "students"

