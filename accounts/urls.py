from django.urls import path,include
from accounts import views
urlpatterns = [

    path('',views.Login,name='Signin'),
    path('main/',include('core.urls')),
    path('logout/',views.Logout,name='logout'),
    path('signup/',views.Signup,name='Signup'),
    path('about/',views.About,name='about'),
    path('blog/',views.Blog,name='blog'),
    path('contact/',views.Contact,name='contact'),
    path('shop/',views.Shop,name='shop'),
    path('services/',views.Services,name='services'),
    path('thankyou/',views.Thank_you,name='thankyou'),
]