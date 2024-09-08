from django.shortcuts import render,redirect
from core.models import *
from core.form import *
from core.urls import *
from django.utils import timezone
from django_countries.fields import CountryField
import razorpay
from razorpay import resources,utility
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.


Razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
Razorpay_client.set_app_details({"title" : "Django", "version" : "5.0.7."})
def Index(request):
    product=Product.objects.all()[:7]
    context={
        'product':product
    }

    return render(request,'index.html',context)
def Product_view(request):
    add_image=Add_Image_Form()
    form=Add_Prodect_Form()
    context={
        'product_fields':form,
        'image_fields':add_image,
    }
    if request.method=="POST":
        get_images=request.FILES.getlist('photos')
        print(request.POST)
        data=Add_Prodect_Form(request.POST,request.FILES)
        if data.is_valid():
            fetch_data=data.save()
            # print(data)
            for file in get_images:
                Image.objects.create(image_user=fetch_data,photos=file)
            messages.success(request," product add successfully")
            return redirect("add_product")
        return HttpResponse("sucessfull")
    else:
        return render(request,'add_product.html',context)
def Detail(request,pk):
    product_data=Product.objects.get(id=pk)
    image_data=Image.objects.filter(image_user=product_data)
    context={
        'product_data':product_data,
        'image_data':image_data,
    }
    return render(request,"shop_detail.html",context)
def cart_list(request):
    context={
        'List_of_cart_orders':"No order  here"
    }
    if Orders_list_model.objects.filter(order_list_user=request.user,order_list_ordered_checkbox=False).exists():
        cart_list_orders= Orders_list_model.objects.get(order_list_user=request.user,order_list_ordered_checkbox=False)
        context={
            "List_of_cart_orders":cart_list_orders
        }
        return render(request,'cart_index.html',context)
    return  render(request,'cart_index.html',context)
def Buy_now(request,pk):
    find_product=Product.objects.get(pk=pk)
    order_list_item_new,create=Order_items_models.objects.get_or_create(
        order_user=request.user,
        order_product=find_product,
        ordered_item_checkbox=False
        )
    find_order_list=Orders_list_model.objects.filter(order_list_user=request.user,order_list_ordered_checkbox=False)
    if find_order_list.exists():
        print("value there")
        find_order_list_item=find_order_list[0] 
        if find_order_list_item.order_list_items.filter(order_product__pk=pk).exists():
            print("mistake")
            order_list_item_new.order_quantity +=1
            order_list_item_new.save() 
            # context={
            #     'List_of_cart_orders':"No order  here"
            # }
            # if Orders_list_model.objects.filter(order_list_user=request.user,order_list_ordered_checkbox=False).exists():
            #     cart_list_orders= Orders_list_model.objects.get(order_list_user=request.user,order_list_ordered_checkbox=False)
            #     context={
            #     "List_of_cart_orders":cart_list_orders
            #     }
            return redirect('/main/cart/')
        else:
            find_order_list_item.order_list_items.add(order_list_item_new)
            # context={
            #     'List_of_cart_orders':"No order  here"
            #     }
            # if Orders_list_model.objects.filter(order_list_user=request.user,order_list_ordered_checkbox=False).exists():
            #     cart_list_orders= Orders_list_model.objects.get(order_list_user=request.user,order_list_ordered_checkbox=False)
            #     context={
            #         "List_of_cart_orders":cart_list_orders
            #         }
            #     return render(request,'cart_index.html',context)
            return  redirect('/main/cart/')
            
    else:
        print("i dont have a order")
        context={
        'List_of_cart_orders':"No order  here"
        }
        order_time=timezone.now()
        order_add=Orders_list_model.objects.create(order_list_user=request.user,order_list_start_time=order_time)
        order_add.order_list_items.add(order_list_item_new)
        return redirect('/main/cart/')
def add_cart(request,pk):
    find_product=Product.objects.get(pk=pk)
    order_list_item_new,create=Order_items_models.objects.get_or_create(
        order_user=request.user,
        order_product=find_product,
        ordered_item_checkbox=False
        )
    find_order_list=Orders_list_model.objects.filter(order_list_user=request.user,order_list_ordered_checkbox=False)
    if find_order_list.exists():
        print("value there")
        find_order_list_item=find_order_list[0] 
        if find_order_list_item.order_list_items.filter(order_product__pk=pk).exists():
            order_list_item_new.order_quantity +=1
            order_list_item_new.save() 
            return redirect("/shop/",pk=pk)
        else:
            find_order_list_item.order_list_items.add(order_list_item_new)
            return redirect("/shop/",pk=pk)
    else:
        order_time=timezone.now()
        order_add=Orders_list_model.objects.create(order_list_user=request.user,order_list_start_time=order_time)
        order_add.order_list_items.add(order_list_item_new)
        return redirect("/shop/",pk=pk)
