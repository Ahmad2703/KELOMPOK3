from django.contrib import admin
from .models import UserProfileInfo
from .models import Course

# Register your models here.
admin.site.register(UserProfileInfo)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'schedule')
    list_filter = ('teacher',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = UserProfileInfo.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
