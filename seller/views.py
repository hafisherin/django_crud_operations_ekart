from django.shortcuts import redirect, render

from customer.models import Seller
from eKart_admin.models import Category
from seller.models import Product

# Create your views here.
def seller_home(request):
    sellernew = Seller.objects.get(id = request.session['seller'])
    return render(request, 'seller/seller_home.html',{'seller_details':sellernew})


def add_product(request):
    category_list = Category.objects.all()
    msg = ''
    if request.method == 'POST':
        product_no = request.POST['product_no']
        product_name = request.POST['product_name']
        description = request.POST['description']
        stock = request.POST['stock']
        price = request.POST['price']
        image = request.FILES['image']
        category = request.POST['category']
        seller_p = request.session['seller']
        product,created = Product.objects.get_or_create(product_no = product_no ,seller = seller_p,defaults = {
            'product_no':product_no,
            'product_name':product_name,
            'description':description,
            'stock':stock,
            'price':price,
            'image':image,
            'product_category':Category.objects.get(id = category),
            'seller':Seller.objects.get(id = seller_p)

        })
        if created:
            msg = 'Product added'

        else:
            msg = 'Product already exist' 
    context = {'category':category_list,
                'message':msg}
        
    return render(request, 'seller/add_product.html',context)

def add_category(request):
    return render(request, 'seller/add_category.html')

def view_category(request):
    return render(request, 'seller/view_category.html')

def view_products(request):
    products = Product.objects.filter(seller_id = request.session['seller'])
    return render(request, 'seller/view_product.html',{'products':products})

def profile(request):
    return render(request,'seller/profile.html')



def view_orders(request):
    return render(request,'seller/view_orders.html')

def update_stock(request):
    return render(request,'seller/update_stock.html')

def order_history(request):
    return render(request,'seller/order_history.html')

def change_password(request):
    pwd_status = ''
    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        try:
            if len(new_password) > 8 :
                if new_password == confirm_password :
                    seller = Seller.objects.get( id = request.session['seller'])
                    if seller.password == old_password:
                        seller.password = new_password
                        seller.save()
                        pwd_status = 'password changed'
                    else : 
                        pwd_status = 'Incorrect password'
                else:
                    pwd_status = 'password does not exist'
            else:
                pwd_status = 'password should have minimum 8 characters'
        except :
              pwd_status =   'invalid password'                        
    return render(request,'seller/change_password.html',{'msg' : pwd_status})

def seller_logout(request):
    del request.session ['seller']
    request.session.flush()
    return redirect('customer:seller_login')