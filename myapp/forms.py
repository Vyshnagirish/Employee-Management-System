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
        fields = ['name', 'email', 'username', 'password','employee_type', 'image']

        widgets={
            'password' : forms.TextInput(attrs={
                'type':"password"
            }),
            'employee_type' : forms.Select(attrs={
                'placeholder':"Select Employee Type"
            })
        }
