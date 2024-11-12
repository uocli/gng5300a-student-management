from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .forms import StudentForm
from django.views.generic import ListView, DetailView
from .models import Student
from django.db.models import Q


class StudentDetailView(DetailView):
    """
    This view will display the details of a single student.
    """
    model = Student
    template_name = "student_detail.html"
    context_object_name = "student"


@login_required
def student_create(request):
    """
    This view will handle the creation of a new student.
    """
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


@login_required
def student_edit(request, pk):
    """
    This view will handle the editing of an existing student.
    """
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
    """
    This view will handle the deletion of a student.
    """
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.delete()
        return redirect("student-list")

    return render(request, "student_delete_confirm.html", {"student": student})


def student_list(request):
    """
    This view will display a list of all students.
    """
    query = request.GET.get("q", "")
    students = Student.objects.all().order_by('id')

    if query:
        # Filter students by first name or last name (case-insensitive)
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).order_by('id')
    paginator = Paginator(students, settings.PAGE_SIZE)
    page_number = request.GET.get("page")
    pagination = paginator.get_page(page_number)

    return render(
        request, "student_list.html", {"pagination": pagination, "query": query}
    )
