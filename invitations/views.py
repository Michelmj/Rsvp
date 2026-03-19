from django.shortcuts import render

# Create your views here.
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .models import rsvp
from django.contrib import messages
from django.db import IntegrityError
from .services import append_to_google_sheet
    
    
def home(request):
    return render(request, 'invitations/invite.html')


def invited(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        spouse = request.POST.get('spouse_name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        response = request.POST.get('response')
        
        try:
            rsvp.objects.create(
                name = name,
                spouse_name = spouse,
                email = email,
                number = number,
                response = response
            )
        
        except IntegrityError:
            messages.error(request, "An RSVP has already been submitted with this email or phone number.")
            return redirect('home')
        
        # Email to you
        send_mail(
            subject='New RSVP Submission',
            message=f"""
New RSVP Received

Name: {name}
Email: {email}
Response: {response}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['seph.n.mario@gmail.com'],
            fail_silently=False,
        )

        # Thank-you email to guest
        send_mail(
            subject='Thank You for Your RSVP',
            message=f"""
Dear {name},

Thank you for your RSVP!
Your response: {response}

Warm regards,
Sephora & Mario
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('thank_you')
    
    # If someone visits this URL directly
    return redirect('home')

def thank_you(request):
    return render(request, 'invitations/thank_you.html')