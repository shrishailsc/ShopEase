
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
]

path("checkout/", views.checkout, name="checkout"),
path(
    "order-confirmation/<int:order_id>/",
    views.order_confirmation,
    name="order_confirmation",
)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-confirmation/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
]

path("payment/<int:order_id>/", views.demo_payment, name="demo_payment"),
path("payment/<int:order_id>/", views.demo_payment, name="demo_payment"),


from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/<int:order_id>/", views.demo_payment, name="demo_payment"),
    path("order-confirmation/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
]

