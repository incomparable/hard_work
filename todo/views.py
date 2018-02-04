from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from forms import *
from models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import hashlib
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.core.mail import send_mail
import hashlib, datetime, random
from django.contrib.auth import authenticate, login, logout
import json
from django.core import serializers
# this code is working [Simple signup page]

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()  # save user to database if form is valid
#
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
#             activation_key = hashlib.sha1(salt+email).hexdigest()
#             key_expires = datetime.datetime.today() + datetime.timedelta(2)
#
#             # Get user by username
#             user = User.objects.get(username=username)
#
#             # Create and save user profile
#             new_profile = UserProfile(user=user, activation_key=activation_key,
#                                       key_expires=key_expires)
#             new_profile.save()
#             return redirect('/todo/login', {})
#
#     else:
#         form = SignupForm()
#
#     return render(request, 'signup.html', {'form': form})


# Singnup with email activation_key
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()  # save user to database if form is valid
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            # Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://127.0.0.1:8000/todo/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'Django App',
                [email], fail_silently=False)

            return redirect('/todo/success', {})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


# confirm signup with activation key
def signup_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/index')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    # user = user_profile.user
    user_profile.is_active = True
    user_profile.save()
    return render_to_response('confirm.html')


def success(request):
    return render(request, 'successfully_signup.html')


def d3(request):
    return render(request, 'd3.html')


def d3_data(request):
    return render(request, 'd3_data.html')


@login_required(login_url='/todo/login/')
def index(request):
    todo = Todo1.objects.all()[:50]
    context = {
        'todos': todo
    }
    return render(request, 'index.html', context)


def ajax_data(request):
    todo = Todo1.objects.all().values()
    # todo = auth_user.objects.all().values()
    data = list(todo)
    print"******************", data

    return JsonResponse(data, safe=False, content_type="application/json")


@login_required(login_url='/todo/login/')
def details(request, id):
    todo = Todo1.objects.get(id=id)
    print todo
    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)


@login_required(login_url='/todo/login/')
def add(request):
    if(request.method == 'POST'):
        title = request.POST['title']
        text = request.POST['text']
        todo = Todo1(title=title, text=text)
        todo.save()
        return redirect('/todo')
    else:
        return render(request, 'add.html')


@login_required(login_url='/todo/login/')
def delete(request):
    if(request.method == 'POST'):
        id = request.POST['id']
        todo = Todo1(id=id)
        todo.delete()
        return redirect('/todo')
    else:
        todo = Todo1.objects.all()
        context = {
            'todos': todo
        }
        return render(request, 'delete.html', context)


@login_required(login_url='/todo/login/')
def update(request):
    if(request.method == 'POST'):
        id = request.POST['id']
        title = request.POST['title']
        text = request.POST['text']
        todo = Todo1(id=id)
        todo.title = title
        todo.text = text
        todo.save()
        return redirect('/todo')
    else:
        todo = Todo1.objects.all()
        context = {
            'todos': todo
        }
        return render(request, 'update.html', context)


@login_required(login_url='/todo/login/')
def feedback(request):
    if(request.method == 'POST'):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/todo/add')
    else:
        form = FeedbackForm()
        return render(request, 'feedback.html', {'form': form})


@login_required(login_url='/todo/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:

        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def login1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_user = authenticate(username=username, password=password)

        if new_user is not None:
            user_obj = UserProfile.objects.get(user=new_user.id)

            if user_obj.is_active:
                login(request, new_user)
                return render(request, 'add.html', {'username': username})
            else:
                return render(request, 'not_confirm.html')
        else:
            return HttpResponse("Invalid Login")
    else:
        return render(request, 'login.html', {})


def logout1(request):
    logout(request)
    return redirect('/todo/login')
