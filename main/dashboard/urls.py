from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    # --- CATEGORY ---
    path('category-list/', views.category_list, name='category_list'),
    path('category-create/', views.category_create, name='category_create'),
    path('category-delete/<str:code>/', views.category_delete, name='category_delete'),
    # --- PRODUCT ---
    path('product-list/', views.product_list, name='product_list'),
    path('product-create/', views.product_create, name='product_create'),
    path('product-detail/<str:code>/', views.product_detail, name='product_detail'),
    path('product-delete/<str:code>/', views.product_delete, name='product_delete'),
    # --- ENTER ---
    path('enter-list/', views.enter_list, name='enter_list'),
    path('enter-create/', views.enter_create, name='enter_create'),
    path('enter-delete/<str:code>/', views.enter_delete, name='enter_delete'),
    # --- OUT ---
    path('out-list/', views.out_list, name='out_list'),
    path('out-create/', views.out_create, name='out_create'),
    path('out-delete/<str:code>/', views.out_delete, name='out_delete'),
    path('order-return/<str:code>/', views.order_return, name='order_return'),
    # --- ORDER ---
    path('order-list/', views.order_list, name='order_list'),
    path('order-create/', views.order_create, name='order_create'),
    path('order-delete/<str:code>/', views.order_delete, name='order_delete'),
    # --- ORDER PRODUCT ---
    path('order-product-list/', views.order_product_list, name='order_product_list'),
    path('order-product-list/<str:code>/', views.order_product_list, name='order_product_list'),
    path('order-product-create/', views.order_product_create, name='order_product_create'),
    path('order-product-delete/<str:code>/', views.order_product_delete, name='order_product_delete'),
]