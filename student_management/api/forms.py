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
