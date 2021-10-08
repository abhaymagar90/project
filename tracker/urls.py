from django.urls import path,include
from . import views
from django.contrib.auth.views import logout_then_login

app_name="tracker"
urlpatterns=[

    path('',views.signup,name="signup"), # URL for  signup page

    path('item/',views.add_item,name="items"),  # URL for Adding items

    path('display/',views.display,name="display"), #URL for displaying

    path('<int:id>/', views.delete, name='delete'), #URL for deleting

    path('sortname/',views.sortbyname,name="sname"), #URL for sorting by name page

    path('sortprice/',views.sortbyprice,name="sprice"),#URL for sorting by price page

    path('sortdate/',views.sortbydate,name="sdate"),#URL for sorting by date page

    path('betweendate/',views.betweendate,name = "betweendate" ),


    path('searchbydate/' , views.searchbydate , name = "searchbydate"),

    path('today/' , views.today , name="today"),

    path('yesterday/' , views.yesterday , name="yesterday"),

    path('lastweek/' , views.lastweek , name = "lastweek"),

    path('lastmonth/' , views.lastmonth , name = "lastmonth"),

    path('categories/' , views.categories , name = "categories"),

    path('filters/' , views.filters, name = "filters"),

    path('aboutus/' , views.aboutus , name="aboutus"),


    path('login/',views.loginpage ,name="login"),#URL for Login

	path('logout/', views.logoutpage, name="logout"),
    
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX
]





