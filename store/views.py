from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Banner
from .cart import Cart
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.utils import timezone
import requests
import base64

# =======================
# HOME PAGE
# =======================
@login_required
def home(request):
    products = Product.objects.all()
    banners = Banner.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'banners': banners
    })


# =======================
# ADD TO CART
# =======================
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {'quantity': 1}

    request.session['cart'] = cart
    return redirect('home')


# =======================
# REMOVE FROM CART
# =======================
@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('view_cart')


# =======================
# VIEW CART
# =======================
@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# =======================
# LOGIN VIEW
# =======================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})


# =======================
# REGISTER VIEW
# =======================
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'store/register.html', {'form': form})


# =======================
# PAYMENTS PAGE VIEW
# =======================
@login_required
def payments_page(request):
    amount = request.GET.get('amount', 0)
    return render(request, 'store/payments.html', {'amount': amount})


# =======================
# SAFARICOM STK PUSH
# =======================
@login_required
def stk_push(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')

        # Access token
        consumer_key = 'b5dnlJGefptAf1qo3t8LM8R6EnKVxvmPpyKchFeuuJetZAK5'
        consumer_secret = 'MgGMUnzC3Saj4E8WT8L3CPox9rqltCRASOztZlAeZdyIQWP5ApqyNfPsMtteBgws'
        auth_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        try:
            r = requests.get(auth_url, auth=(consumer_key, consumer_secret))
            r.raise_for_status()
            access_token = r.json().get('access_token')
        except Exception as e:
            return HttpResponse(f"Error fetching access token: {e}", status=500)

        if not access_token:
            return HttpResponse("Access token is missing or invalid", status=400)

        # Payload
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        shortcode = '174379'
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(float(amount)),
            "PartyA": phone,
            "PartyB": shortcode,
            "PhoneNumber": phone,
            "CallBackURL": "https://infinity-link.onrender.com/mpesa/callback/",
            "AccountReference": "Test123",
            "TransactionDesc": "Test Payment"
        }

        try:
            response = requests.post(
                '"https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"',
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return HttpResponse(f"✅ STK Push Initiated. Check your phone.<br><pre>{response.text}</pre>")
        except Exception as e:
            return HttpResponse(f"❌ Error during STK Push: {e}<br><pre>{response.text}</pre>", status=500)

    return redirect('home')
