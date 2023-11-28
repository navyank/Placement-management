from django.contrib import admin
from .models import Course,District,State,Qualification,Trainer,Batch

# Register your models here.

class TrainerAdmin(admin.ModelAdmin):
    filter_horizontal=('trainer',)
class BatchAdmin(admin.ModelAdmin):
    list_display=('course','Startdate','Enddate','Time','batch')  
    exclude=('batch',) 
    def save_model(self, request, obj, form, change):
        if not obj.batch:
             sdate_str = obj.Startdate.strftime("%m_%d")
             ldate_str=obj.Startdate.strftime("%m_%d")
             time_str = obj.Time.strftime("%H_%M")
             batch= f"{obj.course}_{sdate_str}_{time_str}_{ldate_str}"
        obj.batch = batch

        super().save_model(request, obj, form, change) 
admin.site.register(Course)
admin.site.register(District)
admin.site.register(State)
admin.site.register(Trainer,TrainerAdmin)
admin.site.register(Qualification)
admin.site.register(Batch,BatchAdmin)