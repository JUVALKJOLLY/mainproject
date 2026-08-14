from django import forms 
from .models import Student


class StudentForm(forms.ModelForm):
    
    class Meta :
        model = Student
        fields=['first_name' , 'last_name' , 'email' , 'courses']
        widgets={
            'first_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter First Name'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Last Name'
            }),

            'email':forms.EmailInput(attrs={
                'class':'form-control'
            }),

            'courses':forms.CheckboxSelectMultiple()
        }


def clean_email(self):
    email=self.cleaned_data.get('email')
    
    if not email.endswith("@university.edu"):
        raise forms.ValidationError(
            "Only university emails are allowed"
        )    
        
    return email