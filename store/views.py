from unicodedata import category
from django.shortcuts import render
from idna import alabel
from store.models import Contact, Product, Status, Category
from django.core.paginator import Paginator
from cart.cart import Cart
from store.views import Cart
from rest_framework import viewsets, permissions
from store.serializers import ProductSerializer
from django.http import JsonResponse
# Create your views here.


def index(request):
    all_product = Product.objects.all()
    category = Category.objects.all().order_by('name')
    glasses = Product.objects.filter(
        category_id=2).order_by('-public_day')[0:10]
    wallets = Product.objects.filter(
        category_id=4).order_by('-public_day')[0:10]
    bags = Product.objects.filter(category_id=1).order_by('-public_day')[0:10]
    shoes = Product.objects.filter(category_id=3).order_by('-public_day')[0:10]
    jewellery = Product.objects.filter(
        category_id=5).order_by('-public_day')[0:10]
    page = request.GET.get('page', 1)
    paginator = Paginator(all_product, 20)
    product_pager = paginator.page(page)
    cart = Cart(request)

    return render(request, "store/index.html", {
        'all_product': product_pager,
        'category': category,
        'glasses': glasses,
        'wallets': wallets,
        'bags': bags,
        'shoes': shoes,
        'jewellery': jewellery,
        'cart': cart

    })


def product(request, pk):
    cart = Cart(request)

    all_product = Product.objects.all()
    if pk == 0:
        # doc het tat ca san pham
        all_product = Product.objects.all()
    else:
        all_product = Product.objects.filter(
            category_id=pk)

    category = Category.objects.all().order_by('name')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_product, 20)
    product_pager = paginator.page(page)

    return render(request, "store/product.html", {
        'all_product': product_pager,
        'category': category,
        'cart': cart,

    })


def search_product(request):
    cart = Cart(request)
    all_product = Product.objects.all()
    if request.GET.get('search'):
        search = request.GET.get('search')
        all_product = Product.objects.filter(name__contains=search)

    return render(request, "store/product.html", {
        'cart': cart,
        'all_product': all_product,
        'search': search,

    })


def filter_product(request, pk):
    cart = Cart(request)
    all_product = Product.objects.all()
    if pk == 0:
        # newness
        if request.GET.get('filter_new'):
            all_product = Product.objects.all().order_by('-public_day')
        if request.GET.get('low_to_high'):
            all_product = Product.objects.all().order_by('price_buy')
        if request.GET.get('high_to_low'):
            all_product = Product.objects.all().order_by('-price_buy')

    else:
        if request.GET.get('filter_new'):
            all_product = Product.objects.filter(
                category_id=pk).order_by('-public_day')
        if request.GET.get('low_to_high'):
            all_product = Product.objects.filter(
                category_id=pk).order_by('price_buy')
        if request.GET.get('high_to_low'):
            all_product = Product.objects.filter(
                category_id=pk).order_by('-price_buy')

    category = Category.objects.all().order_by('name')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_product, 20)
    product_pager = paginator.page(page)

    return render(request, "store/product.html", {
        'cart': cart,
        'all_product': product_pager,

    })


def product_detail(request, pk):
    cart = Cart(request)

    product = Product.objects.get(id=pk)
    category_id = product.category_id
    category_name = Category.objects.get(id=category_id)
    relate_product = Product.objects.filter(category_id=category_id)

    return render(request, "store/product-detail.html", {
        'product': product,
        'cart': cart,
        'relate_product': relate_product,
        'category_name': category_name
    })


def about(request):
    cart = Cart(request)

    return render(request, "store/about.html", {
        'cart': cart, })


def contact(request):

    cart = Cart(request)

    result_send_mess = ''
    if request.POST.get('btnSend'):
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Khai bao class (model)
        contact = Contact(email=email, message=message)
        contact.save()

        # Thong bao ket qua
        result_send_mess = '''
            <div class="alert alert-success" role="alert">
                You have successfully sent messege!
            </div>
            '''

    return render(request, "store/contact.html", {
        'cart': cart,
        'result_send_mess': result_send_mess,
    })

# Cach1: Xay dung web service truc tiep


def product_service(request):
    products = Product.objects.all()
    result_list = list(products.values(
        'name', 'price_sell', 'price_buy', 'public_day'))

    return JsonResponse(result_list, safe=False)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# def blog(request):
#     cart = Cart(request)

#     return render(request, "store/blog.html", {
#         'cart': cart,
#     })


# def blog_detail(request):
#     cart = Cart(request)

#     return render(request, "store/blog-detail.html", {
#         'cart': cart,
#     })
