from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import StudentForm
from django.views.generic import ListView, DetailView
from .models import Student
from django.db.models import Q


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
@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student-list")
        else:
            # If the form is not valid, it will contain errors
            print(form.errors)
    else:
        form = StudentForm()

    return render(request, "student_create.html", {"form": form})


# View to edit an existing student
@login_required
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


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.delete()
        return redirect("student-list")

    return render(request, "student_delete_confirm.html", {"student": student})


def student_list(request):
    query = request.GET.get("q", "")  # Get the search query from the GET request
    students = Student.objects.all()  # Start with all students

    if query:
        # Filter students by first name or last name (case-insensitive)
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )

    return render(request, "student_list.html", {"students": students, "query": query})
