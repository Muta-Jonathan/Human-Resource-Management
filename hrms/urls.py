from django.urls import path
from . import views
app_name = 'hrms'
urlpatterns = [

# Authentication Routes
    path('', views.Index.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='reg'),
    # path('login/', views.Login_View.as_view(), name='login'),
    # path('admin-register/', views.register, name='reg'),
    path('admin-login/', views.login_view, name='login'),
    path('login/', views.user_login_view, name='user_login'),
    path('employee_login/', views.employee_login_view, name='employee_login'),
    # path('signup/', views.user_register_view, name='user_reg'),
    path('signup/', views.User_Register.as_view(), name='user_reg'),
    path('logout/', views.Logout_View.as_view(), name='logout'),
    path('user_logout/', views.User_Logout_View.as_view(), name='user_logout'),
    path('employee_logout/', views.Employee_Logout_View.as_view(), name='employee_logout'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('user-page/', views.User_page.as_view(), name='user_home'),
    path('employee-page/', views.Employee_page.as_view(), name='employee_home'),

#     test
    path('userprofile/<int:pk>/', views.user_profile, name='updateprofile'),


# Employee Routes
    path('dashboard/employee/', views.Employee_All.as_view(), name='employee_all'),
    path('dashboard/employee/new/', views.Employee_New.as_view(), name='employee_new'),
    path('dashboard/employee/<int:pk>/view/', views.Employee_View.as_view(), name='employee_view'),
    path('dashboard/employee/<int:pk>/update/', views.Employee_Update.as_view(), name='employee_update'),
    path('dashboard/employee/<int:pk>/delete/', views.Employee_Delete.as_view(), name='employee_delete'),
    path('dashboard/employee/<int:id>/kin/add/', views.Employee_Kin_Add.as_view(), name='kin_add'),
    path('dashboard/employee/<int:id>/kin/<int:pk>/update/', views.Employee_Kin_Update.as_view(), name='kin_update'),

#Department Routes
    path('dashboard/department/<int:pk>/', views.Department_Detail.as_view(), name='dept_detail'),
    path('dashboard/department/add/', views.Department_New.as_view(), name='dept_new'),
    path('dashboard/department/<int:pk>/update/', views.Department_Update.as_view(), name='dept_update'),

#Attendance Routes
    path('dashboard/attendance/in/', views.Attendance_New.as_view(), name='attendance_new'),
    path('dashboard/attendance/<int:pk>/out/', views.Attendance_Out.as_view(), name='attendance_out'),

#Leave Routes

    # path("dashboard/leave/new/", views.LeaveNew.as_view(), name="leave_new"),
    path('leave/apply/',views.leave_creation,name='createleave'),
    path('leaves/pending/all/',views.leaves_list,name='leaveslist'),
    path('leaves/approved/all/',views.leaves_approved_list,name='approvedleaveslist'),
    path('leaves/cancel/all/',views.cancel_leaves_list,name='cancelleaveslist'),
    path('leaves/all/view/<int:id>/',views.leaves_view,name='userleaveview'),
    path('leaves/view/table/',views.view_my_leave_table,name='staffleavetable'),
    path('leave/approve/<int:id>/',views.approve_leave,name='userleaveapprove'),
    path('leave/unapprove/<int:id>/',views.unapprove_leave,name='userleaveunapprove'),
    path('leave/cancel/<int:id>/',views.cancel_leave,name='userleavecancel'),
    path('leave/uncancel/<int:id>/',views.uncancel_leave,name='userleaveuncancel'),
    path('leaves/rejected/all/',views.leave_rejected_list,name='leavesrejected'),
    path('leave/reject/<int:id>/',views.reject_leave,name='reject'),
    path('leave/unreject/<int:id>/',views.unreject_leave,name='unreject'),

#Recruitment

    path("application/",views.ApplicationView.as_view(), name="application"),
    path("application/<int:pk>/accept",views.accept_application, name="application_accept"),
    path("applicants/",views.Applicants.as_view(), name="applicants"),
    path("recruitment/all/",views.RecruitmentAll.as_view(), name="recruitmentall"),
    path("recruitment/<int:pk>/delete/", views.RecruitmentDelete.as_view(), name="recruitmentdelete"),
    # path("applicant/<int:pk>/view/", views.view_applicant, name='view_applicant'),

#Payroll
    path("employee/pay/",views.Pay.as_view(), name="payroll")

]