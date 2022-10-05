from django.shortcuts import render, redirect
from customer.forms import *
from customer.models import *
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from cart.models import Order, OrderItem
from cart.models import Customer
from cart.cart import Cart
from customer.forms import *
from customer.libs import *


# #sai cai nao import cai do
# from django.contrib.auth.hashers import Argon2PasswordHasher
#  BCryptPasswordHasher, CryptPasswordHasher

# Create your views here.


def customer_login(request):

    # kiem tra trang thai session truoc khi show giao dien dang nhap/ dang ki. Neu session da ton tai roi se ko truy cap vao link dang nhap duoc nua
    if 'session_customer' in request.session:
        return redirect('store:index')

    form_signup = FormSignUp()
    result_login = ''

    # Login
    if request.POST.get('btnLogin'):

        form_signup = FormSignUp(request.POST, Customer)
        # Gan bien
        hasher = PBKDF2PasswordHasher()
        username = request.POST.get('username')
        password = request.POST.get('password')
        encoded = hasher.encode(password, 'a')

        customer = Customer.objects.filter(username=username, password=encoded)

        # Nhap dung: <QuerySet [<Customer: Nguyễn Thanh Tịnh>]>
        # Nhap sai: <QuerySet []>

        if customer.count() > 0:
            # print(customer.values())
            # In ra gia tri: <QuerySet [{'id': 3, 'first_name': 'Thanh Tịnh', 'username': 'Nguyễn', 'email': 'nguyenthithanhtinh06@gmail.com', 'tel': '0943165820', 'address': 'S2.03 Vinhomes Grand Park, Nguyễn Xiển', 'password': '123', 'confirm_password': '123'}]>
            # print(customer.values()[0])
            # In ra gia tri: {'id': 3, 'first_name': 'Thanh Tịnh', 'username': 'Nguyễn', 'email': 'nguyenthithanhtinh06@gmail.com', 'tel': '0943165820', 'address': 'S2.03 Vinhomes Grand Park, Nguyễn Xiển', 'password': '123', 'confirm_password': '123'}
            # tao session
            request.session['session_customer'] = customer.values()[0]
            # khai bao duong link chuyen den giong nhu khai bao trong file html
            return redirect('store:index')

            # result_login = '''
            # <div class="alert alert-success" role="alert">
            #     You have successfully logined!
            # </div>
            # '''
        else:
            result_login = '''
            <div class="alert alert-danger" role="alert">
                You haven't successfully logined. Please check your information and try again !
            </div>
            '''

    return render(request, "store/login.html", {
        'form_signup': form_signup,
        'result_login': result_login,
    })


def customer_register(request):
    # kiem tra trang thai session truoc khi show giao dien dang nhap/ dang ki. Neu session da ton tai roi se ko truy cap vao link dang nhap duoc nua
    if 'session_customer' in request.session:
        return redirect('store:index')

    # Register
    form_signup = FormSignUp()
    result_signup = ''
    if request.POST.get('btnRegister'):
        form_signup = FormSignUp(request.POST, Customer)
        if form_signup.is_valid() and form_signup.cleaned_data['password'] == form_signup.cleaned_data['confirm_password']:
            hasher = PBKDF2PasswordHasher()
            request.POST._mutable = True
            post = form_signup.save(commit=False)
            post.customer_name = form_signup.cleaned_data['customer_name']
            post.username = form_signup.cleaned_data['username']
            post.tel = form_signup.cleaned_data['tel']
            post.email = form_signup.cleaned_data['email']
            post.address = form_signup.cleaned_data['address']
            post.password = form_signup.cleaned_data['password']
            post.confirm_password = form_signup.cleaned_data['confirm_password']
            # ma hoa password, endcode co them salt: chuoi 1 so ki ti
            # salt: yeu cau toi yhieu 1 byte
            post.password = hasher.encode(
                form_signup.cleaned_data['password'], 'a')
            # post.password = hasher.encode(form_signup.cleaned_data['password'],'a') #salt: yeu cau toi thieu 8 byte
            post.confirm_password = hasher.encode(
                form_signup.cleaned_data['confirm_password'], 'a')
            post.save()

            # Gui mail
            # subject = 'Dang Ky tai Khoan moi' + post.email
            # content = 'Chao mung...'
            # '''
            # email_host_user
            # '''

            result_signup = '''
            <div class="alert alert-success" role="alert">
                You have successfully registered!
            </div>
            '''
        else:
            result_signup = '''
            <div class="alert alert-danger" role="alert">
                You haven't successfully registered. Please check your information and try again !
            </div>
            '''

    return render(request, "store/register.html", {
        'form_signup': form_signup,
        'result_signup': result_signup
    })


