from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from employ import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from twilio.rest import Client

# Create your views here.
def index(request):
    return render(request, 'myapp/shared/index.html')

def base(request):
    return render(request, 'myapp/shared/base.html')

def about(request):
    return render(request, 'myapp/shared/about.html')

def contact(request):
    return render(request, 'myapp/shared/contact.html')

def home(request):
    emp = request.session.get('username')
    if emp is None:
        return redirect('loginpage')
    else:
        user=User.objects.get(username=emp)
        unread_count = Messages.objects.filter(to=user, read=False).count()
        if user.employee_type == 'HR' or user.is_superuser == 1:    
            return render(request,'myapp/hrhome.html',{'emp':user,'unread_count':unread_count })
        else:
            return render(request,'myapp/home.html',{'emp':user,'unread_count':unread_count })

def loginpage(request):
    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password']
        try:
            usertable = User.objects.get(username=username1)            
            password2 = usertable.password
            if password1 == password2:                    
                if usertable.employee_type == 'HR' or usertable.is_superuser == 1:
                    request.session['username'] = usertable.username
                    return render(request, 'myapp/hr_dashboard.html',{'emp':usertable})
                else:
                    request.session['username'] = usertable.username
                    return render(request, 'myapp/employee_dashboard.html',{'emp':usertable})
            else:
                error = "Invalid Password."
                return render(request, 'myapp/loginpage.html', {'error': error})
        except ObjectDoesNotExist:
            error = "Employee not found !!"
            return render(request, 'myapp/loginpage.html', {'error': error})
    return render(request, 'myapp/loginpage.html')

def add_employee(request):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:  
        hr=User.objects.get(username=emp) #to show round profile pic of hr 
        unread_count = Messages.objects.filter(to=hr, read=False).count()     
        if request.method == 'POST':
            form = EmployeeRegistrationForm(request.POST,files=request.FILES)
            if form.is_valid():
                form.save()
                to = form.cleaned_data['email']
                usr_name = request.POST.get('name')
                passwd = request.POST.get('password')
                sendemail(to, usr_name, passwd)

                # recipient_number = request.POST.get('phone_number')
                # sendtext(recipient_number,usr_name)                

                return redirect('employee_list') 
            else:
                error = "Invalid data!!"
                return render(request, 'myapp/add_employee.html', {'data': form, 'error': error,'emp':hr,'unread_count':unread_count})
        else:
            form = EmployeeRegistrationForm()
            return render(request, 'myapp/add_employee.html', {'data': form,'emp':hr,'unread_count':unread_count})

def sendemail(to,usr_name, passwd):
    subj="Welcome to Employee Management System!!"
    msg = f"Hi {usr_name}, You're successfully registered to EMP. Your Username is <strong>'{usr_name}'</strong> and Password is <strong>'{passwd}'</strong>"
    html_message = f'<p>{msg}</p>'
    send_mail(subj, '', settings.EMAIL_HOST_USER, [to], html_message=html_message) #to addr should be given in list,else error

def employee_list(request):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    employees = User.objects.exclude(is_superuser=True)
    hr = User.objects.get(username=emp) # line added for displaying round profile pic on top
    unread_count = Messages.objects.filter(to=hr, read=False).count()
    return render(request, 'myapp/employee_list.html', {'view': employees, 'emp':hr,'unread_count':unread_count})