def increase_item(request,pk):
    find_product=Product.objects.get(pk=pk)
    increase_Quantity,create=Order_items_models.objects.get_or_create(
        order_user=request.user,
        order_product=find_product,
        ordered_item_checkbox=False
    )
    fetch_order_list_item=Orders_list_model.objects.filter(order_list_user=request.user,order_list_ordered_checkbox=False)
    if fetch_order_list_item.exists():
        increase=fetch_order_list_item[0]
        if increase.order_list_items.filter(order_product__pk=pk).exists():
            if increase_Quantity.order_quantity<find_product.product_quantity:
                increase_Quantity.order_quantity+=1
                increase_Quantity.save()
                print()
                return redirect('/main/cart/')
                
            else:
                print("quality error")
                return redirect('/main/cart/')
        else:
            print("product id error")
            return redirect('/main/cart/')
    else:
        print("order error")
        return redirect('/main/cart/')
def decrease_order(request,pk):
    fetch_product=Product.objects.get(pk=pk)
    fetch_order_list=Orders_list_model.objects.filter(
        order_list_user=request.user,
        order_list_ordered_checkbox=False
    )
    if fetch_order_list.exists():
        check_fetch_order_list=fetch_order_list[0]
        if check_fetch_order_list.order_list_items.filter(order_product__pk=pk).exists():
            decrease_order_item=Order_items_models.objects.filter(
                order_product=fetch_product,
                ordered_item_checkbox=False,
                order_user=request.user
            )[0]
            if decrease_order_item.order_quantity>1:
                decrease_order_item.order_quantity-=1
                decrease_order_item.save()
                return redirect('/main/cart/')
            else:
                decrease_order_item.delete()
                return redirect('/main/cart/')
        else:
            return redirect('/main/cart/')
    else:
        return redirect('/main/cart/')
def delete(request,pk):
    fetch_product=Product.objects.get(id=pk)
    fetch_list=Order_items_models.objects.filter(order_product=fetch_product,ordered_item_checkbox=False,
    order_user=request.user)[0]
    fetch_list.delete()
    return redirect("/main/cart/")

def Check_out_view(request):
    if Check_out_model.objects.filter(user=request.user).exists():
        get_user=Check_out_model.objects.get(user=request.user.id)
        print(request.user.id,get_user)
        context={
            'form_data':Check_out_Form(instance=get_user)
        }
        if request.method=="POST":
            form_datas=Check_out_Form(request.POST,instance=get_user)
            if form_datas.is_valid():
                form_datas.save()
                return redirect('/main/payment/')
            else:
                return HttpResponse("FORM ERROR")
        else:
            return render(request,'checkout_index.html',context)
    if request.method=='POST':
        form_datas=Check_out_Form(request.POST)
        if form_datas.is_valid():
            country=form_datas.cleaned_data.get('country')
            first_name=form_datas.cleaned_data.get('first_name')
            last_name=form_datas.cleaned_data.get('last_name')
            company_name=form_datas.cleaned_data.get('company_name')
            address=form_datas.cleaned_data.get('address')
            state=form_datas.cleaned_data.get('state')
            post_code=form_datas.cleaned_data.get('post_code')
            order_note=form_datas.cleaned_data.get('order_note')
            get_check_out_data=Check_out_model(user=request.user,country=country,
            first_name=first_name,last_name=last_name,company_name=company_name,
            address=address,
            state=state,
            post_code=post_code,order_note=order_note)
            get_check_out_data.save()
            return redirect('/main/payment/')
        else:
            return HttpResponse("vanakam da mapla theni la irunthu")     
    else: 
        form_datas=Check_out_Form()  
        context={
            'form_data':form_datas
        }        
        return render(request,'checkout_index.html',context)

def Payment(request):
    try:
        payment_order=Orders_list_model.objects.get(order_list_user=request.user,order_list_ordered_checkbox=False)
        print(payment_order)
        payment_address= Check_out_model.objects.get(user=request.user)
        payment_order_amount=payment_order.get_total_product_items()
        payment_currency='INR'
        payment_recept=payment_order.order_list_order_id
        print(payment_address.country)
        notes={
            'address':payment_address.address,
            'state':payment_address.state,
            'post_code':payment_address.post_code,
            "company_name":payment_address.company_name,
        }
        razorpay_order=Razorpay_client.order.create(
            dict(
                amount=payment_order_amount * 100,
                currency=payment_currency,
                receipt=payment_recept,
                notes=notes,
                payment_capture="0",
            )
        )
        payment_order.order_razorpay_id=razorpay_order['id']
        print("sucessfull")
        payment_order.save()
        cart_list_orders= Orders_list_model.objects.get(order_list_user=request.user,order_list_ordered_checkbox=False)
        print(request.user,"this data")
        user_data=Customer.objects.get(user=request.user)
        print(payment_order,"+",razorpay_order['id'],"+",payment_order.order_list_order_id,"+",settings.RAZOR_KEY_ID)
        callback_url='http://127.0.0.1:8000/main/handler/'
        context={
            'payment_order':payment_order,
            'payment_order_id':razorpay_order['id'],
            'order_list_order_id':payment_order.order_list_order_id,
            'final_price':payment_order_amount,
            'razorpay_merchant_id':settings.RAZOR_KEY_ID,
            'cart_data':cart_list_orders,
            'mobile':user_data,
            'callback_url':callback_url
        }
        print('vanakam da mapla')
        return render(request,'payment_razor.html',context)
    except payment_order.DoesNotExist:
        print('no payment order')
        return HttpResponse('404 error')
