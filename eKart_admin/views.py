from django.shortcuts import render

# Create your views here.
def admin_home(request):
    return render(request,'ekart_admin/admin_home.html')

def view_category(request):
    return render(request,'ekart_admin/view_category.html')

def add_category(request):
    return render(request,'ekart_admin/add_category.html')

def pending_sellers(request):
    return render(request,'ekart_admin/pending_sellers.html')

def approved_sellers(request):
    return render(request,'ekart_admin/approved_sellers.html')

def customers(request):
    return render(request,'ekart_admin/customers.html')