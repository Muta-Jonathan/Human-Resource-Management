from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Employee,Department,Attendance,Kin, Recruitment, Payroll, Application




class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id','thumb','first_name','last_name','mobile','email','address','emergency','gender',
                    'department','joined','language','account_no','bank','salary')
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name','location','history')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date','first_in','last_out','status','staff')
    
class KinAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','address','occupation','mobile','employee')
    
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee','start','end','status')
    
class RecruitmentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','position','phone','email')
    
    
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee','pay_period_start','pay_period_end','gross_pay','taxes','deductions','net_pay')


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'applied_on')
# Register your models here.


# admin.site.register(User)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Kin, KinAdmin)
admin.site.register(Recruitment, RecruitmentAdmin)
# admin.site.register(Leave, LeaveAdmin)
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(Application, ApplicationAdmin)
