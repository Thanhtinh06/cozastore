from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import *
from store.models import *
from django.views.decorators.http import require_POST
from cart.models import *
from customer.models import *


# Create your views here.
def cart_detail(request):
    cart = Cart(request)

    # Ma giam gia (Coupon)

    list_coupon = [
        {'TTTH': 0.8},
        {'TTINH': 0.9},
        {'VOILUN': 0.7}
    ]

    coupon_code = ''
    coupon_natural = 1
    if request.POST.get('btnCouponCode'):
        coupon_code = request.POST.get('coupon_code')
        for dict_coupon in list_coupon:
            if coupon_code in dict_coupon:
                cart_new = {}
                coupon_natural = dict_coupon[coupon_code]
                for c in cart:
                    product_cart = {
                        str(c['product'].pk): {
                            'quantity': c['quantity'],
                            'price': str(c['product'].price_sell),
                            'coupon': str(dict_coupon[coupon_code])
                        }
                    }
                    cart_new.update(product_cart)

                    # giữ lại thong tin giam gia trên ô tại thời điểm click nút
                    c['coupon'] = dict_coupon[coupon_code]
                else:
                    # Update session Cart => đè cart new lên cart đã tồn tại
                    request.session['cart'] = cart_new
                break
            else:
                cart_new = {}
                for c in cart:
                    product_cart = {
                        str(c['product'].pk): {
                            'quantity': c['quantity'],
                            'price': str(c['product'].price_sell),
                            'coupon': str(coupon_natural)
                        }
                    }
                    cart_new.update(product_cart)

                    # giữ lại thong tin giam gia trên ô tại thời điểm click nút
                    c['coupon'] = coupon_natural
                else:
                    # Update session Cart => đè cart new lên cart đã tồn tại
                    request.session['cart'] = cart_new

    # Update cart
    if request.POST.get('btnUpdateCart'):
        cart_new = {}
        for c in cart:
            quantity_new = int(request.POST.get(
                'quantity2' + str(c['product'].pk)))
            print(quantity_new)

            if quantity_new != 0:
                product_cart = {
                    str(c['product'].pk): {'quantity': quantity_new,
                                           'price': str(c['product'].price_sell),
                                           'coupon': str(c['coupon'])}
                }
                cart_new.update(product_cart)

                # giữ lại số lượng mới trên ô tại thời điểm click nút
                c['quantity'] = quantity_new
            else:
                # Xóa sản phẩm ra khỏi giỏ hàng khi sản phẩm mới = 0
                cart.remove(c['product'])
        else:
            # Update session Cart => đè cart new lên cart đã tồn tại
            request.session['cart'] = cart_new

    return render(request, "store/shoping-cart.html", {
        'cart': cart,
        'coupon_code': coupon_code
    })


@ require_POST
def buy_now(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('quantity'):
        cart.add(product, int(request.POST.get('quantity')))
    if request.POST.get('btn_add2'):
        quantity = request.POST.get('quanlity')
        cart.add(product, int(quantity))

    return redirect('cart:cart_detail')


@ require_POST
def remove_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def checkout(request):
    # kiem tra trang thai dang nhap cua khach hang
    if 'session_customer' not in request.session:
        return redirect('cart:cart_detail')

    # Doc thong tin gioi hang tu session cart
    cart = Cart(request)

    # Thuc hien dat hang
    if request.POST.get('btnBuy'):
        # Lay thong tin nguoi dat hang
        customer = Customer.objects.get(
            pk=request.session.get('session_customer')['id'])
        # Order
        order = Order()
        order.total = cart.get_final_total_price()
        order.customer = customer
        order.save()
        # OderItem
        for c in cart:
            # order dau tien la thuoc tinh class oderitem, order thu 2 la bien order phia tren
            OrderItem.objects.create(order=order,
                                     product=c['product'],
                                     price=c['price'],
                                     quantity=c['quantity'],
                                     )
        # Xoa session cart khi mua hang thanh cong
        cart.clear()
        return render(request, "store/result.html", {
            'cart': cart,
        })

        # Khi bam nut dat hang 3 hành động trên sẽ thực hiện cùng lúc
    return render(request, "store/checkout.html", {
        'cart': cart
    })


def wishlist(request):
    return render(request, "store/wishlist.html")