# def render_pdf(request):
#     order_razorpay_id=request.session['order_razorpay_id']
#     payment_order_razor=Orders_list_model.objects.get(order_razorpay_id=order_razorpay_id)
#     amount=payment_order_razor.get_total_product_items()
#     amount=amount*100
#     get_id=payment_order_razor.order_list_user_id
#     cart_list_ord=Orders_list_model.objects.get(order_list_user_id=get_id)
 
#     payment_status=request.session['payment_status']
    
#     context={
#             'payment_order_razor':payment_order_razor,
#             'payment_status':payment_status,
#             # 'check_out_id':check_out_id,
#             'cart_list_ord':cart_list_ord,
#             }
#     template_path = 'invoice.html'
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response,)
#     # if error then show some funny view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response 

@csrf_exempt
def handlerequest(request):
    print("i am working")
    if request.method=="POST":
        try:
            order_payment_id=request.POST.get("razorpay_payment_id")# fetching data here
            order_razorpay_id=request.POST.get("razorpay_order_id")
            order_signature_id=request.POST.get('razorpay_signature')
            print(request,"this id")
            params_dict={
                'razorpay_order_id':order_razorpay_id,
                'razorpay_payment_id':order_payment_id,
                'razorpay_signature':order_signature_id,
            }

            try:
                payment_order_razor=Orders_list_model.objects.get(order_razorpay_id=order_razorpay_id)
                print('payment id gated')
            except:
                print("payment_order_failed")
                return HttpResponse('505 error')
            payment_order_razor.order_payment_id=order_payment_id
            payment_order_razor.order_signature_id=order_signature_id
            payment_order_razor.save()
            O_id=payment_order_razor.order_list_user
            print(Razorpay_client.utility.verify_payment_signature(params_dict))
            result=Razorpay_client.utility.verify_payment_signature(params_dict)
            if result != None:
                print("Find for final")
                amount=payment_order_razor.get_total_product_items()
                amount=amount*100
                payment_status=Razorpay_client.payment.capture(order_payment_id,amount)
                if payment_status != None:
                    print(payment_status)
                    print("payment completed sucessfully")
                    cart_list_ord=Orders_list_model.objects.get(order_list_user=O_id,order_list_ordered_checkbox=False)
                    payment_order_razor.order_list_ordered_checkbox=True
                    payment_order_razor.save()
                    check_out_id=Check_out_model.objects.get(user=O_id)
                    print(cart_list_ord.order_list_user)
                    userdata=Customer.objects.get(user=cart_list_ord.order_list_user)
                    
                    request.session[
                        "order_completed"
                    ]="your order Placed successfully  and your order will delivered as soon as posable"
                    request.session['order_razorpay_id']=order_razorpay_id
                    request.session['payment_status']=payment_status
                    request.session['payment_status']=payment_status
                    Invoice_Time=timezone.now()
                 
                    
                  
                    context={
                        'payment_order_razor':payment_order_razor,
                        'payment_status':payment_status,
                        'check_out_id':check_out_id,
                        'cart_list_ord':cart_list_ord,
                        'Invoice_Time':Invoice_Time,
                        "userdata":userdata
                    }
                    print("now")
                    return render(request,'invoice.html',context)
                else:
                    print("payment failed")
                    payment_order_razor.order_list_ordered_checkbox=False
                    payment_order_razor.save()
                    request.session[
                        'order_failed'
                    ]="unfortunately  your order not placed plebe try agin"
                    return redirect('payment')
            else:
                payment_order_razor.order_list_ordered_checkbox=False
                payment_order_razor.save()
                print("this is a problem")
                return HttpResponse("true error")

        except:
            print("payment failed")
            payment_order_razor.order_list_ordered_checkbox=False
            payment_order_razor.save()
            return HttpResponse("Error")
    else:
        return HttpResponse("This is Not A POSt Method")
    
def Email(request):
    print("hello")
    if request.method=="POST":
        F_name=request.POST.get('first_name')
        L_name=request.POST.get('last_name')
        subject=request.POST.get('subject')
        email=request.POST.get('email')
        message=request.POST.get('message')
        messages.success(request,"Message send successfully")
        print("working")
        send_mail(subject,"customer details : "+ F_name +" "+L_name+ " " +"message  :"+ message,  "muthurajpostbox@gmail.com",[email])        
       
        return render(request,'contact_index.html')
    else:
        print("not a post")
        return render(request,'contact_index.html')

        






