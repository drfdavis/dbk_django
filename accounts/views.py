from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from .models import DBKAccount
from .forms import RegistrationForm
# send email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import requests


def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            phonenumber = form.cleaned_data['phonenumber']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user  = DBKAccount.objects.create_user(firstname=firstname, lastname=lastname,email=email,username=username,password=password)
            user.phonenumber = phonenumber
            user.save()

            # User sending email and activation key generation
            current_url = get_current_site(request)
            email_subject = "Please activate your account"
            email_message = render_to_string('accounts/accountverification.html',{
                "user":user,
                "domain":current_url,
                "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                "token":default_token_generator.make_token(user)
            })    
            registering_user_email = email
            send_email = EmailMessage(email_subject, email_message, to=[registering_user_email])
            send_email.send()
            # End of user email sending

            # messages.success(request, f"Thank you for registering with us, We have sent a verification email to {registering_user_email}.")

            return redirect('/accounts/login/?command=verify&email='+registering_user_email)
    else:
        form = RegistrationForm()
    
    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email =request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request,'invalid credentials')
            return redirect("login")
    return render(request,'accounts/login.html')



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('login')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = DBKAccount._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError, DBKAccount.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request,"Congratulations!, Your account is activated.")
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


# Password reset Functionality
def passwordreset(request):
    if request.method =='POST':
        email = request.POST['email']
        if DBKAccount.objects.filter(email=email).exists():
            user = DBKAccount.objects.get(email__exact=email)

            # User sending email and activation key generation
            current_url = get_current_site(request)
            email_subject = "Reset your password"
            email_message = render_to_string('accounts/reset_password_email.html',{
                "user":user,
                "domain":current_url,
                "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                "token":default_token_generator.make_token(user)
            })    
            registering_user_email = email
            send_email = EmailMessage(email_subject, email_message, to=[registering_user_email])
            send_email.send()
            # End of user email sending

            messages.success(request, "An email has been sent to reset your password.")
            return redirect('login')
        else:
            messages.error(request, 'Account does not exists')
            return redirect('passwordreset')

    return render(request, 'accounts/passwordreset.html')



def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = DBKAccount._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError, DBKAccount.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid 
        messages.success(request,"Please reset your password")
        return redirect('changepassword')

    else:
        messages.error(request,'This link has expired!')
        return redirect("login")



def changePassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password == confirmpassword:
            uid = request.session.get('uid')
            user = DBKAccount.objects.get(pk=uid)
            user.set_password(password)
            user.save() 
            messages.success(request,"Password reset successful")
            return redirect("login")
        else:
            messages.error(request,'Password does not match!')
            return redirect('changepassword')
    else:
        return render(request, 'accounts/changepassword.html')