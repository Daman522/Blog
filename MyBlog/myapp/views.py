from django.shortcuts import render
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from django.urls import reverse
import re
from .models import *
import json
from django.http import JsonResponse
from time import sleep
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import stripe

import random
from datetime import datetime  
# Create your views here.



def base(request):
    return render(request,'base.html')

def design(request):
    return render(request,'design.html')


def home(request):
    p=Post.objects.all()
    print(p)
    return render(request,'home.html',locals())


class Login(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        data = {
            'status' : False
        }
        print(request.POST)
        email= request.POST['email']
        password = request.POST['password']
        try:
            user_= User.objects.get(email=email)
            print(user_,'----user')
            user = authenticate(request,username=user_.username, password=password)
            print(user,'-------useerrr')
            if user is not None:
                login(request, user)
                data['status'] = True
                data['message'] = 'Logged in'
                # messages.success(request, 'logged in')
                return HttpResponseRedirect(reverse("base"))
            else:
                data['status'] = False
                data['message'] = 'Invalid Credentials'
                # messages.error(request, "Invalid Credentials")
                return HttpResponseRedirect(reverse("base"))
        except Exception as e:
            data['status'] = False
            data['message'] = 'User not exists with given username'
            messages.error(request, 'User not exists with given username')
            return HttpResponseRedirect(reverse("base"))

        finally:
            return HttpResponse(json.dumps(data), content_type="application/json")


class Register(View):
   
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        print(request.POST,'---rrrppppp')
        data = {
            'status' : False
        }
        username= request.POST.get('username')
        email= request.POST.get('email')
        password=request.POST.get('password')
        confirmpass=request.POST.get('re_password')

        try:
            User.objects.get(email=email)
            return HttpResponse("email already exists")

        except User.DoesNotExist:
            if password == confirmpass:
                u=User(username=username,email=email)
                print(u,'--u')
                u.set_password(password)
                print(u.set_password(password),'--passswww')
                u.save()
                data['status'] = True
                data['message'] = 'Registered!,Now you can login'
                # messages.success(request, 'Now you can login')
                return HttpResponseRedirect('login')
                # return HttpResponse("REGISTERRRRR")
            else:
                messages.error(request, 'password doesnt match')
        except Exception as e:
            print(e)
            data['status'] = False
            data['message'] = 'Error'
        finally:
            return HttpResponse(json.dumps(data), content_type="application/json")

class Logout(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse("base"))








#for adding posts
@login_required(login_url='login')
def addpost(request):
   
    if request.method=='POST':
        # print(request.POST,'--------ooo')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        # date= request.POST.get('date')
        img=request.FILES.getlist('img', None)[0]
        print(img)
  
        obj = Post(title=title,desc =desc ,image=img,author=request.user)
        obj.save()
        return HttpResponse('CREATED')


    return render(request,'addpost.html')



def allpost(request):
    if request.method=="POST":
        pass
    p=Post.objects.all()
    print(p)
    return render(request,'allpost.html',locals())



def viewpost(request,id):
    p=Post.objects.get(id=id)
    return render(request,'viewpost.html',locals())


def updatepost(request,id):
    if request.method == "POST":
        print(request.POST,'------updateee')
     
        try:
            P = Post.objects.get(id = id)
           
            P.title = request.POST.get('title')
            P.desc = request.POST.get('desc')

            if request.FILES.getlist('img', None):
                print(request.FILES.getlist('img', None))
                P.image = request.FILES.getlist('img', None)[0]
           
            P.save()
            print("sssssssssssss")
            messages.success(request, 'Updated!')
            # return HttpResponseRedirect(reverse('viewpost', kwargs={'id':id}))
            return HttpResponseRedirect(reverse('base'))
        
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse("base"))
     



    else:
        p = Post.objects.get(id = id)
        print(  p.author.id ,'author--------')
        print(request.user.id ,'useridd--------')
        if p.author.id != request.user.id:
            messages.error(request, 'Errors')
            return HttpResponseRedirect(reverse('base'))
        return render(request,"updatepost.html",locals())



def deletepost(request,id):
    
    d = Post.objects.filter(id=id)
    print(d,'------')
    messages.error(request, 'deleted')
    d.delete()
    
    return HttpResponseRedirect(reverse('base'))

def stripe(request):
    

    if request.method=="POST":
        print(request.POST)
        price_id = request.POST.get('price_id')

        stripe.api_key = "sk_test_51IutOESIibBGQfNw9Kh8WrqFVo4JfQsNcuThkgeVNjer8AOxtQorMLICj36KOMVQ6l78052I3TG9oIbATRAaQELH00zYrLUTQc"

        session = stripe.checkout.Session.create(
            success_url='http://127.0.0.1:8000/success/?session_id={CHECKOUT_SESSION_ID}&pid='+price_id,
            cancel_url='http://127.0.0.1:8000/cancel',
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': price_id,
                # For metered billing, do not pass quantity
                'quantity': 1
            }],
        )

        return redirect(session.url, code=303)

    return render(request,'stripe.html')


       