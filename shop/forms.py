from django import forms
from .models import *
from django.core.mail import EmailMessage

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm


class SubscribeForm(forms.ModelForm):
    
    class Meta: 
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs= {
            'placeholder': 'Enter your email...',
            })
        }
        
    def send_email(self):
    
        email = self.cleaned_data['email']
        subject = f"Email from ÉCLAT ESSENTIALS"
        body = f"You successfully subscribed to our newsletter!"
        from_email = 'katyadess.django@gmail.com'
        to_email = [email]
        
        email_message = EmailMessage(subject, body, from_email, to_email)
        email_message.send()
        
        
class ContactForm(forms.Form):
        
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required': 'required'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'required': 'required'}))
    files = forms.FileField(widget = forms.FileInput(attrs={
            "name": "file-upload",
            "type": "file",
            "id": 'file-upload',
            'allow_multiple_selected': True,
    }), required=False)
    
    def send_email(self):
    
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        files = self.files.getlist('file_upload')
        
        subject = f"New Contact Form Submission from {name}"
        body = f"Message from {name} ({email}):\n\n{message}"
        from_email = f'{email}'
        to_email = ['katyadess.django@gmail.com']
        
        email_message = EmailMessage(subject, body, from_email, to_email)

        for file in files:
            email_message.attach(file.name, file.read(), file.content_type)

        email_message.send()