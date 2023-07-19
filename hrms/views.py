from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect, resolve_url,reverse, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Employee, Department,Kin, Attendance, Recruitment, Application
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView,View,DetailView,TemplateView,ListView,UpdateView,DeleteView
from .forms import RegistrationForm, LoginForm, EmployeeForm, KinForm, DepartmentForm, AttendanceForm, \
    RecruitmentForm, ApplicationForm, UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# LEAVES
from leave.forms import LeaveCreationForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from leave.models import Leave

# Create your views here.
class Index(TemplateView):
   template_name = 'hrms/home/home.html'

#   Authentication
class Register (CreateView):
    model = User
    form_class  = RegistrationForm
    template_name = 'hrms/registrations/register.html'
    success_url = reverse_lazy('hrms:login')

# class Login_View(LoginView):
#     model = User
#     form_class = LoginForm
#     template_name = 'hrms/registrations/login.html'

# def register(request):
#     msg = None
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             msg = 'user created'
#             return redirect('hrms:login')
#         else:
#             msg = 'form is not valid'
#     else:
#         form = RegistrationForm
#     return render(request, 'hrms/registrations/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('hrms:dashboard')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error occured'
    return render(request, 'hrms/registrations/login.html', {'form': form})

def user_login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hrms:user_home')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error occured'
    return render(request, 'hrms/registrations/user_login.html', {'form': form})


