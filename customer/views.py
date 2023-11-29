from datetime import date
import datetime
from django.db.models import  F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from random import randint
from django.conf import settings
from django.core.mail import send_mail
import razorpay

from customer.models import Cart, Customer, Order, OrderItem
from seller.models import Product,Seller
# Create your views here.


def customer_home(request):
    customer = Customer.objects.get(id = request.session['customer'])
    products = Product.objects.all()
    context = {
        'products': products,
        'customer_details':customer
    }
    return render(request, 'customer/customer_home.html',context)


def store(request):
    query = request.GET.get('query')
    if query == 'all':
        product = Product.objects.all()
    else:
        product = Product.objects.filter(product_category = query)
    return render(request, 'customer/store.html',{'product':product})


def product_detail(request,id):
    msg = ''
    product = Product.objects.get(id = id)
    customer = Customer.objects.get(id = request.session['customer'])
    
    if request.method == 'POST':
        if 'customer'in request.session:
            cart = Cart(customer = customer,product = product, price= product.price)
            # product_exist = Product .objects.filter(product = product).exists()
            
            cart.save()
            msg = 'Added to Cart'
        else:
            return redirect('customer:customer_login')
        
    try:
        cart_item = get_object_or_404(Cart,customer = customer, product= id)    
        item_exist = True
    except Exception as e:
        item_exist = False

    context ={
        'product':product,
        'message':msg,
        'item_exist':item_exist

    }



    return render(request, 'customer/product_detail.html',context)


def cart(request):
    customer = Customer.objects.get(id = request.session['customer'])
    grand_total = 0

    cart = Cart.objects.filter(customer_id = customer.id).annotate(sub_total = F('quantity')*F('price'))
    for item in cart:
        grand_total += item.sub_total


    context = {
        'cart':cart,
        'customer_details':customer,
        'grand_total':grand_total
    }

    return render(request, 'customer/cart.html',context)

def remove_cart(request,id):
    item =Cart.objects.get(id = id)
    item.delete()
    return redirect('customer:cart')

def update_cart(request):
    product_id =request.POST['id']
    product_quantity  = request.POST['qty']
    grand_total = 0
    cart_item = Cart.objects.get(product = product_id)
    cart_item.quantity = product_quantity

    cart_item.save()
    
    cart = Cart.objects.filter(customer_id = request.session['customer']).annotate(sub_total = F('quantity')*F('price'))
    for item in cart:
        grand_total += item.sub_total

        return JsonResponse({'status':'quantity_update','grand_total': grand_total})
    

    
