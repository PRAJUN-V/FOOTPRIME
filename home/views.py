from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .utils import sent_otp
from datetime import datetime
import pyotp
from django.core.mail import send_mail
from adminpage.models import Product,ProductVariant,Category
from django.contrib.auth.forms import PasswordResetForm
from .custom_otp_generator import generate_otp
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .custom_otp_generator_and_senter import generate_sent_otp
import time
from django.db.models import Q
from django.contrib.auth import authenticate, update_session_auth_hash
from banner.models import Banner
from .models import Enquiry


# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from offer.models import ProductOffer


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            if user.is_staff:
                # Redirect if the user is an admin
                return redirect('adminpage:admin_login')  # Replace with your admin page URL
            else:
                # Redirect if the user is a regular user
                return redirect('home:home')
        else:
            messages.error(request, 'Incorrect username or password')
            return redirect('home:signin')

    else:
        return render(request, 'user_authentication/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'User already exists')
            return redirect('home:signup')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already registered')
            return redirect('home:signup')

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('home:signup')

        # Validate the password
        try:
            validate_password(pass1, request.user)
        except ValidationError as e:
            messages.error(request, ', '.join(e.messages))
            return redirect('home:signup')

        otp = generate_sent_otp(email)
        start_time = time.time()

        request.session['new_user'] = {
            'username': username,
            'email': email,
            'pass1': pass1,
            'otp': otp,
            'start_time': start_time
        }

        return redirect('home:otp_verification')

    else:
        return render(request, 'user_authentication/signup.html')

    
@login_required(login_url='home:signin')
def signout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('home:signin')



#otp verfication
def otp_verification(request):
    error_message = None
    if request.method == 'POST':
        otp1 = request.POST['otp']

        new_user_info = request.session.get('new_user', None)
        
        otp2 = new_user_info['otp']
        start_time = new_user_info['start_time']
        
        if(time.time() - start_time) <= 60:
         if otp1 == otp2:
          # user = get_object_or_404(User, username = username)
          # login(request,user)
            myuser = User.objects.create_user(new_user_info['username'],new_user_info['email'],new_user_info['pass1'])
            myuser.save()
            del request.session['new_user']
            messages.error(request,'Your account has been created Please login')
            return redirect('home:signin')
        
         else:
                messages.error(request,'Invalid one time password')
                print('Invalid one time password')

        else:
                messages.error(request,'OTP expired')
                print('OTP expired')
    
    return render(request, 'user_authentication/otp_verification.html')


#resent OTP
def resent_otp(request):
        new_user_info = request.session.get('new_user', None)
        email = new_user_info['email']
        request.session['new_user']['otp'] =  generate_sent_otp(email)
        request.session['new_user']['start_time'] =  time.time()
        request.session.modified = True
        return redirect('home:otp_verification')


@never_cache
def home(request):
    banner = Banner.objects.all()
    latest_products = Product.objects.filter(is_active=True).order_by('-id')[:3]
    return render(request,'home/home.html',{'banner':banner,'lp':latest_products})


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        category = request.POST.get('category')
        print(category)
        if category == 'all shoes':
            return render(request,'shop/products_listing_page.html',{'products':products,'categories': categories})
        else:
            products = Product.objects.filter(category__name=category)
            return render(request,'shop/products_listing_page.html',{'products':products,'categories': categories,'category_name':category})
    return render(request,'shop/products_listing_page.html',{'products':products,'categories': categories})

#product details
def product_details(request,id):
    product=Product.objects.get(id=id)
    sizes = product.variants.values_list('size', flat=True).distinct()
    print(sizes)
    variant_instance = get_object_or_404(ProductVariant, product_id=id, size=8)
    variant_price = ProductVariant.objects.get(product_id=id, size=8).price
    variant_quantity = ProductVariant.objects.get(product_id=id, size=8).quantity

    print(variant_price)
    #  # Get the price and quantity for size 8
    # size_8_variant = product.variants.filter(size='8').first()
    # size_8_price = size_8_variant.price if size_8_variant else None
    # size_8_quantity = size_8_variant.quantity if size_8_variant else None
    if not variant_instance.price_adjusted:
    # Check if there is a discount for the product and adjust the price if necessary
        product_offer = ProductOffer.objects.filter(product=product).first()
        if product_offer:
            variant_price -= product_offer.discount_amount
            variant_instance.price_adjusted = True  # Set the flag to indicate price adjustment
            # Ensure the price doesn't go below zero
            variant_price = max(0, variant_price)
            variant_instance.price = variant_price
            variant_instance.save()
    product_offer = ProductOffer.objects.filter(product=product).first()
    if product_offer == None:
        a = False
    else:
        a = True      
    print(variant_price)
    product_varient_details={
        'price':variant_price,
        'quantity':variant_quantity,
        'selected':8
    }
    context = {
    'product': product,
    'sizes': sizes,
    **product_varient_details  # This syntax is available in Python 3.5 and later
        }
    context['offer'] = a
    return render(request, 'products/product_details_varient.html',context)


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print('usernot exist')
            messages.error(request,'Usernot exist')
            return redirect('home:forgot_password')
        # Send OTP via email
        if pass1 != pass2:
            print('Password and confirm password not matching')
            messages.error(request,'Password and confirm password not matching')
            return redirect('home:forgot_password')
        else:
            otp = generate_otp()
            print(otp)
            subject = 'Your OTP for Login'
            message = f'OTP : {otp}'
            from_email = 'o23211671@gmail.com'

            # print(otp)
            send_mail(subject, message, from_email, [user.email]) 
            request.session['forget_otp'] = {
                'username': username,
                'pass1': pass1,
                'g_otp' : otp
            }
            return redirect('home:forgot_password_otp_verification')
    return render(request, 'user_authentication/forgot_password.html')

    # return render(request, 'forgot_password.html', {'form': form})
    # return render(request, 'user_authentication/forgot_password.html')


def forgot_password_otp_verification(request):
    otp_session = request.session.get('forget_otp', None)
    username = otp_session['username'] 
    pass1 = otp_session['pass1']  
    g_otp = otp_session['g_otp']
    print(username) 
    print(pass1)
    
    user = User.objects.get(username=username)
           
    if request.method == 'POST':
            otp_post = request.POST['otp']
            # Set the new password for the user
            if g_otp == otp_post:
                user.set_password(pass1)
                user.save()
                print(f"New password set for user {username}")
                return redirect('home:signin')
            else:
                 print('otp wrong')
                 return redirect('home:forgot_password_otp_verification')
            
    
      
    return render(request,'user_authentication/forgot_password_otp_verification.html')


def product_details_varient(request, id, varient):
    product=Product.objects.get(id=id)
    sizes = product.variants.values_list('size', flat=True).distinct()
    variant_instance = get_object_or_404(ProductVariant, product_id=id, size=varient)
    variant_price = ProductVariant.objects.get(product_id=id, size=varient).price
    variant_quantity = ProductVariant.objects.get(product_id=id, size=varient).quantity
    # print(sizes)
    # print(varient)
    # print(id)
    # print(variant_price)
    # print(variant_quantity)
    if not variant_instance.price_adjusted:
    # Check if there is a discount for the product and adjust the price if necessary
        product_offer = ProductOffer.objects.filter(product=product).first()
        if product_offer:
            variant_price -= product_offer.discount_amount
            variant_instance.price_adjusted = True  # Set the flag to indicate price adjustment
            # Ensure the price doesn't go below zero
            variant_price = max(0, variant_price)
            variant_instance.price = variant_price
            variant_instance.save()
    product_offer = ProductOffer.objects.filter(product=product).first()
    if product_offer == None:
        a = False
    else:
        a = True   

    print(variant_price)
    product_varient_details={
        'price':variant_price,
        'quantity':variant_quantity,
        'selected':varient
    }
    context = {
    'product': product,
    'sizes': sizes,
    **product_varient_details  # This syntax is available in Python 3.5 and later
        }
    context['offer'] = a
    return render(request, 'products/product_details_varient.html',context)


def searchbar(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    query = request.GET.get('q')

    if query:
        products = products.filter(Q(title__icontains=query) | Q(category__name__icontains=query))

    if request.method == 'POST':
        category = request.POST.get('category')
        if category == 'all_shoes':
            if query:
                return render(request, 'shop/products_listing_page.html', {'products': products, 'categories': categories})
            else:
                return render(request, 'shop/products_listing_page.html', {'products': products, 'categories': categories})
        elif category:
            products = products.filter(category__name=category)

    return render(request, 'shop/products_listing_page.html', {'products': products, 'categories': categories})


@login_required(login_url='home:signin')    
def change_password(request):
    if request.method == 'POST':
        old_pass = request.POST['old_pass']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        user = authenticate(username=request.user.username, password=old_pass)

        if user is not None:
            try:
                # Validate the new password
                validate_password(pass1, user)
            except ValidationError as e:
                messages.error(request, ', '.join(e.messages))
                return redirect('home:change_password')

            if pass1 == pass2:
                user.set_password(pass1)
                user.save()
                update_session_auth_hash(request, user)  # Update session to prevent logout
                messages.success(request, 'Password changed. Login with your new password...')
                return redirect('home:signin')  # Redirect to the user's profile or any other appropriate page
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'The old password is incorrect.')
    
    return render(request, 'user_authentication/change_password.html')


def about(request):
    return render(request,'home/about.html')


def contact(request):
    return render(request,'home/contact.html')

def enquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # Assuming the user is logged in and you have access to the logged-in user

        # Create an enquiry object and save it to the database
        enquiry = Enquiry.objects.create( name=name, email=email, subject=subject, message=message)
        # You might add some error handling here if the saving process fails

        # Redirect the user to a thank you page or any other appropriate page
        # return redirect('thank_you_page_url')

    return render(request,'home/contact.html')
