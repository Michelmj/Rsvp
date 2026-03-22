from django.shortcuts import render, redirect
from django.conf import settings
from .models import rsvp
from django.contrib import messages
from django.db import IntegrityError
import os
import resend
from .services import append_to_google_sheet


def send_email(to_email, subject, body):
    try:
        resend.api_key = os.environ.get('RESEND_API_KEY')
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": subject,
            "text": body
        })
    except Exception as e:
        print(f"Email error: {e}")


def home(request):
    if request.session.get('rsvp_submitted'):
        return redirect('thank_you')
    return render(request, 'invitations/invite.html')


def invited(request):
    if request.method == 'POST':

        if request.session.get('rsvp_submitted'):
            return redirect('thank_you')

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
            messages.error(request, "An RSVP has already been submitted with this email address.")
            return redirect('home')

        request.session['rsvp_submitted'] = True
        request.session.set_expiry(0)

        try:
            append_to_google_sheet(name, spouse, email, number, response)
        except Exception as e:
            print(f"Google Sheets error: {e}")

        send_email(
            to_email='seph.n.mario@gmail.com',
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
    accepted_guests = rsvp.objects.filter(response='accepts').order_by('submittedat')

    # Count total people (guest + spouse if they have one)
    total_people = sum(2 if guest.spouse_name else 1 for guest in accepted_guests)

    return render(request, 'invitations/thank_you.html', {
        'accepted_guests': accepted_guests,
        'total_people': total_people,
    })