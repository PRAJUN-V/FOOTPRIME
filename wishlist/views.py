from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from adminpage.models import Product, ProductVariant
from django.contrib.auth.models import User
from .models import Wishlist, WishlistItem
from django.shortcuts import render, get_object_or_404
# Create your views here.

@login_required(login_url='home:signin')
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
    return render(request, 'wishlist/wishlist.html',{'wishlist_item': wishlist_items})

@login_required(login_url='home:signin')
def add_to_wishlist(request, product_id, varient):
    print(product_id)
    print(varient)
    product = Product.objects.get(id=product_id)
    # Get the selected variant
    specific_variant = ProductVariant.objects.get(product=product_id, size=varient)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    variant_price = specific_variant.price
    wishlist_item, item_created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product, size=varient, price = variant_price)
    if not item_created:
        wishlist_item.save()
    else:
        # If it's a new item in the cart, set the size and other details
        wishlist_item.size = varient
        wishlist_item.variant_stock_quantity = product.variants.filter(size=varient).first().quantity
        wishlist_item.save()
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
    print(wishlist_items)
    return render(request, 'wishlist/wishlist.html',{'wishlist_item': wishlist_items, 'wishlist': wishlist})


@login_required(login_url='home:signin')
def remove_wishlist_item(request, wishlist_item_id):
    item = get_object_or_404(WishlistItem, pk=wishlist_item_id)
    wishlist = item.wishlist  # Get the cart to recalculate the total price

    # Remove the item from the cart
    item.delete()

    return render(request, 'wishlist/wishlist.html', {'wishlist_item': WishlistItem.objects.filter(wishlist=wishlist)})