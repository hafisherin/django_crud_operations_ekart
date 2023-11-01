from django.shortcuts import redirect, render
from random import randint
from django.conf import settings
from django.core.mail import send_mail

from customer.models import Customer, Seller
# Create your views here.


def customer_home(request):
    return render(request, 'customer/customer_home.html')


def store(request):
    return render(request, 'customer/store.html')


def product_detail(request):
    return render(request, 'customer/product_detail.html')


def cart(request):
    return render(request, 'customer/cart.html')


def place_order(request):
    return render(request, 'customer/place_order.html')


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
            request.session['seller_name'] = sellernew[0].first_name + ' ' + seller[0].last_name
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