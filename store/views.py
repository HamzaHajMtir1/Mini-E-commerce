from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem
from django.contrib import messages


def product_list(request):
    products = Product.objects.all()
    
    # Get cart items count
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart_items = CartItem.objects.filter(session_key=session_key)
    cart_items_count = sum(item.quantity for item in cart_items)
    
    context = {
        'products': products,
        'cart_items_count': cart_items_count
    }
    return render(request, 'store/product_list.html', context)



def add_to_cart(request, product_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, session_key=session_key)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    # ✅ Ajouter un message flash
    messages.success(request, f'Produit "{product.name}" ajouté au panier !')

    return redirect('product_list')



def cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

# Supprimer un produit du panier
def remove_from_cart(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id)
    item.delete()
    return redirect('cart')

# Mettre à jour la quantité
def update_cart(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    return redirect('cart')
