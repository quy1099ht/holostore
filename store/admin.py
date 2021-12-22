from django.contrib import admin
from .models import Product, Payment, Cart,Customer,Offer,Comment

class ProductAdmin(admin.ModelAdmin):
     list_display = ('name','tag', 'price', 'stock', 'description')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('total_price','username','datetime')

class CartsAdmin(admin.ModelAdmin):
    list_display = ('user','price','item','quantity', 'ordered_date', 'ordered', 'img_url')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username','name','password', 'email')

class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'Off_description', 'discount')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('username','product_name', 'comment')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart, CartsAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment,CommentAdmin)