from random import randint
from django.conf import settings
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from customer.models import Seller
from eKart_admin.models import Category

# Create your views here.
def admin_home(request):
    return render(request,'ekart_admin/admin_home.html')

def view_category(request):
    category_list = Category.objects.all()
    return render(request,'ekart_admin/view_category.html',{'category':category_list})

def add_category(request):
    msg = ''
    if request.method == 'POST':
        c_name = request.POST['category_name']
        c_description = request.POST['description']
        c_image =  request.FILES['category_image']

        category_exist = Category.objects.filter(category_name = c_name)
        if not category_exist:
            new_category = Category(
                category_name = c_name,
                description = c_description,
                cover_picture = c_image
            )
            new_category.save()
            msg = 'Category added succesfull'
        else:
            msg = ' Category already exist'    
    return render(request,'ekart_admin/add_category.html',{'message':msg})



def approve_seller(request,id):
    seller = Seller.objects.get(id = id)
    seller_id = randint(111111,999999)
    temporary_password = 'sel-'+ str(seller_id)
    subject = 'login credantials'
    message = 'Hai! Your ekart account has been approved. your id is '+str(seller_id)+' And password is '+ temporary_password 
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [seller.email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list
    )
    Seller.objects.filter(id = id).update(loginid = seller_id ,password = temporary_password , status = 'Approved')
    return redirect('ekart_admin:pending_sellers')

def pending_sellers(request):
    pending_list = Seller.objects.filter(status = 'pending')
    return render(request,'ekart_admin/pending_sellers.html',{'list':pending_list})

def approved_sellers(request):

    return render(request,'ekart_admin/approved_sellers.html')

def customers(request):
    return render(request,'ekart_admin/customers.html')

def admin_login(request):
    return render(request,'ekart_admin/admin_login.html')

