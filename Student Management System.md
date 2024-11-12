

# Student Management System



[TOC]



## Project Setup

### Install Django

Ensure that you have **Python** installed. Open your terminal or command prompt and install Django using pip.

```bash
pip install django
```

### Create a Django Project

Initialize a new Django project:

```bash
django-admin startproject student_management
```

Navigate to the project directory:

```bash
cd student_management
```

### Create a Django App

Create an app **api** within the project:

```bash
django-admin startapp api
```

Add the app to your INSTALLED_APPS in student_management/settings.py:

```python
INSTALLED_APPS = [
    # Default apps...
    "api.apps.ApiConfig",
]
```



## Implementing Key Features

### Models

Create models in students/models.py to define database tables. Here’s an example model for a simple student management system:

```python
from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField()
    grade = models.IntegerField()
```

Run migrations to create the table:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Views

In api/views.py, create views for CRUD operations (Create, Read, Update, Delete) to manage student records.

```python
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
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
    query = request.GET.get("q", "")  # Get the search query from the GET request
    students = Student.objects.all()  # Start with all students

    if query:
        # Filter students by first name or last name (case-insensitive)
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    paginator = Paginator(students, 5)
    page_number = request.GET.get("page")
    pagination = paginator.get_page(page_number)

    return render(
        request, "student_list.html", {"pagination": pagination, "query": query}
    )
```

### Templates

In the api/templates/ folder, create base.html, student_create.html, student_delete_confirm.html, student_detail.html, student_edit.html and student_list.html.

#### base.html

The base.html provides a unified layout across the system.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- ... -->
</head>
<body>

<header>
    <nav>
        <ul>
            <li><a href="{% url 'student-list' %}" class="app-name">Student Management App</a></li>
            {% if user.is_authenticated %}
                <li><a href="{% url 'logout' %}">Logout</a></li>
            {% else %}
                <li><a href="{% url 'login' %}">Login</a></li>
            {% endif %}
        </ul>
    </nav>
</header>

<div class="container">
    {% block content %}
    {% endblock %}
</div>

<footer class="centered-content">
    <p>&copy; 2024 Student Management App</p>
</footer>

</body>
</html>
```

#### student_create.html and student_edit.html

The two pages employ the same form element which reflects the backend form.py.

student_create.html

```html
{% extends 'base.html' %}
{% block title %}Create Student{% endblock %}

{% block content %}
    <h4>Create Student</h4>
    <a class="material-button" href="{% url 'student-list' %}">Back to Student List</a>
    <form method="post">
        {% csrf_token %}
        {{ form.as_div }}
        <button class="material-button material-button-error" type="submit">Create</button>
    </form>
{% endblock %}
```



student_edit.html

```html
{% extends 'base.html' %}

{% block title %}Edit Student{% endblock %}

{% block content %}
    <h4>Edit Student</h4>
    <a class="material-button" href="{% url 'student-list' %}">Back to Student List</a>
    <form method="post">
        {% csrf_token %}
        {{ form.as_div }}
        <button class="material-button material-button-error" type="submit">Update</button>
    </form>
{% endblock %}
```



api/forms.py

To display the **Date of Birth** and **Enrollment Date** fields on the form, **widgets** is added to indicate the field type. Also, some validation on **Email** and **Grade** has been implemented.

```python
from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "enrollment_date",
            "grade",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "enrollment_date": forms.DateInput(attrs={"type": "date"}),
        }

    # Custom validation for the email field
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required.")
        return email

    # Custom validation for grade to be between 1 and 12
    def clean_grade(self):
        grade = self.cleaned_data.get("grade")
        if grade < 1 or grade > 12:
            raise forms.ValidationError("Grade must be between 1 and 12.")
        return grade

```

### Authentication

The end users are required to login to the system to take actions which are related to database manipulation: Create, Update or Delete.

![login](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/URUHCs.png)

You can also log yourself out by clicking on the Logout button.

![Logout](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/hzm8jj.png)

### Admin Panel

The student model has been registered on the Admin Panel, so the admins can manage the students there through http://127.0.0.1:8000/admin/.

![Admin](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/5eYWUI.png)



## UI Enhancement

To have a user-friendly interface, [Google Fonts](https://fonts.google.com/) and [Material UI](https://mui.com/) have been introduced.

base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- ... -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <!-- ... -->
</head>
<body>
<!-- ... -->
</body>
</html>
```



## Testing the Application

Run the Django development server to test your application:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ to access the app.

![server](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/u2B8dB.png)

### Student List

Student List in this app is the default page. The list has been equipped with pagination and searching functions.

### Pagination

5 students are displayed in one page by default. PAGE_SIZE in environment variables can be configured to change the number.

![student list](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/IbjKlp.png)

### Searching

Searching has been added to the top of the list, where students can be filtered by their names.

![searching](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/aluY9O.png)

### Student Creation and Update

The two pages utilize the same form element where all available fields are configured from the backend `api/forms.py`.



#### Creation

The **Add New Student** button is available on the Student List form.

![Add](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/7Xw0tm.png)

The form has a button which lets users go back to the student list.

![AddForm](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/Eza5Or.png)

#### Update

To update a student, the end users have to View the student first. In the student detail page, options are available for editing a student or going back to the student list.

![View](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/69nch7.png)

![Detail](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/R8IIvO.png)

![Update](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/GXpAkc.png)

### Student Deletion

The **Delete** action is also available on the student list. As deletion is a dangerous action, there is a confirmation page following. After confirmation, the record will be removed from the database and the user will be redirected to the home page where all rest students are displayed.

![DeleteAction](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/JrErp1.png)

![Deletion](https://cdn.jsdelivr.net/gh/uocli/img@main/2024-11-12/LIfMX8.png)

