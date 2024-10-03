from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
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
from wallet.models import Wallet
from django.http import JsonResponse

@login_required(login_url='home:signin')
def add_to_cart(request, product_id, varient):
    product = Product.objects.get(id=product_id)
    
    # Get the selected variant
    specific_variant = ProductVariant.objects.get(product=product_id, size=varient)
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    variant_price = specific_variant.price
    variant_quantity = specific_variant.quantity
    print(variant_quantity)
    # Check if the product variant is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, size=varient, price = variant_price)


    print(product)
    print(specific_variant)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If it's a new item in the cart, set the size and other details
        cart_item.size = varient
        cart_item.save()
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.price * item.quantity for item in cart_items)


    return render(request,'cart/cart_management.html',{'cart_item': cart_items, 'total_price': total_price,'cart': cart})  # Redirect to the cart view

@login_required(login_url='home:signin')
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product variant is already in the cart
    cart_item= CartItem.objects.filter(cart=cart)
    total_price = sum(item.price * item.quantity for item in CartItem.objects.filter(cart=cart))
    
    return render(request,'cart/cart_management.html',{'cart_item':cart_item,'total_price': total_price})

@login_required(login_url='home:signin')
def checkout(request, product_id,varient):
    product = Product.objects.get(id=product_id)
    user=request.user
    user_id = user.id
    specific_variant = ProductVariant.objects.get(product=product_id, size=varient)
    address=UserAddress.objects.filter(user=user_id)
   
    user_mobile_instance = UserMobile.objects.get(user=request.user)
    if specific_variant.quantity == 0:
        return redirect(reverse('your_app_name:your_view_name'))
   
    if request.method == 'POST':
        print('hi')
        print(request.POST)
        if 'coupon_code' in request.POST:
            code  = request.POST.get('coupon_code')
            print(code)
            return redirect('home:home')
        else:
            address  = request.POST.get('address')
            order_details = OrderDetails.objects.create(
                    user=request.user,
                    order_time=timezone.now(),  # Assuming you import timezone from django.utils
                    user_mobile= user_mobile_instance,
                    user_address=address,  # Replace with the actual address
                    product=product,
                    product_variant=specific_variant,
                    product_quantity=1,  # Replace with the actual quantity
                    product_price=specific_variant.price,  # Replace with the actual price
                    payment_method='cash_on_delivery',
                    order_status='pending'
                )
            return redirect('cart_management:order_confirmed')
        
    return render(request, 'cart/checkout.html', {'products': product,'varient':specific_variant,'address':address})

@login_required(login_url='home:signin')
def order_confirmed(request):
    return render(request,'cart/order_confirmed.html')

