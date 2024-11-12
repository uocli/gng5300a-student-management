# Student Management

## Description

This is a student management system that allows you to add, delete, update and view students. This project is part of the requirements of the course GNG5300[A].

## Installation

```shell
git clone https://github.com/uocli/gng5300a-student-management.git
cd gng5300a-student-management
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd student_management
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
