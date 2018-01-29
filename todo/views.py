from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from forms import *
from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import hashlib, datetime, random
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def signup(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = SignupForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            # email_subject = 'Account confirmation'
            # email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            # 48hours http://127.0.0.1:8000/confirm/%s" % (username, activation_key)

            # send_mail(email_subject, email_body, 'myemail@example.com',
            #     [email], fail_silently=False)

            return render(request,'login.html',{})
    else:
        args['form'] = SignupForm()

    return render_to_response('signup.html', args, context_instance=RequestContext(request))


@login_required
@permission_required('todo', login_url='login')
def index(request):
    todo = Todo1.objects.all()[:50]
    context = {
        'todos': todo
    }
    # return HttpResponse('hello world!')
    return render(request, 'index.html', context)


@login_required
@permission_required('todo', login_url='login')
def details(request, id):
    todo = Todo1.objects.get(id=id)
    print todo
    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)


@login_required
@permission_required('todo', login_url='login')
def add(request):
    if(request.method == 'POST'):
        title = request.POST['title']
        text = request.POST['text']
        todo = Todo1(title=title, text=text)
        todo.save()
        return redirect('/todo')
    else:
        return render(request, 'add.html')


@login_required
@permission_required('todo', login_url='login')
def feedback(request):
    if(request.method == 'POST'):
        name = request.POST['name']
        email = request.POST['email']
        stars = request.POST['stars']
        message = request.POST['message']
        feed = Feedback(name=name, email=email, stars=stars, message=message)
        feed.save()
        return render(request, 'add.html')
    else:
        return render(request, 'feedback.html')


@login_required
@permission_required('todo', login_url='login')
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


@login_required
@permission_required('todo', login_url='login')
def update(request):
    if(request.method == 'POST'):
        id = request.POST['id']
        title = request.POST['title']
        text = request.POST['text']
        todo = Todo1(id=id)
        todo.title=title
        todo.text=text
        todo.save()
        return redirect('/todo')
    else:
        todo = Todo1.objects.all()
        context = {
            'todos': todo
        }
        return render(request, 'update.html', context)


def login1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_user = authenticate(username=username, password=password)

        if new_user is not None:
            if new_user.is_active:
                login(request, new_user)
                return render(request, 'add.html', {'username': username})
            else:
                return HttpResponse("Disabled account")

        else:
            return HttpResponse("Invalid Login")


    else:
        return render(request, 'login.html', {})


@login_required
@permission_required('todo', login_url='login')
def logout_view(request):
    logout(request)
    return render(request, '/login')