def edit(request,id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        x=User.objects.get(id=id) #to get id of employee whom we want to edit  & to show round prfile pic of hr
        unread_count = Messages.objects.filter(to=id, read=False).count()
        employee_code = x.employee_code
        frm=EmployeeRegistrationForm(instance=x)
        return render(request,'myapp/editemployee.html',{'edit':frm, 'id':id,'emp':x,'employee_code':employee_code,'unread_count':unread_count})
    
def save_edit(request,id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        x=User.objects.get(id=id)
        unread_count = Messages.objects.filter(to=id, read=False).count()
        if request.method == 'POST':
            name = request.POST['name']
            phone_number =  request.POST['phone_number']
            employee_type = request.POST['employee_type']
            if 'image' in request.FILES:
                profile_pic = request.FILES['image']
                x.image = profile_pic
            x.name = name
            x.phone_number = phone_number
            x.employee_type = employee_type
            x.save()
            return redirect(employee_list)
        else:
            error="Invalid data!!"
            return render(request, 'myapp/editemployee.html', {'data': emp, 'error': error,'unread_count':unread_count})

def profile(request):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage')    
    else:
        user=User.objects.get(username=emp)
        unread_count = Messages.objects.filter(to=user, read=False).count()
        if user.employee_type == 'HR' or user.is_superuser == 1:    
            return render(request,'myapp/hrprofile.html',{'emp':user,'unread_count':unread_count })
        else:
            return render(request,'myapp/profile.html',{'emp':user,'unread_count':unread_count })


def editprofile(request,id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        x=User.objects.get(id=id)
        unread_count = Messages.objects.filter(to=id, read=False).count()
        frm=EmployeeRegistrationForm(instance=x)
        if x.employee_type == 'HR' or x.is_superuser == 1:    
            return render(request,'myapp/editprofilehr.html',{'edit':frm, 'id':id,'emp':x,'unread_count':unread_count})
        else:
            return render(request,'myapp/editprofile.html',{'edit':frm, 'id':id,'emp':x,'unread_count':unread_count})

    
def save_profile(request,id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        x=User.objects.get(id=id)
        unread_count = Messages.objects.filter(to=id, read=False).count()
        if request.method == 'POST':
            name = request.POST['name']
            phone_number =  request.POST['phone_number']
            if 'image' in request.FILES:
                profile_pic = request.FILES['image']
                x.image = profile_pic
            x.name = name
            x.phone_number = phone_number
            x.save()
            return redirect(profile)
        else:
            frm=EmployeeRegistrationForm(instance=x)
            return render(request, 'myapp/editprofile.html',{'edit':frm,'unread_count':unread_count})
   
def delete_employee(request,id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        x=User.objects.get(id=id)
        x.delete()
        return redirect(employee_list)

def logoutpage(request):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        if 'username' in request.session:
            del request.session['username']

            logout(request)
            return redirect('loginpage') 
        
# def sendtext(recipient_number,usr_name):
#     wts_msg = f"Hi {usr_name}, You're successfully registered to EMP."         
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN) # Create a Twilio client                
#     # Send the text message
#     client.messages.create(
#         body=wts_msg,
#         from_='+18148023116',  # my Twilio phone number
#         to=recipient_number
# )



def sendmessage(request, emp_type):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        if emp_type == 'emp':
            template = 'myapp/sendmessageemp.html'
        else:
            template = 'myapp/sendmessagehr.html'
        pic=User.objects.get(username=emp) #to show round profile pic 
        unread_count = Messages.objects.filter(to=pic, read=False).count()
        if request.method == "POST":  
            form=MessagesForm(request.POST, files=request.FILES)
            if form.is_valid():
                messagefrom_user = User.objects.get(username=emp)
                form.instance.messagefrom = messagefrom_user
                form.save()
                return redirect('outbox')
            else:
                error = "Invalid"
                return render(request, template,{'error':error,'emp':pic,'unread_count':unread_count})
        else:
            form = MessagesForm()
            return render(request, template,{'form':form,'emp':pic,'unread_count':unread_count})

def outbox(request):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        pic=User.objects.get(username=emp) #to show round profile pic 
        myid = User.objects.get(username=emp)
        emp_type=myid.employee_type
        mymessages = Messages.objects.filter(messagefrom=myid).order_by('-send_on')
        unread_count = Messages.objects.filter(to=myid, read=False).count()
        topic = User.objects.all()
        if emp_type =='HR':
            return render(request, 'myapp/outboxhr.html',{'mymessages':mymessages,'emp':pic, 'topic':topic,'unread_count':unread_count})
        else:
            return render(request, 'myapp/outboxemp.html',{'mymessages':mymessages,'emp':pic,'topic':topic,'unread_count':unread_count})


def inbox(request):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        pic=User.objects.get(username=emp) #to show round profile pic
        myid = User.objects.get(username=emp)
        fromwhom = Messages.objects.filter(to=myid).order_by('-send_on')
        unread_count = Messages.objects.filter(to=myid, read=False).count()  #to display unread messages
        print(unread_count)
        if myid.employee_type =='HR':
            return render(request, 'myapp/inboxhr.html',{'mymessages':fromwhom,'emp':pic,'unread_count':unread_count})
        else:
            return render(request, 'myapp/inboxemp.html',{'mymessages':fromwhom,'emp':pic, 'unread_count':unread_count})

def openmessage(request,id,message_type):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        pic=User.objects.get(username=emp) #to show round profile pic
        id = Messages.objects.get(id=id) #to get id of the particular clicked message 
        unread_count = Messages.objects.filter(to=id, read=False).count()
        if message_type == 'inbox':
            id.read=True
            id.save()
            template = 'myapp/openinboxmessage.html'
        else:
            template = 'myapp/openoutboxmessage.html'
        return render(request, template, {'message':id,'emp':pic,'unread_count':unread_count})
    

def reply(request, id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        id = Messages.objects.get(id=id)
        unread_count = Messages.objects.filter(to=id, read=False).count()
        return render(request, 'myapp/reply.html', {'message':id,'unread_count':unread_count})

def sendreply(request):
    emp = request.session.get('username')
    if emp is None:  # Not logged in
        return redirect('loginpage')
    else:
        if request.method == 'POST':
            # Get the form data from the request
            message = request.POST['message']
            to = request.POST['to']  #to is a foreign key, cannot directly takethe value from post method
            to_message = User.objects.get(username=to)
            subject = request.POST['subject']
            messagefrom = User.objects.get(username=emp)

            if 'attachment' in request.FILES:
                attachment = request.FILES['attachment']
            else:
                attachment = None

            # Create a new Messages instance
            reply = Messages.objects.create(
                message=message,
                messagefrom=messagefrom,
                subject=subject,
                to=to_message,
            )

            if attachment is not None:
                reply.attachment = attachment
            reply.save()

            return redirect('inbox')

def delete_message(request, id, target):
    emp = request.session.get('username')
    if emp is None:  # Not logged in
        return redirect('loginpage')
    else:
        if target == 'inbox':
            redirect_url = 'inbox'
        elif target == 'outbox':
            redirect_url = 'outbox'
        else:
            return HttpResponse("Invalid target") 

        try:
            message = Messages.objects.get(id=id)
            message.delete()
            return redirect(redirect_url)
        except Messages.DoesNotExist:
            return HttpResponse("Message not found") 


def changepassword(request, id):
    emp = request.session.get('username')
    pic=User.objects.get(username=emp) #to show round profile pic

    if emp is None:  # Not logged in
        return redirect('loginpage')
    else:
        x=User.objects.get(id=id)
        unread_count = Messages.objects.filter(to=id, read=False).count()
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                current_password = form.cleaned_data['current_password']
                new_password = form.cleaned_data['new_password']
                confirm_password = form.cleaned_data['confirm_password']
                password_in_db = x.password
                if password_in_db == current_password:
                    if new_password == confirm_password:
                        x.password = new_password
                        x.save()
                        message_success = 'Password changed successfully !!'
                        return render(request,'myapp/profile.html',{'emp':pic, 'message_success':message_success} )
                    else:
                        messages.error(request, 'New password and confirm password do not match')
                else:
                    messages.error(request, 'Current password is incorrect !!')
            else:
                # Initialize the form if the submitted form is invalid
                form = ChangePasswordForm()
        else:
            # Initialize the form for the initial GET request
            form = ChangePasswordForm()
        if x.employee_type == 'HR':
            return render(request, 'myapp/changepasswordhr.html', {'form': form,'emp':pic,'unread_count':unread_count})
        else:
            return render(request, 'myapp/changepassword.html', {'form': form,'emp':pic,'unread_count':unread_count})
