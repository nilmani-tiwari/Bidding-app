from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Item,Bidder

# Create your views here.


def login_user(request): 

    print("***************************************************************")
    
    if request.method == 'POST':
        username = request.POST.get('email').strip().lower()
        
        password =request.POST.get('password').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("user login")
            return redirect("/home")
        else:
            print("invalid user")
            messages.info(request, 'Username OR password is incorrect')
            return render(request,'login.html' )
            # return redirect('/login_user')
           
    
    return render(request,'login.html' )


def register(request): 

    print("*****************&&&&&&&&&&&&&&&&&**********************************************")
    
    if request.method == 'POST':
        name = request.POST.get('name').strip().lower()
        username = request.POST.get('email').strip().lower()
        
        password =request.POST.get('password').strip()

        print(name,username,password)

        user = User.objects.filter(email=username)
        if not user.exists():
            user = User.objects.create(username=username, email=username, first_name=name)
        else:
            user = user.first()
            messages.success(request, f'User {username} Already exist')
            return redirect('/')
        user.set_password(password)
        user.save()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("user login")
            messages.success(request, f'User {username} created successfully')
            # return redirect(dashboard)
        else:
            print("invalid user")
            messages.info(request, 'Username OR password is incorrect')
            return render(request,'login.html' )
            # return redirect('/login_user')
           
    
    return render(request,'register.html' )



@login_required(login_url='login_user')
def home(request): 
    user=request.user
    
    obj=Item.objects.all().values()
    
    
    ob=Bidder.objects.values("item").filter(user=user)
    for i in obj:
        print(i["id"])
        if {"item":i.get("id") }in ob:
            i.update({"bided":True})
            print(True)
        else:
            i.update({"bided":False})

    print(ob)
    context={"items":obj}

           
    return render(request,'home.html',context )
from django.db.models import Min  
@login_required(login_url='login_user')
def singleitem(request,id): 
    user=request.user
    

    obj=Item.objects.get(id=id)


    ob=Bidder.objects.filter(item=obj,user=user).order_by("myPrice")
    
    print(ob,obj,user)

    cprice=(obj.basePrice)-1
    context={"item":obj,"cprice":cprice}
    
    exist=ob.exists()
    if exist:
        ob=ob.first()
        messages.success(request, f'You have Already bidded for  {ob.item.name} @ {ob.myPrice}')


    if request.method == 'POST':
        myprice = request.POST.get('myprice')
        item= request.POST.get('iid')
        i_obj=Item.objects.get(id=int(item))
        # print(myprice ,"*(*&*((((((((((((((*************<")

        
        
        if exist:
            ob.myPrice=myprice
        else:
            ob=Bidder(item=obj,user=user,myPrice=myprice)
            ob.save()

        lowest_price = Bidder.objects.values('myPrice',"item","user").order_by('myPrice').first()
        # print(lowest_price,"***************************7777777777777")
        
        email=User.objects.get(id=lowest_price["user"]).email
        i_obj.currentPrice=lowest_price["myPrice"]
        i_obj.lowest_bidder_id=lowest_price["user"]
        i_obj.lowest_bidder_email=email
        i_obj.save()

        messages.success(request, f'Your bidding {myprice} submited successfully for {i_obj.name}')
        # return redirect(f'/single-item/{int(item)}/')
        return redirect(f'/home/')




        
           
    return render(request,'home2.html',context )

def logoutUser(request):
    logout(request)
    return redirect('/')



@login_required(login_url='login_user')
def item_report(request):
    print(request.user.is_superuser )
    context={}
    if request.user.is_superuser :
    
        obj=Item.objects.all()
        context={"items":obj}

    else:
        messages.info(request, 'Only admin can view this report')


    return render(request,'report.html',context )


@login_required(login_url='login_user')
def lowest_bidder(request,item):
    print(request.user.is_superuser )
    context={}
    if request.user.is_superuser :
        item=Item.objects.get(id=item)
        print(item)
    
        obj=Bidder.objects.filter(item=item).order_by("myPrice")
        lowest_bid=obj.first()
        print(obj)
        context={"bid":obj,"lowest_bid":lowest_bid,"item":item}

    else:
        messages.info(request, 'Only admin can view this report')


    return render(request,'bid_report.html',context )