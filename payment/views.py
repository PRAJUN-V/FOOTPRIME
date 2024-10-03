from django.shortcuts import render,redirect
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse
from django.conf import settings
from user_profile.models import UserAddress, UserMobile
from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from cart_management.models import Cart, CartItem
from adminpage.models import Product, ProductVariant
from django.shortcuts import render, get_object_or_404
from user_profile.models import UserAddress, UserMobile
from cart_management.models import OrderDetails
from django.utils import timezone
from django.contrib import messages
from django.db.models import F
from django.shortcuts import render, redirect, reverse
from coupon.models import Coupon,CouponUsage
from decimal import Decimal
from adminpage.models import Payment

# Create your views here.
def home(request):
    # total_price = request.GET.get('total_price') 
    total_price_str = request.session.get('total_price', '800')
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_price_str,
        'item_name':'Product 1',
        'invoice':str(uuid.uuid4()),
        'currency_code':'USD',
        'notify_url':f'http://{host}{reverse("paypal-ipn")}',
        'return_url':f"http://{host}{reverse('payment:paypal_return')}",
        'cancel_return':f'http://{host}{reverse("payment:paypal_cancel")}',
    }
    form = PayPalPaymentsForm(initial = paypal_dict)
    context = {'form':form}
    return render(request,'payment/home.html',context)

def paypal_return(request):
    print('success')
    address =  request.session.get('user_address', None)
    cart, created = Cart.objects.get_or_create(user=request.user)
    print(cart)
    cart_item = CartItem.objects.filter(cart=cart)
    print(cart_item)
    user=request.user
    user_id = user.id
    address=UserAddress.objects.filter(user=user_id)
    cart_items_info = cart_item.values_list('product_id', 'quantity','size','price')
                    # Iterate through the items in the cart
    print(cart_items_info)
    for product_id, quantity, size, price in cart_items_info:
        product = get_object_or_404(Product, id=product_id)
        product_variant = get_object_or_404(ProductVariant, product=product, size=size)
        ProductVariant.objects.filter(product=product, size=size).update(quantity=F('quantity') - quantity)
        address  = request.session.get('user_address', None)
                        # Assuming you have a model for user_mobile_instance, adjust this part accordingly
        user_mobile_instance, created = UserMobile.objects.get_or_create(user=user)
        selected_payment_option = request.session.get('user_payment_option', None)
        payment = Payment.objects.create(
        user=request.user,
        amount= request.session.get('total_price', None),
        payment_type=selected_payment_option
        )

                        # Create an OrderDetails instance for each product in the cart
        order_details = OrderDetails.objects.create(
                            user=request.user,
                            order_time=timezone.now(),
                            user_mobile=user_mobile_instance,
                            user_address=address,
                            product=product,
                            product_variant=product_variant,
                            product_quantity=quantity,
                            product_price = request.session.get('total_price', None),
                            payment=payment, 
                            order_status='pending'
                        )
                    # Save coupon usage after order confirmation
        applied_coupon_code = request.session.get('applied_coupon')
        if applied_coupon_code:
                        applied_coupon = Coupon.objects.get(code=applied_coupon_code)
                        CouponUsage.objects.create(user=request.user, coupon=applied_coupon)
        if 'applied_coupon' in request.session:
                        del request.session['applied_coupon']   
        cart_item.delete()
        return redirect('cart_management:order_confirmed')
    del request.session['total_price']
    del request.session['user_payment_option']
    del request.session['user_address']
    return redirect('cart_management:order_confirmed')

def paypal_cancel(request):
    print('canceled')
    return redirect('cart_management:cart_checkout')