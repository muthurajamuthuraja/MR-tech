from django.urls import path
from core import views
from django.urls import path,include

urlpatterns = [
    path('index',views.Index,name='index'),
    path('addproduct',views.Product_view,name='add_product'),
    path('add_cart/<int:pk>',views.add_cart,name='add_cart'),
    path('buy_now/<int:pk>',views.Buy_now,name='buy_now'),
    path('cart/',views.cart_list,name='cart'),
    path('email/',views.Email,name='email'),
    path('detail/<int:pk>',views.Detail,name='detail'),
    path('check_out/',views.Check_out_view,name='check_out'),
    path('increase/<int:pk>',views.increase_item,name='increase_item'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('decrease_order/<int:pk>',views.decrease_order,name='decrease_order'),
    path('payment/',views.Payment,name='payment'),
    path('handler/',views.handlerequest,name='handler'),
    # path('render_pdf/',views.render_pdf,name='render_pdf'),
]