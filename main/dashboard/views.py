from django.shortcuts import render, redirect
from .. import models
from datetime import datetime



def staff_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            result = func(request, *args, **kwargs)
        else:
            return redirect('auth:login')
        return result
    return wrapper



@staff_required 
def index(request):
    context = {}
    return render(request, 'dashboard/index.html', context)

# ---------- CATEGORY ----------

@staff_required 
def category_list(request):
    queryset = models.Category.objects.all()
    return render(request, 'dashboard/category/list.html', {'queryset':queryset})

@staff_required 
def category_create(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name = request.POST['name']
        )
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/category/create.html')

@staff_required 
def category_delete(request, code):
    queryset = models.Category.objects.get(code=code)
    queryset.delete()
    return redirect('dashboard:category_list')

# ---------- PRODUCT ----------

@staff_required
def product_list(request):
    queryset = models.Product.objects.all()
    return render(request, 'dashboard/product/list.html', {'queryset':queryset})

@staff_required
def product_create(request):
    categories = models.Category.objects.all()
    if request.method == 'POST':
        discount_price = request.POST.get('discount_price')
        models.Product.objects.create(
            name = request.POST.get('name'),
            category = models.Category.objects.get(code=request.POST.get('category_code')),
            price = float(request.POST.get('price')),
            discount_price = float(discount_price) if discount_price else None,
            quantity = 0,
            banner_image = request.FILES.get('banner_image'),
        )
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/create.html', {'categories':categories})

@staff_required
def product_detail(request, code):
    queryset = models.Product.objects.get(code=code)
    images = models.ProductImage.objects.filter(product=queryset)
    videos = models.ProductVideo.objects.filter(product=queryset)
    context = {
        'product':queryset,
        'images':images,
        'videos':videos,
    }
    return render(request, 'dashboard/product/detail.html', context)

@staff_required
def product_delete(request, code):
    models.Product.objects.get(code=code).delete()
    return redirect('dashboard:product_list')
    

# ---------- ENTER ----------

@staff_required
def enter_list(request):
    queryset = models.Enter.objects.all()
    return render(request, 'dashboard/enter/list.html', {'queryset':queryset})

@staff_required
def enter_create(request):
    queryset = models.Product.objects.all()
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST['code'])
        quantity = request.POST['quantity']
        models.Enter.objects.create(
            product=product,
            quantity=int(quantity),
            date = datetime.now()
        )
        return redirect('dashboard:enter_list')
    return render(request, 'dashboard/enter/create.html', {'queryset':queryset})

@staff_required
def enter_delete(request, code):
    models.Enter.objects.get(code=code).delete()
    return redirect('dashboard:enter_list')

# ---------- OUT ----------

@staff_required
def out_list(request):
    queryset = models.Out.objects.all()
    return render(request, 'dashboard/out/list.html', {'queryset':queryset})

@staff_required
def out_create(request):
    queryset = models.Product.objects.all()
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST['code'])
        quantity = request.POST['quantity']
        models.Out.objects.create(
            product=product,
            quantity=int(quantity),
        )
        return redirect('dashboard:out_list')
    return render(request, 'dashboard/out/create.html', {'queryset':queryset})

@staff_required
def out_delete(request, code):
    models.Out.objects.get(code=code).delete()
    return redirect('dashboard:out_list')

# ---------- ORDER ----------

@staff_required
def order_list(request):
    queryset = models.Order.objects.all()
    return render(request, 'dashboard/order/list.html', {'queryset':queryset})

@staff_required
def order_create(request):
    if request.method == 'POST':
        models.Order.objects.create(
            name=request.POST['name'],
            is_returned=False,
        )
        return redirect('dashboard:order_list')
    return render(request, 'dashboard/order/create.html')

@staff_required
def order_delete(request, code):
    models.Order.objects.get(code=code).delete()
    return redirect('dashboard:order_list')

def order_return(request, code):
    order = models.Order.objects.get(code=code)
    order.is_returned = True
    order.save
    return redirect('dashboard:order_list')

# ---------- ORDER PRODUCT ----------

@staff_required
def order_product_list(request, code):
    if code:
        queryset = models.OrderProduct.objects.filter(order__code = code)
    else:
        queryset = models.OrderProduct.objects.all()
    return render(request, 'dashboard/order_product/list.html', {'queryset':queryset})

@staff_required
def order_product_create(request):
    products = models.Product.objects.all()
    orders = models.Order.objects.all()
    if request.method == 'POST':
        models.OrderProduct.objects.create(
            product = models.Product.objects.get(code=request.POST.get('product_code')),
            order = models.Order.objects.get(code=request.POST.get('order_code')),
            quantity = request.POST.get('quantity')
        )
        models.Out.objects.create(
            product = models.Product.objects.get(code=request.POST.get('product_code')),
            quantity = request.POST.get('quantity'),
        )
        return redirect('dashboard:order_list')
    return render(request, 'dashboard/order_product/create.html', {'products':products, 'orders':orders})

@staff_required
def order_product_delete(request, code):
    models.OrderProduct.objects.get(code=code).delete()
    return redirect('dashboard:order_product_list')
