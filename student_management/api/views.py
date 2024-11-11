from django.shortcuts import render, get_object_or_404, redirect
from .forms import StudentForm
from django.views.generic import ListView, DetailView
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


# View to create a new student
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
        else:
            # If the form is not valid, it will contain errors
            print(form.errors)
    else:
        form = StudentForm()

    return render(request, "student_create.html", {"form": form})


# View to edit an existing student
def student_edit(request, pk):
    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student-list")
        else:
            print(form.errors)
    else:
        form = StudentForm(instance=student)

    return render(request, "student_edit.html", {"form": form})
