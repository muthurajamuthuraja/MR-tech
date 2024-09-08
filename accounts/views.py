from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import *
def Login(request):
    context={
        'Error':''
    }
    if request.method=='POST':
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request,user)
            return redirect("index")
        else:
            context={
                'Error':'User and password incorrect'
            }
            print("not working")
            return render(request,'accounts/login.html',context)
    return render(request,'accounts/login.html',context)
def Logout(request):
    logout(request)
    return redirect('Signin')
def Signup(request):
    context={
        'Error':''
    }
    if request.method=='POST':
        print("i am working")
        if User.objects.filter(username=request.POST['username']).exists():
            print('user name error')
            context={
                'Error':'user_name already be taken'
            }
            messages.success(request,"User_name already be taken")
            return render(request,'accounts/signup.html')
        elif User.objects.filter(email=request.POST['email']).exists():
            print("email error")
            context={
                "Error":'Email already taken'
            }
            messages.success(request,"Email already be taken")
            return render(request,'accounts/signup.html')
        elif request.POST.get('password')!=request.POST.get('conform_password'):
            
            context={
                "Error":'conform password not correct'
            }
            messages.success(request,'conform password not correct')
            return render(request,'accounts/signup.html')
        else:
            user=User(username=request.POST['username'],email=request.POST['email'])
            user.set_password(request.POST['password'])
            user.save()
            print("i am here")
            data_Customer=Customer(user=user,mobile=request.POST['mobile_number'])
            data_Customer.save()
            Login_verification=authenticate(username=request.POST['username'],password=request.POST['password'])
            print(request.POST['username'],"this is")
            if Login_verification is not None:
                login(request,Login_verification)
                return redirect('/main/index')
            else:
                print("login error")
    messages.success(request,"Welcome <~>")
    return render(request,'accounts/signup.html',context)

def About(request):
    return render(request,'about_index.html')
def Blog(request):
    return render(request,'blog_index.html')
def Cart(request):
    return render(request,'cart_index.html')
# def Checkout(request):
#     return render(request,'checkout_index.html')
def Contact(request):
    return render(request,'contact_index.html')
def Shop(request):
    product=Product.objects.all()
    context={
        'product':product,
    }
    return render(request,'shop_index.html',context)
def Services(request):
    return render(request,'services_index.html')
def Thank_you(request):
    return render(request,'thankyou_index.html')