def employee_login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('hrms:employee_home')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error occured'
    return render(request, 'hrms/registrations/employee_login.html', {'form': form})

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    if user.is_authenticated:
        form = UserProfile(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                user = user.save()
                return redirect('hrms:user_home')
            else:
                return redirect('hrms:user_home')
    else:
        return redirect('hrms:user_login')
    return render(request, 'hrms/user_profile.html', {'form': form})


# def user_register_view(request):
#     msg = None
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             msg = 'user created'
#             return redirect('hrms:user_login')
#         else:
#             msg = 'form is not valid'
#     else:
#         form = RegistrationForm
#     return render(request, 'hrms/registrations/user_register.html', {'form': form})


class User_Register(CreateView):
    model = User
    form_class  = RegistrationForm
    template_name = 'hrms/registrations/user_register.html'
    success_url = reverse_lazy('hrms:user_login')

class User_page(TemplateView):
   template_name = 'hrms/user/home.html'


class Employee_page(TemplateView):
   template_name = 'hrms/employee/index.html'

class Logout_View(View):
    def get(self,request):
        logout(self.request)
        return redirect ('hrms:login',permanent=True)

class User_Logout_View(View):
    def get(self,request):
        logout(self.request)
        return redirect ('hrms:user_login',permanent=True)


class Employee_Logout_View(View):
    def get(self,request):
        logout(self.request)
        return redirect ('hrms:employee_login',permanent=True)
    
    
 # Main Board   
class Dashboard(LoginRequiredMixin,ListView):
    template_name = 'hrms/dashboard/index.html'
    login_url = 'hrms:login'
    model = get_user_model()
    context_object_name = 'qset'            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['emp_total'] = Employee.objects.all().count()
        context['dept_total'] = Department.objects.all().count()
        context['admin_count'] = self.model.objects.all().count()
        context['workers'] = Employee.objects.order_by('-id')
        return context

# Employee's Controller
class Employee_New(LoginRequiredMixin,CreateView):
    model = Employee  
    form_class = EmployeeForm  
    template_name = 'hrms/employee/create.html'
    login_url = 'hrms:login'
    redirect_field_name = 'redirect:'
    
    
class Employee_All(LoginRequiredMixin,ListView):
    template_name = 'hrms/employee/index.html'
    model = Employee
    login_url = 'hrms:login'
    context_object_name = 'employees'
    paginate_by  = 5
    
class Employee_View(LoginRequiredMixin,DetailView):
    queryset = Employee.objects.select_related('department')
    template_name = 'hrms/employee/single.html'
    context_object_name = 'employee'
    login_url = 'hrms:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            query = Kin.objects.get(employee=self.object.pk)
            context["kin"] = query
            return context
        except ObjectDoesNotExist:
            return context
        
class Employee_Update(LoginRequiredMixin,UpdateView):
    model = Employee
    template_name = 'hrms/employee/edit.html'
    form_class = EmployeeForm
    login_url = 'hrms:login'
    
    
class Employee_Delete(LoginRequiredMixin,DeleteView):
    pass

class Employee_Kin_Add (LoginRequiredMixin,CreateView):
    model = Kin
    form_class = KinForm
    template_name = 'hrms/employee/kin_add.html'
    login_url = 'hrms:login'
   

    def get_context_data(self):
        context = super().get_context_data()
        if 'id' in self.kwargs:
            emp = Employee.objects.get(pk=self.kwargs['id'])
            context['emp'] = emp
            return context
        else:
            return context

class Employee_Kin_Update(LoginRequiredMixin,UpdateView):
    model = Kin
    form_class = KinForm
    template_name = 'hrms/employee/kin_update.html'
    login_url = 'hrms:login'

    def get_initial(self):
        initial = super(Employee_Kin_Update,self).get_initial()
        
        if 'id' in self.kwargs:
            emp =  Employee.objects.get(pk=self.kwargs['id'])
            initial['employee'] = emp.pk
            
            return initial

#Department views

class Department_Detail(LoginRequiredMixin, ListView):
    context_object_name = 'employees'
    template_name = 'hrms/department/single.html'
    login_url = 'hrms:login'
    def get_queryset(self): 
        queryset = Employee.objects.filter(department=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dept"] = Department.objects.get(pk=self.kwargs['pk']) 
        return context
    
class Department_New (LoginRequiredMixin,CreateView):
    model = Department
    template_name = 'hrms/department/create.html'
    form_class = DepartmentForm
    login_url = 'hrms:login'

class Department_Update(LoginRequiredMixin,UpdateView):
    model = Department
    template_name = 'hrms/department/edit.html'
    form_class = DepartmentForm
    login_url = 'hrms:login'
    success_url = reverse_lazy('hrms:dashboard')

#Attendance View

class Attendance_New (LoginRequiredMixin,CreateView):
    model = Attendance
    form_class = AttendanceForm
    login_url = 'hrms:login'
    template_name = 'hrms/attendance/create.html'
    success_url = reverse_lazy('hrms:attendance_new')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.localdate()
        pstaff = Attendance.objects.filter(Q(status='PRESENT') & Q (date=timezone.localdate())) 
        context['present_staffers'] = pstaff
        return context

class Attendance_Out(LoginRequiredMixin,View):
    login_url = 'hrms:login'

    def get(self, request,*args, **kwargs):

       user=Attendance.objects.get(Q(staff__id=self.kwargs['pk']) & Q(status='PRESENT')& Q(date=timezone.localdate()))
       user.last_out=timezone.localtime()
       user.save()
       return redirect('hrms:attendance_new')   

# class LeaveNew (LoginRequiredMixin,CreateView, ListView):
#     model = Leave
#     template_name = 'hrms/leave/create.html'
#     form_class = LeaveForm
#     login_url = 'hrms:login'
#     success_url = reverse_lazy('hrms:leave_new')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["leaves"] = Leave.objects.all()
#         return context

class Payroll(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'hrms/payroll/index.html'
    login_url = 'hrms:login'
    context_object_name = 'stfpay'



class ApplicationView(CreateView):
    model = Application
    template_name = 'hrms/recruitment/index.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('hrms:index')

class Applicants(ListView):
    model = Application
    form = ApplicationForm
    login_url = 'hrms:login'
    template_name = 'hrms/recruitment/applicants.html'
    context_object_name = 'applicants'


def accept_application(request, pk):
    if request.user.is_authenticated:
        applicant = Application.objects.get(pk=pk)
        # form.save((applicant.first_name, applicant.last_name, applicant.position, applicant.email, applicant.phone))
        return render(request, 'hrms/recruitment/check.html', {'applicant':applicant})
    else:
        return redirect('hrms:admin-login')

# class AcceptApplication(LoginRequiredMixin, View):
#     login_url = 'hrms:login'
#     model = Recruitment
#     template_name = 'hrms/recruitment/check.html'
#     def get(self,request, pk):
#         applicant = Application.objects.get(id=pk)
#         form = RecruitmentForm(request.POST or None, instance=applicant)
#         if form.is_valid():
#             form.save()
#             return redirect('hrms:recruitmentall')


class RecruitmentAll(LoginRequiredMixin,ListView):
    model = Recruitment
    login_url = 'hrms:login'
    template_name = 'hrms/recruitment/all.html'
    context_object_name = 'recruit'

class RecruitmentDelete (LoginRequiredMixin,View):
    login_url = 'hrms:login'
    def get (self, request,pk):
     form_app = Application.objects.get(pk=pk)
     form_app.delete()
     return redirect('hrms:recruitmentall', permanent=True)

class Pay(LoginRequiredMixin,ListView):
    model = Employee
    template_name = 'hrms/payroll/index.html'
    context_object_name = 'emps'
    login_url = 'hrms:login'




def leave_creation(request):
    if not request.user.is_authenticated:
        return redirect('hrms:login')
    if request.method == 'POST':
        form = LeaveCreationForm(data = request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            user = request.user
            instance.user = user
            instance.save()


            # print(instance.defaultdays)
            messages.success(request,'Leave Request Sent,wait for Human Resource Managers response',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('hrms:createleave')

        messages.error(request,'failed to Request a Leave,please check entry dates',extra_tags = 'alert alert-warning alert-dismissible show')
        return redirect('hrms:createleave')

    dataset = dict()
    form = LeaveCreationForm()
    dataset['form'] = form
    dataset['title'] = 'Apply for Leave'
    return render(request,'hrms/user/create_leave.html',dataset)
    # return HttpResponse('leave creation form')



# def leave_creation(request):


# 	if request.method == 'POST':
# 		form = LeaveCreationForm(data = request.POST)
# 		cform = CommentForm(data = request.POST)
# 		if form.is_valid() and cform.is_valid():
# 			instance = form.save(commit = False)
# 			user = request.user
# 			instance.user = user
# 			instance.save()
# 			print(instance)

# 			# Commment form save  logic
# 			comment_inst = cform.save(commit = False)
# 			# comment_inst.leave = instance
# 			# comment_inst.comment = request.POST['comment']
# 			cinstance.save()

# 			return HttpResponse('success')

# 		else:
# 			return HttpResponse('error')


# 	dataset = dict()

# 	form = LeaveCreationForm()
# 	cform = CommentForm()
# 	dataset['form'] = form
# 	dataset['cform'] = cform
# 	return render(request,'dashboard/create_leave.html',dataset)





def leaves_list(request):
    if not (request.user.is_staff and request.user.is_superuser):
        return redirect('hrms:login')
    leaves = Leave.objects.all_pending_leaves()
    return render(request,'hrms/dashboard/leaves_recent.html',{'leave_list':leaves,'title':'leaves list - pending'})



def leaves_approved_list(request):
    if not (request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    leaves = Leave.objects.all_approved_leaves() #approved leaves -> calling model manager method
    return render(request,'hrms/dashboard/leaves_approved.html',{'leave_list':leaves,'title':'approved leave list'})



def leaves_view(request,id):
    if not (request.user.is_authenticated):
        return redirect('/')

    leave = get_object_or_404(Leave, id = id)
    employee = Employee.objects.filter(first_name = leave.user)[0]
    # employee = User.objects.get(id=id)
    print(employee)
    return render(request,'hrms/dashboard/leave_detail_view.html',{'leave':leave,'employee':employee,'title':'{0}-{1} leave'.format(leave.user.username,leave.status)})


def approve_leave(request,id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    user = leave.user
    employee = Employee.objects.filter(first_name = user)[0]
    # employee = User.objects.get(id=id)
    leave.approve_leave

    messages.error(request,'Leave successfully approved for {0}'.format(employee.username),extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('hrms:userleaveview', id = id)


def cancel_leaves_list(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leaves = Leave.objects.all_cancel_leaves
    return render(request,'hrms/dashboard/leaves_cancel.html',{'leave_list_cancel':leaves,'title':'Cancel leave list'})



def unapprove_leave(request,id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    leave.unapprove_leave()
    return redirect('hrms:leaveslist') #redirect to unapproved list


def cancel_leave(request,id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    leave.leaves_cancel

    messages.success(request,'Leave is canceled',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('hrms:cancelleaveslist')#work on redirecting to instance leave - detail view


# Current section -> here
def uncancel_leave(request,id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request,'Leave is uncanceled,now in pending list',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('hrms:cancelleaveslist')#work on redirecting to instance leave - detail view



def leave_rejected_list(request):

    dataset = dict()
    leave = Leave.objects.all_rejected_leaves()

    dataset['leave_list_rejected'] = leave
    return render(request,'hrms/dashboard/rejected_leaves_list.html',dataset)



def reject_leave(request,id):
    dataset = dict()
    leave = get_object_or_404(Leave, id = id)
    leave.reject_leave
    messages.success(request,'Leave is rejected',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('hrms:leavesrejected')

    # return HttpResponse(id)


def unreject_leave(request,id):
    leave = get_object_or_404(Leave, id = id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request,'Leave is now in pending list ',extra_tags = 'alert alert-success alert-dismissible show')

    return redirect('hrms:leavesrejected')



# Rabotec staffs leaves table user only
def view_my_leave_table(request):
    # work on the logics
    if request.user.is_authenticated:
        user = request.user
        leaves = Leave.objects.filter(user = user)
        employee = Employee.objects.filter(first_name = user).first()
        print(leaves)
        dataset = dict()
        dataset['leave_list'] = leaves
        dataset['employee'] = employee
        dataset['title'] = 'Leaves List'
    else:
        return redirect('hrms:login')
    return render(request,'hrms/dashboard/staff_leaves_table.html',dataset)


def view_test(request):
    return render(request, 'hrms/dashboard/dashboard_index.html', {})
