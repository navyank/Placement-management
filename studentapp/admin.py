from django.contrib import admin
from .models import Student,Resume,JobApply
from django.utils.html import mark_safe,format_html
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group
from placement.models import *

class StudentAdmin(admin.ModelAdmin):
    list_display=('FullName','Gender','Address','phoneNumber','qualification','course','trainer','batch','verify_button')
    list_filter = ('verify',) 
    def verify_button(self, obj):
        button_text = "VERIFY" if not obj.verify else "UNVERIFY"
        url = reverse('admin:studentapp_student_change', args=[str(obj.id)])
        return format_html(
            '<a class="button" href="{}?verify=1">{}</a>',  # Pass verify=1 as a query parameter
            url,
            button_text
        )

    verify_button.short_description = 'Verify'

    actions = ['toggle_verify']

    def toggle_verify(self, request, queryset):
        for student in queryset:
            student.verify = True
            student.save()

    toggle_verify.short_description = "Verify Selected Students"

    def response_change(self, request, obj):
        if "_verify" in request.POST:
            obj.verify = True
            obj.save()
            self.message_user(request, "Student verified successfully.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        
        # Check if the user is in the Trainer group
        trainer_group = Group.objects.get(name='trainer')
        is_trainer = trainer_group in request.user.groups.all()

        if is_trainer:
            # If the user is in the Trainer group, filter students based on their trainer
            trainer_username = request.user.username
            return queryset.filter(trainer__trainer__username=trainer_username)
        else:
            # If the user is not in the Trainer group, show all students
            return queryset
        
        
    
class ResumeAdmin(admin.ModelAdmin):
    list_display=('FullName','email_id','download_resume_link') 
    def download_resume_link(self, obj):
        if obj.resume:
            return mark_safe(f'<a href="{obj.resume.url}" download>Download Resume</a>')
        return "No Resume"

    download_resume_link.short_description = "Resume"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_authenticated:
            student_group = Group.objects.get(name='Student')  # Change 'student' to your group name
            if student_group in request.user.groups.all():
                # For users in the 'student' group, filter based on `username == password`
                username = request.user.username
                qs = qs.filter(FullName=username)
        return qs
    
    
class JobApplyAdmin(admin.ModelAdmin):
        list_display=('FullName','Work_Experience','resume') 
admin.site.register(Student,StudentAdmin)
admin.site.register(Resume,ResumeAdmin)
admin.site.register(JobApply,JobApplyAdmin)