def customer_logout(request):
    # xoa session hien tai

    # kiem tra ton tai session
    if 'session_customer' in request.session:
        del request.session['session_customer']

    return redirect('store:index')


def user_profile(request):

    return render(request, "store/users-profile.html")


def my_account(request):
    cart = Cart(request)

    if 'session_customer' not in request.session:
        return redirect('customer:customer_login')

    # Cap nhat thong tin khach hang
    result_update_info = ''
    if request.POST.get('btnUpdate'):
        # Gan bien
        customer_name = request.POST.get('customer_name')
        username = request.POST.get('username')
        tel = request.POST.get('tel')
        # email = request.POST.get('email')
        address = request.POST.get('address')

        # Cap nhat vao CSDL
        customer = Customer.objects.get(
            id=request.session['session_customer']['id'])
        customer.customer_name = customer_name
        customer.username = username
        customer.tel = tel
        customer.address = address

        customer.save()

        # Cap nhat vao session
        request.session['session_customer']['customer_name'] = customer_name
        request.session['session_customer']['username'] = username
        request.session['session_customer']['tel'] = tel
        request.session['session_customer']['address'] = address

        print(request.session['session_customer'])

        # Thong bao ket qua

        result_update_info = '''
            <div class="alert alert-success" role="alert">
                You have successfully updated!
            </div>
            '''

    result_change_password = ''
    current_password = ''
    new_password = ''
    confirm_new_password = ''
    # Đổi mật khẩu
    if request.POST.get('btnChangePassword'):
        # Gan bien
        hasher = PBKDF2PasswordHasher()
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Check mk
        if hasher.encode(current_password, 'a') == request.session['session_customer']['password'] and new_password == confirm_new_password:
            # Cap nhat CSDL
            customer = Customer.objects.get(
                id=request.session['session_customer']['id'])
            customer.password = hasher.encode(new_password, 'a')
            customer.confirm_password = hasher.encode(
                confirm_new_password, 'a')
            customer.save()

            # Cap nhat vao session
            request.session['session_customer']['password'] = hasher.encode(
                new_password, 'a')
            request.session['session_customer']['confirm_password'] = hasher.encode(
                confirm_new_password, 'a')

            # Thong bao ket qua

            result_change_password = '''
                <div class="alert alert-success" role="alert">
                    You have successfully changed new password!
                </div>
            '''
        else:
            result_change_password = '''
                <div class="alert alert-danger" role="alert">
                    You haven't successfully changed new password. Please check your information and try again !
                </div>
                '''

    # Hien thi Order
    # id_customer = request.session['session_customer']['id']
    # all_order = Order.objects.filter(customer_id=id_customer)

    # dict_id_order = all_order.values('id')
    # list_id_order = []
    # for item in dict_id_order:
    #     list_id_order.append(item['id'])

    # # detail_order = {}
    # detail_order = []
    # for i in list_id_order:
    #     order_item = OrderItem.objects.filter(order_id=i)
    #     detail_order.append(order_item)

    return render(request, "store/my-account.html", {
        'result_update_info': result_update_info,
        'result_change_password': result_change_password,
        'current_password': current_password,
        'new_password': new_password,
        'confirm_new_password': confirm_new_password,
        'cart': cart,
        # 'all_order': all_order,
        # 'detail_order': detail_order,
        # 'list_id_order': list_id_order,

    })
