from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home),
    path("translate",views.translate),
    path('cart',views.deleteFromCart),
    path('comment',views.addComment),
    path('coupon',views.get_coupon),
    path('translator',views.translator),
    path('checkLogin',views.check_login),
]
