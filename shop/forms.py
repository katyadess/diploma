from django import forms
from .models import *
from django.core.mail import EmailMessage

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm



class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'id': 'email', 
            'name': 'email',
        }), 
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'name': 'password'
        }), 
        required=True
    )


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
        
        
class RegisterForm(UserCreationForm):
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'id': 'email', 
            'name': 'email',
        }), 
        required=True
    )
    
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'first-name',
            'id': 'first-name'
        }),
        max_length=100, 
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'last-name',
            'id': 'last-name'
        }),
        max_length=100, 
        required=True
    )
    
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'phone', 
            'name': 'phone',
            'type': 'tel',
            'onkeydown': "phoneNumberFormatter()",
        }), 
        required=True
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
    
    
class EditAccountForm(UserChangeForm):
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'id': 'email', 
            'name': 'email',
        }), 
        required=True
    )
    
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'first-name',
            'id': 'first-name'
        }),
        max_length=100, 
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'last-name',
            'id': 'last-name'
        }),
        max_length=100, 
        required=True
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class EditPhoneForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['telephone'] 
        widgets = {
            'telephone': forms.TextInput(attrs= {
                'id': 'phone', 
                'name': 'phone',
                'type': 'tel',
                'onkeydown': "phoneNumberFormatter()",
            })
        }
        
class AddAddressForm(forms.ModelForm):
    
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'phone', 
            'name': 'phone',
            'type': 'tel',
            'onkeydown': "phoneNumberFormatter()",
        }), 
        required=True
    ) 
    
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone_number', 'city', 'street']
        
class EditAddressForm(forms.ModelForm):
    
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'phone', 
            'name': 'phone',
            'type': 'tel',
            'onkeydown': "phoneNumberFormatter()",
        }), 
        required=True
    ) 
    
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone_number', 'city', 'street']
        

class ProductReviewForm(forms.ModelForm):
    
    text = forms.CharField(widget = forms.Textarea(attrs={
        'name': 'message',
        'id': 'message',
        'rows': 0,
        
    }), required=True)
    
    class Meta:
        model = ProductReview
        fields = ['rating', 'text']
        
class ReplyForm(forms.ModelForm):
    
    text = forms.CharField(widget = forms.Textarea(attrs={
        'name': 'text',
        'id': 'text',
        'rows': 0,
        
    }), required=True)
    
    class Meta:
        model = ProductReview
        fields = ['text']
        
class ReviewImageForm(forms.ModelForm):
    
    image = forms.FileField(widget = forms.FileInput(attrs={
        "name": "file-upload",
        "type": "file",
        "id": 'file-upload',
        'allow_multiple_selected': True,
    }), required=False)
    
    class Meta:
        model = ReviewImage
        fields = ['image']
        
        
class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []