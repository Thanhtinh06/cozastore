from django.urls import path, re_path
from store.views import *

app_name = 'store'

urlpatterns = [
    path('', index, name="index"),
    path('product/<int:pk>', product, name="product"),
    path('product-detail/<int:pk>', product_detail, name="product_detail"),
    path('contact/', contact, name="contact"),
    path('about/', about, name="about"),
    path('search/', search_product, name="search"),
    path('filter/', filter_product, name="filter"),
    path('product-service/', product_service, name="product_service"),
    # path('blog/', blog, name="blog"),
    # path('blog-detail/', blog_detail, name="blog_detail"),



]
