from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Student


# Display a list of all students
class StudentListView(ListView):
    model = Student
    template_name = "student_list.html"
    context_object_name = "students"


# Display the details of a single student
class StudentDetailView(DetailView):
    model = Student
    template_name = "student_detail.html"
    context_object_name = "student"


# Create a new student
class StudentCreateView(CreateView):
    model = Student
    template_name = "student_create.html"
    fields = [
        "first_name",
        "last_name",
        "email",
        "date_of_birth",
        "enrollment_date",
        "grade",
    ]
    success_url = reverse_lazy("student-list")
