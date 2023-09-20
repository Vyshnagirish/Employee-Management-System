from django import forms
from myapp.models import *

class EmployeeRegistrationForm(forms.ModelForm):
    EMPLOYEE_TYPE_CHOICES = (
        ('EMPLOYEE', 'Employee'),
        ('HR', 'HR'),
    )
    employee_type = forms.ChoiceField(choices=EMPLOYEE_TYPE_CHOICES, widget=forms.Select)
    class Meta:
        model = User 
        fields = ['name', 'email', 'username', 'password','phone_number','employee_type', 'image']

        widgets={
            'password' : forms.TextInput(attrs={
                'type':"password"
            }),
            'employee_type' : forms.Select(attrs={
                'placeholder':"Select Employee Type"
            })
        }

class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['to', 'subject', 'message','attachment']

    # def __init__(self, *args, **kwargs):
    #     super(MessagesForm, self).__init__(*args, **kwargs)
    #     self.fields['to'].queryset = User.objects.all()  # Set queryset for the 'to' field

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
