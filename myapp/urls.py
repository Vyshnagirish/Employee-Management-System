from django.urls import path
from myapp import views
urlpatterns = [
    path('',views.base,name='base'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
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
    path('sendmessageemp/',views.sendmessage, {'emp_type':'emp'}, name="sendmessageemp"),
    path('sendmessagehr/',views.sendmessage, {'emp_type':'hr'}, name="sendmessagehr"),
    path('outbox/',views.outbox, name="outbox"),
    path('inbox/',views.inbox, name="inbox"),
    path('openinboxmessage/<int:id>',views.openmessage, {'message_type':'inbox'}, name="openinboxmessage"),
    path('openoutboxmessage/<int:id>',views.openmessage, {'message_type':'outbox'}, name="openoutboxmessage"),
    path('reply/<int:id>',views.reply, name="reply"),
    path('sendreply/',views.sendreply, name="sendreply"),
    path('deleteinboxmessage/<int:id>/', views.delete_message, {'target': 'inbox'}, name='deleteinboxmessage'),
    path('deleteoutboxmessage/<int:id>', views.delete_message, {'target': 'outbox'}, name='deleteoutboxmessage'),
    path('changepassword/<int:id>', views.changepassword, name='changepassword'),
]