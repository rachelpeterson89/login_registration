from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):

    # Check if post request
    if request.method == 'POST':

        # Check if register object is valid
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect('/')

        # Check to see if user email is already in use
        user = User.objects.filter(email=request.POST['email'])

        # Could also say if(user):
        if len(user) > 0:
            messages.error(request,'Email is already in use!',extra_tags='email')
            return redirect('/')

        # Hash the password with Bcrypt
        pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

        # Create user in database
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw
        )

        # Put user id into session & redirect
        request.session['user_id'] = User.objects.last().id
        return redirect('/dashboard')

    else:
        return redirect('/')

def login(request):
    # Check if it is a POST REQUEST
    if request.method == 'POST':

        # Validate the login object
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect('/')

        # Check to see if the email is in the Database
        user = User.objects.filter(email=request.POST['login_email'])
        if len(user) == 0:
            messages.error(request,'Invalid Email/Password',extra_tags='login_email')
            return redirect('/')

        # Check if passwords match
        if not bcrypt.checkpw(request.POST['login_password'].encode(),user[0].password.encode()):
            messages.error(request,'Invalid Email/Password',extra_tags='login_password')
            return redirect('/')

        # Push UserId into session and redirect
        request.session['user_id'] = user[0].id
        print("iiiiiiiiiddddddd", request.session['user_id'])
        return redirect('/dashboard')
    else:
        return redirect('/')

def dashboard(request):
    # If there's nobody in session we don't want them to login
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_the_messages': Message.objects.all(),
            'all_the_comments': Comment.objects.all(),
        }
        return render(request, 'dashboard.html', context)


def logout(request):
    # you want to clear out session and redirect to root route
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')


def post_message(request):
    user = User.objects.get(id=request.session['user_id'])
    print("this is my user", user)
    Message.objects.create(message_content=request.POST['message'], message_user=User.objects.get(id=request.session['user_id']))
    return redirect('/dashboard')


def post_comment(request):
    Comment.objects.create(comment_content=request.POST['comment'], comment_user=User.objects.get(id=request.session['user_id']), message=Message.objects.get(id=request.POST['message_id']))
    return redirect('/dashboard')

def delete_msg(request, message_id):
    message_to_destroy = Message.objects.get(id=message_id)
    message_to_destroy.delete() 
    return redirect('/dashboard')

def delete_cmt(request, comment_id):
    comment_to_destroy = Comment.objects.get(id=comment_id)
    comment_to_destroy.delete()
    return redirect('/dashboard')