@login_required(login_url='home:signin')
def cart_checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart)
    # total_price = sum(item.price * item.quantity for item in cart_item)
    original_total_price = sum(item.price * item.quantity for item in cart_item)
    user=request.user
    user_id = user.id
    address=UserAddress.objects.filter(user=user_id)

    # Check if there's an applied coupon in the session
    applied_coupon_code = request.session.get('applied_coupon')
    if applied_coupon_code:
        try:
            coupon = Coupon.objects.get(code=applied_coupon_code)
            # Recalculate total price with the applied coupon
            # Assuming coupon.discount_price is the percentage of discount
            discount_percentage = Decimal(coupon.discount_price) / 100  # Convert percentage to decimal

            # Calculate the discount amount
            discount_amount = original_total_price * discount_percentage

            # Calculate the total price after applying the discount
            total_price = original_total_price - discount_amount

            # Ensure that the total price doesn't go below zero
            total_price = max(total_price, Decimal(0))
  # Ensure total_price doesn't go negative
        except Coupon.DoesNotExist:
            # Handle the case where the coupon does not exist (possibly invalidated)
            messages.error(request, "Invalid coupon code.")
            total_price = original_total_price
    else:
        total_price = original_total_price

    if request.method == 'POST':
        if 'coupon_code' in request.POST:
            code = request.POST.get('coupon_code')
            try:
                coupon = Coupon.objects.get(code=code)
                # Check if the user has already used this coupon
                
                if coupon.is_active:
                # Check if the user has already used this coupon
                    if not CouponUsage.objects.filter(user=request.user, coupon=coupon).exists():
                        if total_price >= coupon.minimum_cart_value:
                            request.session['applied_coupon'] = coupon.code
                            messages.success(request, f'{coupon.code} is applied')
                            total_price -= Decimal(coupon.discount_price)
                            total_price = max(total_price, Decimal(0))  # Ensure total_price doesn't go negative
                        else:
                            messages.error(request, f'The minimum cart value for this coupon is {coupon.minimum_cart_value}')
                        # Save coupon usage after order confirmation

                    else:
                        # User has already used the coupon
                        messages.error(request, "This coupon has already been used by the user.")  # Ensure total_price doesn't go negative

                    # Save coupon usage after order confirmation
                else:
                # Coupon is not active, mark it as expired
                    messages.error(request, "Coupon expired")
            except Coupon.DoesNotExist:
        # Handle the case where the coupon does not exist
                messages.error(request, "Invalid coupon code.")
            except CouponUsage.DoesNotExist:
        # Handle the case where the CouponUsage does not exist
                messages.error(request, "CouponUsage does not exist") 

            
            return redirect('cart_management:cart_checkout')
        else:
            selected_payment_option = request.POST.get('payment_option', None)
            # Check if a payment option was selected
            if selected_payment_option:
            # Process the selected payment option
                if selected_payment_option == 'COD':
                    if total_price <= 10000:
                        address = request.POST.get('address')
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
                            address  = request.POST.get('address')
                            # Assuming you have a model for user_mobile_instance, adjust this part accordingly
                            user_mobile_instance, created = UserMobile.objects.get_or_create(user=user)
                            selected_payment_option = request.POST.get('payment_option', None)
                            payment = Payment.objects.create(
                                user=request.user,
                                amount=total_price,
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
                                product_price=total_price,
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
                    else:
                        messages.error(request, "COD not applicable for price greater than 10000") 
                        return redirect('cart_management:cart_checkout')

                elif selected_payment_option == 'Paypal':
                    address = request.POST.get('address')
                    request.session['user_address'] = address
                    
                    selected_payment_option = request.POST.get('payment_option', None)
                    request.session['user_payment_option'] = selected_payment_option
                    # Handle Paypal logic
                    total_price_str = str(total_price)
                    request.session['total_price'] = total_price_str
                    return redirect('payment:home')
                elif selected_payment_option == 'Wallet':
                    user_wallet, created = Wallet.objects.get_or_create(user=request.user)
                    if user_wallet.balance >= total_price:
                # Perform the wallet payment
                        user_wallet.balance -= total_price
                        user_wallet.save()
                        address = request.POST.get('address')
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
                            address  = request.POST.get('address')
                            # Assuming you have a model for user_mobile_instance, adjust this part accordingly
                            user_mobile_instance, created = UserMobile.objects.get_or_create(user=user)
                            selected_payment_option = request.POST.get('payment_option', None)
                            payment = Payment.objects.create(
                                user=request.user,
                                amount=total_price,
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
                                product_price=total_price,
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
                    else:
                        messages.error(request, 'Insufficient balance in your wallet. Please add money to your wallet.')
                        return redirect('wallet:wallet')

                else:
                    # Handle other payment options
                    return HttpResponse('Invalid Payment Option')
            
    return render(request,'cart/cart_checkout.html',{'cart_item': cart_item,'total_price': total_price,'address':address,'original_price':original_total_price,'discount':original_total_price-total_price})

@login_required(login_url='home:signin')
def remove_cart_item(request, cart_item_id):
    item = get_object_or_404(CartItem, pk=cart_item_id)
    cart = item.cart  # Get the cart to recalculate the total price

    # Remove the item from the cart
    item.delete()

    # Recalculate the total price after removing the item
    total_price = sum(item.price * item.quantity for item in CartItem.objects.filter(cart=cart))

    return render(request, 'cart/cart_management.html', {'cart_item': CartItem.objects.filter(cart=cart), 'total_price': total_price})


@login_required(login_url='home:signin')
def quantity_add(request, cart_item_id, product_id, size):
    item = get_object_or_404(CartItem, pk=cart_item_id)
    cart = item.cart
    product = Product.objects.get(id=product_id)
    variant = ProductVariant.objects.get(product=product, size=size)
    item.quantity += 1
    response_data = {}

    if variant.quantity < item.quantity:
        response_data['error'] = 'Stock limit exceeded'
    elif item.quantity <= 5:
        item.save()
    else:
        response_data['error'] = 'Each customer is limited to a maximum purchase quantity of 5 units'

    response_data['quantity'] = item.quantity
    total_price = sum(item.price * item.quantity for item in CartItem.objects.filter(cart=cart))
    response_data['total_price'] = total_price

    return JsonResponse(response_data)

@login_required(login_url='home:signin')
def quantity_minus(request, cart_item_id):
    item = get_object_or_404(CartItem, pk=cart_item_id)
    cart = item.cart
    item.quantity -= 1
    response_data = {}

    if item.quantity != 0:
        item.save()
    else:
        response_data['error'] = 'Product quantity must be at least 1'

    response_data['quantity'] = item.quantity
    total_price = sum(item.price * item.quantity for item in CartItem.objects.filter(cart=cart))
    response_data['total_price'] = total_price

    return JsonResponse(response_data)


@login_required(login_url='home:signin')
def apply_coupon(request):
    pass

@login_required(login_url='home:signin')
def payment_page(request):
   return render(request,'cart/payment.html')