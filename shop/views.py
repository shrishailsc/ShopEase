
from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Order, OrderItem


def home(request):
    products = Product.objects.all()
    return render(request, "shop/home.html", {"products": products})


def cart_detail(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product is None:
            continue

        quantity = int(quantity)
        if quantity <= 0:
            continue

        subtotal = product.price * quantity
        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })
        total += subtotal

    return render(
        request,
        "shop/cart.html",
        {"items": items, "total": total},
    )


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    key = str(product_id)
    quantity = int(cart.get(key, 0))

    if quantity < product.stock:
        cart[key] = quantity + 1
        request.session["cart"] = cart
        messages.success(request, "Product added to cart.")
    else:
        messages.error(request, "No more stock available.")

    return redirect("cart")


def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    key = str(product_id)

    if key in cart:
        try:
            quantity = int(request.POST.get("quantity", 1))
        except (ValueError, TypeError):
            quantity = 1

        if quantity <= 0:
            cart.pop(key, None)
        elif quantity <= product.stock:
            cart[key] = quantity
        else:
            messages.error(request, "Requested quantity exceeds available stock.")

    request.session["cart"] = cart
    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")



def checkout(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product is None:
            continue

        quantity = int(quantity)
        if quantity <= 0:
            continue

        subtotal = product.price * quantity
        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })
        total += subtotal

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("home")

    if request.method == "POST":
        name = request.POST.get("customer_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        postal_code = request.POST.get("postal_code", "").strip()

        if not all([name, email, phone, address, city, state, postal_code]):
            messages.error(request, "Please fill in every field.")
            return render(request, "shop/checkout.html", {
                "items": items, "total": total
            })

        if len(postal_code) != 6 or not postal_code.isdigit():
            messages.error(request, "Enter a valid 6-digit PIN code.")
            return render(request, "shop/checkout.html", {
                "items": items, "total": total
            })

        try:
            with transaction.atomic():
                order_lines = []
                verified_total = Decimal("0.00")

                for item in items:
                    product = Product.objects.select_for_update().get(
                        pk=item["product"].pk
                    )
                    quantity = item["quantity"]

                    if quantity > product.stock:
                        raise ValueError(
                            f"Not enough stock for {product.name}."
                        )

                    order_lines.append((product, quantity))
                    verified_total += product.price * quantity

                order = Order.objects.create(
                    customer_name=name,
                    email=email,
                    phone=phone,
                    address=address,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    total_amount=verified_total,
                )

                for product, quantity in order_lines:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        price=product.price,
                        quantity=quantity,
                    )
                    product.stock -= quantity
                    product.save(update_fields=["stock"])

        except Product.DoesNotExist:
            messages.error(request, "A product is unavailable.")
            return redirect("cart")
        except ValueError as error:
            messages.error(request, str(error))
            return redirect("cart")

        request.session["cart"] = {}
        return redirect("demo_payment", order_id=order.id)

    return render(request, "shop/checkout.html", {
        "items": items,
        "total": total,
    })


def demo_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.payment_status = "DEMO_PAID"
        order.save(update_fields=["payment_status"])
        return redirect("order_confirmation", order_id=order.id)

    return render(request, "shop/payment.html", {"order": order})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        "shop/order_confirmation.html",
        {"order": order},
    )
