from django.urls import path
from myapp import views
urlpatterns = [
    path('',views.loginpage,name='loginpage'),
    path('login/',views.loginpage,name='loginpage'),
    path('home/',views.home,name='home'),
    path('add_employee/',views.add_employee,name='add_employee'),
    path('employee_list/',views.employee_list,name='employee_list'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logoutpage,name='logoutpage'),
    path('edit/<int:id>',views.edit, name="edit"),
    path('save_edit/<int:id>',views.save_edit, name="save_edit"),
    path('delete/<int:id>',views.delete_employee, name="delete"),
    path('editprofile/<int:id>',views.editprofile, name="editprofile"),
    path('save_profile/<int:id>',views.save_profile, name="save_profile"),
]