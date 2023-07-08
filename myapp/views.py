from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from employ import settings
from twilio.rest import Client

# Create your views here.
def home(request):
    emp = request.session.get('username')
    if emp is None:
        return redirect('loginpage')
    else:
        user=User.objects.get(username=emp)
        if user.employee_type == 'HR' or user.is_superuser == 1:    
            return render(request,'myapp/hrhome.html',{'hr':user })
        else:
            return render(request,'myapp/home.html',{'emp':user })

# def employees(request):
#     emp = request.session.get('username')
#     if emp is None:
#         return redirect('loginpage')
#     else:
#         return render(employees.html)

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
                    return render(request, 'myapp/hr_dashboard.html',{'hr':usertable})
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
        if request.method == 'POST':
            form = EmployeeRegistrationForm(request.POST,files=request.FILES)
            if form.is_valid():
                form.save()
                to = form.cleaned_data['email']
                usr_name = request.POST.get('name')
                sendemail(to,usr_name)

                # recipient_number = request.POST.get('phone_number')
                # sendtext(recipient_number,usr_name)                

                return redirect('employee_list') 
            else:
                error = "Invalid data!!"
                return render(request, 'myapp/add_employee.html', {'data': form, 'error': error,'hr':hr})
        else:
            form = EmployeeRegistrationForm()
            return render(request, 'myapp/add_employee.html', {'data': form,'hr':hr})
   
def employee_list(request):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    employees = User.objects.exclude(is_superuser=True)
    hr = User.objects.get(username=emp) # line added for displaying round profile pic on top
    return render(request, 'myapp/employee_list.html', {'view': employees, 'hr':hr})

def profile(request):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage')    
    else:
        user=User.objects.get(username=emp)
        # emp = EmployeeRegistrationForm(request.POST,files=request.FILES)
        if user.employee_type == 'HR' or user.is_superuser == 1:    
            return render(request,'myapp/hrprofile.html',{'hr':user })
        else:
            return render(request,'myapp/profile.html',{'emp':user })

def edit(request,id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        x=User.objects.get(id=id) #to get id of employee whom we want to edit
        frm=EmployeeRegistrationForm(instance=x)
        hr=User.objects.get(username=emp) #to show round prfile pic of hr
        return render(request,'myapp/editemployee.html',{'edit':frm, 'id':id,'hr':hr})
    
def save_edit(request,id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        x=User.objects.get(id=id)
        emp = EmployeeRegistrationForm(request.POST, instance=x,files=request.FILES)
        if emp.is_valid():
            emp.save()
            return redirect(employee_list)
        else:
            error="Invalid data!!"
            return render(request, 'myapp/editemployee.html', {'data': emp, 'error': error})
        
def editprofile(request,id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        x=User.objects.get(id=id)
        frm=EmployeeRegistrationForm(instance=x)
        return render(request,'myapp/editprofile.html',{'edit':frm, 'id':id,'emp':x})
    
def save_profile(request,id):
    emp = request.session.get('username')
    if emp is None:                 #not logged in  
        return redirect('loginpage') 
    else:
        x=User.objects.get(id=id)
        emp = EmployeeRegistrationForm(request.POST, instance=x,files=request.FILES)
        if emp.is_valid():
            emp.save()
            return redirect(profile)
        else:
            return render(request, 'myapp/editprofile.html',{'emp':emp})
   
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
        
def sendemail(to,usr_name):
    subj="Welcome to Employee Management System!!"
    msg=f"Hi {usr_name}, You're successfully registered to EMP."
    send_mail(subj,msg,settings.EMAIL_HOST_USER,[to])  #to addr should be given in list,else error

# def sendtext(recipient_number,usr_name):
#     wts_msg = f"Hi {usr_name}, You're successfully registered to EMP."         
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN) # Create a Twilio client                
#     # Send the text message
#     client.messages.create(
#         body=wts_msg,
#         from_='+18148023116',  # my Twilio phone number
#         to=recipient_number
# )