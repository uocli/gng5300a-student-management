from django.contrib import admin
from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "enrollment_date")
    search_fields = ("name",)
    list_filter = ("grade",)


admin.site.register(Student, StudentAdmin)
