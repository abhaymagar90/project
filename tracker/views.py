from django.db.models import Q

from django.shortcuts import render,redirect,reverse

from django.shortcuts import get_object_or_404

from django.http import HttpResponse,HttpResponseRedirect

from .forms import ItemModelForm

from . models import Item , Category , Sub_category

from django.db.models import Sum

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import SignUpForm

from datetime import datetime , timedelta

import re,json

import requests


def signup(request):                       #View for signing up using custom inbuilt UserCreationForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():                #Checking for form validation and retriving username,pass from POST data
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
                
            return HttpResponseRedirect('/login')
    else:
        form = SignUpForm()                 # IF not logged in then Show empty form
    return render(request, 'registration/signup.html', {'form': form})

def loginpage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/item')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'registration/login.html',context )


def logoutpage(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def add_item(request):                      # Add all expenses items
    k=Item.objects.aggregate(Sum('price'))   # gets total sum of expenses
    l=json.dumps(k)                          # converts into json string
    p=re.findall("\d+",l)                    #Retrives numerical part from returned string
    item = Item.objects.all()
    if request.method == "POST":
        form = ItemModelForm(request.POST,request.FILES, request = request)  #request.FILES contains uploaded files
        if form.is_valid():
            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            model_instance = form.save(commit=False)
            model_instance.save()
            form = ItemModelForm(request = request)
            return HttpResponseRedirect('/item') #redirects to same page after POST
    else:
        form = ItemModelForm(request = request)
    return render(request, "tracker/index.html", {'form': form ,'item':item,'sum':p })


@login_required(login_url='login')
def display(request):                                     #displaying all items
    category = request.GET.get('category')
    if category == None:
        item = Item.objects.filter(un = request.user.id)
    else:
        item = Item.objects.filter(category__name=category , un = request.user.id)


    k = Item.objects.filter(un = request.user.id).aggregate(Sum('price'))
    l = json.dumps(k)
    p = re.findall("\d+", l)
    item = Item.objects.filter(un = request.user.id)

    categories = Category.objects.all()
    d = { 'item' : item  , 'categories' : categories , 'items':item ,'sum':p}

    return render(request,"tracker/table.html",d)

@login_required(login_url='login')
def delete(request,id):                                    #deleting items by primary key on click
    deleteitem=get_object_or_404(Item,pk=id).delete()
    return HttpResponseRedirect('/display')

@login_required(login_url='login')
def sortbyname(request):                                   # sorting by name
    sname=Item.objects.order_by('name').filter(un = request.user.id)
    return render(request,"tracker/sname.html",{'name':sname})

@login_required(login_url='login')
def sortbyprice(request):                                  #sorting by price
    sprice=Item.objects.order_by('price').filter(un = request.user.id)
    return render(request,"tracker/sprice.html",{'price':sprice})

@login_required(login_url='login')
def sortbydate(request):                                    #sorting by date
    sdate=Item.objects.order_by('created_at').filter(un = request.user.id)
    return render(request,"tracker/sdate.html",{'date':sdate})



@login_required(login_url='login')
def betweendate(request):
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        searchresult = Item.objects.filter(Q(created_at__gte=fromdate) & Q(created_at__lte=todate) ,  un = request.user.id)
        searchresultcount = Item.objects.filter(Q(created_at__gte=fromdate) & Q(created_at__lte=todate),  un = request.user.id).count()
        d = {"searchresult" : searchresult , "fromdate" : fromdate , "todate" : todate , "searchresultcount" : searchresultcount}
        return render(request , "tracker/betweendate.html" , d)
    else:
        searchresult = Item.objects.none()
        return render(request , "tracker/betweendate.html" , {"searchresult":searchresult})




@login_required(login_url='login')
def searchbydate(request):
    if request.method == "POST":
        searchbydate = request.POST['searchbydate']
        
        search = Item.objects.filter(created_at = searchbydate ,  un = request.user.id)
        
        d = {"search" : search , "searchbydate" : searchbydate}
        return render(request , "tracker/searchbydate.html" , d)
    else:
        search = Item.objects.none()
        return render(request , "tracker/searchbydate.html" , {"search":search})

@login_required(login_url='login')
def today(request):
    
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    
    tv = Item.objects.filter(created_at = today ,  un = request.user.id)
    return render(request ,"tracker/today.html" , {"tv" : tv} )
    
@login_required(login_url='login')
def yesterday(request):
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    
    yv = Item.objects.filter(created_at = yesterday ,  un = request.user.id)
    return render(request ,"tracker/yesterday.html" , {"yv" : yv} )

@login_required(login_url='login')
def lastweek(request):
    today = datetime.now().date()
    lastweek = today - timedelta(7)
    
    lw = Item.objects.filter(created_at__gte=lastweek , created_at__lte=today ,  un = request.user.id)
    return render(request ,"tracker/lastweek.html" , {"lw" : lw} )

@login_required(login_url='login')
def lastmonth(request):
    if not request.user.is_authenticated:
         return render(request ,"tracker/index.html")
    today = datetime.now().date()
    lastmonth = today - timedelta(30)
    
    lm = Item.objects.filter(created_at__gte=lastmonth , created_at__lte=today ,  un = request.user.id)
    return render(request ,"tracker/lastmonth.html" , {"lm" : lm} )
    
@login_required(login_url='login')
def categories(request):
    category = request.GET.get('category')
    sub_category = request.GET.get('sub_category')
    
    
    if category == None:
        
        if sub_category == None:
            item = Item.objects.filter(un = request.user.id)
            
        else:
            item = Item.objects.filter(sub_category__name=sub_category , un = request.user.id)
       
    else:
        if sub_category == None:
            item = Item.objects.filter(category__name=category , un = request.user.id)
        else:
            item = Item.objects.filter(sub_category__name=sub_category , un = request.user.id)
    
    k = Item.objects.aggregate(Sum('price'))
    l = json.dumps(k)
    p = re.findall("\d+", l)
    categories = Category.objects.all()
    d = { 'item' : item  , 'categories' : categories , 'items':item ,'sum':p}
    return render(request,"tracker/categories.html",d)

@login_required(login_url='login')
def filters(request):
    return render(request,"tracker/filters.html")

@login_required(login_url='login')
def load_cities(request):
    category_id = request.GET.get('category_id')
    sub_categories = Sub_category.objects.filter(category_id=category_id ).all()
    return render(request, 'tracker/sub_category_dropdown_list_options.html', {'sub_categories': sub_categories})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

def aboutus(request):
    return render(request ,"tracker/aboutus.html")
