from django.shortcuts import render, redirect
from django.conf import settings
from .models import rsvp
from django.contrib import messages
from django.db import IntegrityError
import os
import sendgrid
from sendgrid.helpers.mail import Mail


def send_email(to_email, subject, body):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    sg.send(message)


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
                name=name,
                spouse_name=spouse,
                email=email,
                number=number,
                response=response
            )

        except IntegrityError:
            messages.error(request, "An RSVP has already been submitted with this email or phone number.")
            return redirect('home')

        # Email to you
        send_email(
            to_email='phi.jim@hotmail.com',
            subject='New RSVP Submission',
            body=f"""
New RSVP Received

Name: {name}
Spouse: {spouse}
Email: {email}
Phone: {number}
Response: {response}
"""
        )

        # Thank-you email to guest
        send_email(
            to_email=email,
            subject='Thank You for Your RSVP',
            body=f"""
Dear {name},

Thank you for your RSVP!
Your response: {response}

Warm regards,
Sephora & Mario
"""
        )

        return redirect('thank_you')

    return redirect('home')


def thank_you(request):
    return render(request, 'invitations/thank_you.html')