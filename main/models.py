from django.db import models
from random import sample
import string
import os
from datetime import datetime
import qrcode
from PIL import Image
from io import BytesIO

class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 
    
    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True

    
class Category(CodeGenerate):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    def products(self):
        return Product.objects.filter(category=self)


class Product(CodeGenerate):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount_price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    banner_image = models.ImageField(upload_to='banner-image/')
    qrcode_img = models.ImageField(blank=True, upload_to='qrcode-img/')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.name, box_size=15)
        qr_image_pil = qr_image.get_image()
        stream = BytesIO()
        qr_image_pil.save(stream, format='PNG')
        self.qrcode_img.save(f"{self.name}.png", BytesIO(stream.getvalue()), save=False)
        super(Product, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.banner_image:
            banner_image_path = self.banner_image.path
            if os.path.exists(banner_image_path):
                os.remove(banner_image_path)
        if self.qrcode_img:
            qrcode_img_path = self.qrcode_img.path
            if os.path.exists(qrcode_img_path):
                os.remove(qrcode_img_path)
        super(Product, self).delete(*args, **kwargs)

    def status(self):
        return bool(self.quantity)


class ProductImage(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-image/')

    def __str__(self):
        return self.product.name
    
    def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        super(ProductImage, self).delete(*args, **kwargs)


class ProductVideo(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    video = models.FileField(upload_to='product-video/')

    def __str__(self):
        return self.product.name
    
    def delete(self, *args, **kwargs):
        if self.video:
            video_path = self.video.path
            if os.path.exists(video_path):
                os.remove(video_path)
        super(ProductVideo, self).delete(*args, **kwargs)


class Enter(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if self.pk:
           enter = Enter.objects.get(id=self.id)
           self.product.quantity -= enter.quantity
        self.product.quantity += self.quantity
        self.product.save()
        super(Enter, self).save(*args, **kwargs)


class Out(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if self.pk:
            out = Out.objects.get(id=self.id)
            self.product.quantity += out.quantity
        if (self.product.quantity - int(self.quantity)) >= 0:
            self.product.quantity -= int(self.quantity)
            self.product.save()
            super(Out, self).save(*args, **kwargs)
        else:
            raise ValueError('Mahsulot soni bilan xatolik!')

class Order(CodeGenerate):
    name = models.CharField(max_length=255) # Buyurtmachi ismi
    date = models.DateTimeField(auto_now_add=True) # Buyurtma vaqti
    is_returned = models.BooleanField(default=False) # False ---> Jo'natilgan | True ---> Qaytarilgan

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_returned:
            products = OrderProduct.objects.filter(order=self)
            for product in products:
                Enter.objects.create(
                    product = product.product,
                    quantity = product.quantity,
                    date = datetime.now()
                )
        super(Order, self).save(*args, **kwargs)
    
    @property
    def total_quantity(self): # ---> Barcha mahsulotlar umumiy sonini qaytaradi
        quantity = 0
        queryset = OrderProduct.objects.filter(order=self)
        for q in queryset:
            quantity += q.quantity
        return quantity
    
    @property
    def total_price(self): # ---> Chegirmalar hisobga olinmagan umumiy qiymatni qaytaradi
        price = 0
        queryset = OrderProduct.objects.filter(order=self)
        for q in queryset:
            price += q.price
        return price

    @property
    def total_discount_price(self): # ---> Chegirmalar hisobga olingan umumiy qiymatni qaytaradi
        discount_price = 0
        queryset = OrderProduct.objects.filter(order=self)
        for q in queryset:
            discount_price += q.discount_price
        return discount_price


class OrderProduct(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name
    
    @property
    def price(self):
        return self.quantity * self.product.price
    
    @property
    def discount_price(self):
        if self.product.discount_price:
            return self.quantity * self.product.discount_price
        else:
            return self.quantity * self.product.price
    
        
    
    
    