def update_payment(request):

    
    if request.method == 'GET':
        return redirect('customer:customer_home')

    order_id = request.POST['razorpay_order_id']
    payment_id = request.POST['razorpay_payment_id']
    signature = request.POST['razorpay_signature']
    client = razorpay.Client(auth = (settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }
    print(params_dict)
    signature_valid = client.utility.verify_payment_signature(params_dict)
    if signature_valid:
        print("**************** yes")
    
        order_details = Order.objects.get(order_id = order_id)
        order_details.payment_status = True
        order_details.payment_id = payment_id
        order_details.signature_id = signature
        # order_details.shipping_address_id = shipping_address
        order_details.order_status = 'order placed on ' + str(date.today())
        cart = Cart.objects.filter(customer = request.session['customer'])

        for item in cart:
            order_item = OrderItem(order_id = order_details.id,  products_id = item.product.id, quantity = item.quantity, price = item.product.price )
            order_item.save()
            selected_qty = item.quantity
            selected_product = Product.objects.get(id = item.product.id)
            selected_product.stock -= selected_qty
            selected_product.save()
            

   
        order_details.save()
        cart.delete()
        return render(request,'customer/order_complete.html')

        # customer_name = request.session['customer_name']
        # order_number =  order_details.order_no
        # current_year = datetime.now().year
        
        # subject = "Order Confirmation"
        # from_email = settings.EMAIL_HOST_USER

        # to_email = ['hafi@gmail.com']

        
        # address = DeliveryAddress.objects.get(customer = request.session['customer'], id = shipping_address)
        # html_content = render_to_string('customer/invoice.html', {
        # 'customer_name': customer_name,
        # 'order_no': order_number,
        # 'order_date': order_details.created_at,
        # 'current_year': current_year,
        # 'address': address,
        # 'grand_total': order_details.total_amount
        
        # })
            
        # msg = EmailMultiAlternatives(subject, html_content, from_email, to_email)
        # msg.attach_alternative(html_content, "text/html")

 
        # msg.send()
    
    

def place_order(request):
    return render(request, 'customer/place_order.html')

def order_product(request):
    cart = Cart.objects.filter(customer = request.session['customer']).annotate(sub_total = F('quantity')*F('price'))
    grand_total = 0 
    for item in cart:
        grand_total += item.sub_total
    order_amount = grand_total 
    order_currency = 'INR'
    order_receipt ='order_receipt_01'
    notes = {'shipping address':'Koyas ,calicut'}
    order_number = 'OD-EKART-'+str(randint(1111111111,9999999999))
    client = razorpay.Client(auth = (settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET))
    payment = client.order.create({
        'amount': order_amount*100,
        'currency': order_currency,
        'receipt':order_receipt,
        'notes':notes
    })
    order = Order(customer_id = request.session['customer'],order_id = payment['id'],order_amount =grand_total,order_number = order_number)
    order.save()


    return JsonResponse(payment)


def order_complete(request):
    return render(request, 'customer/order_complete.html')


def dashboard(request):
    return render(request, 'customer/dashboard.html')


def seller_register(request):
    msg = ''
    status = False
    if request.method == 'POST' :
        f_name  = request.POST['fname']
        l_name = request.POST['lname']
        email = request.POST['email']
        gender = request.POST['gender']
        city = request.POST['city']
        country = request.POST['country']
        company_name = request.POST['cmp_name']
        bank_name  = request.POST['bank_name']
        bank_branch = request.POST['branch']
        ifsc = request.POST['ifsc']
        seller_image = request.FILES['picture']
        
        
        account_number = request.POST['acct_name']

        seller_exist = Seller.objects.filter(email = email).exists()
        if not seller_exist :
            seller = Seller(
                first_name = f_name,
                last_name = l_name,
                email = email,
                gender = gender,
                city = city,
                country = country,
                picture = seller_image,
                account_number = account_number, 
                company_name = company_name,
                bank_name = bank_name,
                bank_branch = bank_branch,
                ifsc = ifsc
            )
            
            seller.save()
            msg = 'Account created successfully' 
            status = True
        else :
            msg = 'Account already exist'
          
    return render(request, 'customer/seller_register.html',{'message' : msg})


def seller_login(request):
    msg = ''
    if request.method == 'POST':
        s_username = request.POST['sellerid']
        s_password = request.POST['password']
        
        sellernew = Seller.objects.filter(loginid =  s_username, password = s_password)

        if sellernew.exists():
            request.session['seller'] = sellernew[0].id
            request.session['seller_name'] = sellernew[0].first_name + ' ' + sellernew[0].last_name
            return redirect('Seller:seller_home')
        else :
            msg = 'Incorrect Password or Seller Id'

    return render(request, 'customer/seller_login.html' ,{'message' : msg})


def customer_signup(request):
    msg = ''
    status = False
    if request.method == 'POST':
        f_name = request.POST['fname']
        l_name = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        city = request.POST['city']
        country = request.POST['country']
        pasword= request.POST['password']

        customer_exist = Customer.objects.filter(email = email).exists()
        
        if not customer_exist:
            customer = Customer(
                first_name = f_name,
                last_name = l_name,
                email = email,
                gender = gender,
                city = city,
                country = country,
                password = pasword)
            customer.save()
            msg = 'Succesfully registered'
            status = True
        else:
            msg = 'Already registered'   
    return render(request, 'customer/customer_signup.html',{'message' : msg ,'status' : status})


def customer_login(request):
    msg = ''
    if request.method == 'POST':
        c_email = request.POST['email']
        c_pasword = request.POST['password']
        
        customer = Customer.objects.filter(email = c_email , password = c_pasword)

        if customer.exists():
            request.session['customer'] = customer[0].id
            return redirect('customer:customer_home')
        else :
            msg = 'incorrect password or username'
         


    return render(request, 'customer/customer_login.html',{'message' : msg })



def forgot_password_customer(request):
    return render(request, 'customer/forgot_password_customer.html')


def forgot_password_seller(request):
    return render(request, 'customer/forgot_password_seller.html')