from django.shortcuts import render, redirect
from django.contrib import messages

from tuokoleane.tokens import account_activation_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from io import BytesIO
import sys
from django.core.files import File
from PIL import Image, ImageDraw
import os
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.encoding import force_bytes
from .models import *
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.db.models import Q
import re
from django.contrib.auth import get_user_model
from datetime import datetime, date
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import json
from django.utils.safestring import mark_safe, SafeText, SafeData
from django.utils.encoding import force_str
import random
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse
from tuokoleane.settings import EMAIL_HOST_USER
from time import sleep
# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        contributions = Contribution.objects.filter(contributor = request.user)
        total_contribution = 0
        for contribution in contributions:
            total_contribution += int(contribution.amount)

        events_involved_in = [x for x in FundraisingEvent.objects.all() if request.user in x.members.all() and x.host != request.user ]
        events_involved_in_count = len(events_involved_in)
        my_events = FundraisingEvent.objects.filter(host = request.user)

        latest_events = FundraisingEvent.objects.filter(host = request.user)
        percentage_progress = 0
        if len(latest_events) > 0:
            latest_event = latest_events[len(latest_events) - 1]
            percentage_progress = (int(latest_event.amount_contributed) / int(latest_event.target_amount) ) * 100
        return render(request, 'fundraiser/dashboard.html', {'total_contribution':total_contribution,'events_involved_in': events_involved_in,'events_involved_in_count':events_involved_in_count, 'my_events': my_events, 'percentage_progress': percentage_progress})
    else:
        return redirect("fundraiser:index")

def index(request):
    if request.user.is_authenticated:
        return redirect("fundraiser:dashboard")
    else:
        return render(request, 'fundraiser/index.html')



def contact_us(request):
    return render(request, 'fundraiser/contact_us.html')


def register(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email_address")
        password = request.POST.get("password1")
        users = User.objects.filter(email__iexact=email)
        if users.count() > 0:
            error_msg = "user with that email already exists,kindly enter another email address."
            return render(request, 'fundraiser/register.html',
                            {'error_msg': error_msg})
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=email,
                                                    password=password)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Please activate your Tuokoleane account'
            message = render_to_string('fundraiser/activation_request.html',
                                        {'user': user,
                                        'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user)
                                        }
                                    )

            user.email_user(subject, message)

            return render(request, 'fundraiser/activation_sent.html')

    elif request.user.is_authenticated:
        return redirect("fundraiser:dashboard")

    else:
        return render(request, 'fundraiser/register.html')


def activation_sent_view(request):
    return render(request, 'fundraiser/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'fundraiser/account_activated.html')
    else:
        return render(request, 'fundraiser/activation_invalid.html')




def login_user(request):
    if request.method == "POST" and not request.user.is_authenticated:
        email = request.POST.get('email_address')
        password = request.POST.get('password')
        try:
            username =User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                
                return redirect("fundraiser:dashboard")
            
            else:
                return render(request, 'fundraiser/login.html', {"error_msg": "incorrect username or password"})
        except:
            return render(request, 'fundraiser/login.html', {"error_msg": "incorrect username or password"})
    else:
        return render(request, 'fundraiser/login.html')
    

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'fundraiser/profile.html')
    else:
        return redirect("fundraiser:login_user")


def logout_user(request):
    logout(request)
    request.session.clear()
    return redirect('fundraiser:index')

def fundraising_event(request, code):
    event = FundraisingEvent.objects.get(code = code)
    contributions = Contribution.objects.filter(fundraising_event = event)
    members_contributions = []
    for contribution in contributions:
        contributor = contribution.contributor
        person_contributions = Contribution.objects.filter(Q(contributor = contributor) & Q(fundraising_event = event))
        total_person_contribution_amount = 0
        for person_contribution in person_contributions:
            total_person_contribution_amount += int(person_contribution.amount)
        
        full_name = contributor.first_name + ' ' + contributor.last_name
        members_contributions.append(
            [full_name, total_person_contribution_amount]
        )
        

    joined = "yes"
    if request.user not in event.members.all():
        joined = "no"

    percentage_progress = (int(event.amount_contributed) / int(event.target_amount)) * 100
    return render(request, 'fundraiser/fundraising_event.html', {
        'event': event, 'joined':joined, 'contributions': contributions,
        'members_contributions': members_contributions, 'percentage_progress': percentage_progress,
        })

def create_fundraising_event(request):
    if request.user.is_authenticated and request.method == "POST":
        code = get_random_string(20)
        event = FundraisingEvent.objects.create(
            host = request.user,
            code = code,
            name = request.POST.get("event_name"),
            intent = request.POST.get("event_intention"),
            description = request.POST.get("event_description"),
            start_date = request.POST.get("event_start_date"),
            end_date = request.POST.get("event_end_date"),
            target_amount = request.POST.get('event_target_amount'),
            amount_contributed = 0,
            active = True

        ).save()

        event.members.add(request.user)
        return redirect("fundraiser:fundraising_event", code)

    elif not request.user.is_authenticated:
        return redirect("fundraiser:login_user")
    
    return redirect("fundraiser:dashboard")


def join_fundraising_event(request, code):
    if request.user.is_authenticated:
        event = FundraisingEvent.objects.get(code = code)
        if request.user not in event.members.all():
                event.members.add(request.user)

        return redirect("fundraiser:fundraising_event", code = code)
    
    else:
        return redirect("fundraiser:index")


def donate(request):
    if request.user.is_authenticated and request.method == "POST":
        event_code = request.POST.get("event_code")
        event = FundraisingEvent.objects.get(code = event_code)
        amount = request.POST.get("amount")
        Contribution.objects.create(
            contributor = request.user,
            fundraising_event = event,
            amount = amount,
            mpesa_transaction_code = get_random_string(12).upper(),

        ).save()
        event.amount_contributed = int(event.amount_contributed) + int(amount)
        event.save()
        data = {"successful":"yes"}
        return JsonResponse(data)

    return redirect("fundraiser:dashboard")


def about_us(request):
    return render(request, 'fundraiser/about_us.html')

def contact_us(request):
    return render(request, 'fundraiser/contact_us.html')


def our_services(request):
    return render(request, 'fundraiser/our_services.html')

def how_it_works(request):
    return render(request, 'fundraiser/how_it_works.html')