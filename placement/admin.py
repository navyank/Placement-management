from django.contrib import admin
from .models import Job,Company
from studentapp.models import Student
from django.contrib.auth.models import Group,User
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.
# class StudentAdmin(admin.ModelAdmin):
#     # list_display=('FullName','Address','phoneNumber','qualification','course','trainer','batch','Resume')
class CompanyAdmin(admin.ModelAdmin):
      # def get_actions(self, request):
      #   actions = super(CompanyAdmin, self).get_actions(request)
      #   del actions['delete_selected']
      #   return actions

     
      list_display=('Name','email_id','website','state','district','Phone_Number','contact_person')
class JobAdmin(admin.ModelAdmin):
      # def get_actions(self, request):
      #   actions = super(JobAdmin, self).get_actions(request)
      #   del actions['delete_selected']
      #   return actions
      list_display=('Job_title','jobcode','Vacancies','job_location','company','gender','description','Course','Salary','Last_date','apply') 
      exclude = ('jobcode',)
      def apply(self, obj):
        apply_url = reverse('admin:studentapp_jobapply_add')
        return format_html('<a class="button" href="{}?job_id={}">Apply</a>'.format(apply_url, obj.id))
    
      apply.short_description = 'Apply'
      def save_model(self, request, obj, form, change):
        if not obj.jobcode:
            # Generate jobcode based on customer name, date, and time
             date_str = obj.Last_date.strftime("%m_%d")
            #  job_title_str = obj.Job_title.replace(" ", "_")  # Replace spaces in job title with underscores
             company_str = str(obj.company).replace(" ", "_")  # Replace spaces in company name with underscores
             jobcode = f"{obj.Job_title}_{date_str}_{company_str}"
        obj.jobcode = jobcode

        super().save_model(request, obj, form, change)
        
    
       
      def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_authenticated:
            student_group = Group.objects.get(name='Student')
            user = request.user

            # Check if the user is in the Student group
            is_student = student_group in user.groups.all()

            # If the user is not in the Student group, show all jobs
            if not is_student:
                return queryset

            # If the user is in the Student group, check for verification
            student = Student.objects.filter(FullName=request.user.username).first()
            if student and student.verify:
                # Get the student's selected course
                selected_course = student.course
                student_gender = student.Gender  
                # Filter jobs based on the selected course
                queryset = queryset.filter(Course=selected_course)
                if student_gender == "male":
                    queryset = queryset.filter(gender="male")
                elif student_gender == "female":
                    queryset = queryset.filter(gender="female")
                else:
                    # If the student's gender is "others" or "both," show all jobs
                    queryset = queryset.all()
                return queryset

        return queryset.none()
                
admin.site.register(Job,JobAdmin)
admin.site.register(Company,CompanyAdmin)
