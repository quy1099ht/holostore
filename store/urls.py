from django.urls import path
from . import views
from django.conf.urls import handler404

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home),
    path('homes',views.homes),
    path('products',views.products),
    path('product', views.showProduct),
    path('login',views.login),
    path('logout',views.logout),
    path('register',views.register),
    path('cart',views.cart),
    path('user',views.profie),
    path('search',views.search),
    path('add_product', views.add_product),
    path('about',views.about),
    path('update',views.update),
    path('check_out',views.check_out),
    path('up_avatar',views.up_avatar),
    path('translator',views.translator),
    path('promote',views.promote),
    path('calculator',views.calculator),
    path('test',views.test),
]


handler404 = 'store.views.handle_404'