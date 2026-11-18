from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.AssetTrackLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_redirect, name="dashboard_redirect"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/employee/", views.employee_dashboard, name="employee_dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
    path("company/", views.company_manage_view, name="company_manage"),
    path("company/regenerate-code/", views.company_regenerate_code, name="company_regenerate_code"),
    path("company/request/<int:pk>/<str:action>/", views.company_request_review, name="company_request_review"),
    path("company/add-member/", views.company_add_member, name="company_add_member"),
    path("company/remove-member/<int:pk>/", views.company_remove_member, name="company_remove_member"),
    path("company/join/", views.employee_join_company, name="employee_join_company"),
    path("company/leave/", views.employee_leave_company, name="employee_leave_company"),
]
