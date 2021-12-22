from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache

from store.admin import CartsAdmin
from .models import Comment, Offer, Product, Payment, Customer, Cart
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import hashlib


# Create your views here.
@never_cache
def home(request):
    try:
        user = request.session.get('user')
        username = Customer.objects.get(username=user)
        return render(request, "home.html", {
            'user': user,
            'username': username.name
        })
    except:
        return render(request, "home.html", {'user': user})

@never_cache
def homes(request):
    return redirect('/')

@never_cache
def products(request):
    user = request.session.get('user')
    products = Product.objects.all()
    try:

        username = Customer.objects.get(username=user)
        return render(request, 'products.html', {
            'user': user,
            'products': products,
            'username': username.name,
            'search' : "",
            'search_state' : False
        })
    except:
        return render(request, 'products.html', {
            'user': user,
            'products': products,
            'search' : "",
            'search_state' : False
        })

@never_cache
def showProduct(request):
    if request.method == "POST":
        name = request.POST['pname']
        products = Product.objects.all()
        product = Product.objects.get(name=name)
        comments = Comment.objects.filter(product_name=product.name)
        user = request.session.get('user')
        try:
            username = Customer.objects.get(username=user)
            return render(
                request, 'sproduct.html', {
                    'user': user,
                    'product': product,
                    'username': username.name,
                    'comments': comments
                })
        except:
            return render(request, 'sproduct.html', {
                'user': user,
                'product': product,
                'comments': comments
            })

@never_cache
def login(request):
    if request.session.get("user") == None:
        if request.method == "POST":
            user_name = request.POST['user']
            password = request.POST['pass']
            if checkLogin(user_name, password):
                request.session['user'] = user_name
                user = request.session.get('user')
                request.session['name'] = get_name(user)
                return redirect('/')
            else:
                user = None
                fail = True
                return render(request, 'login.html', {'user': user, 'fail': fail})
        else:
            return render(request, 'login.html', {'user': None})
    else:
        return redirect("/")


def logout(request):
    del request.session['user']
    del request.session['name']
    return redirect('/')


def addpayment_to_db():
    addpayemnt = Payment.objects.create(amount=Payment.amount,
                                        ptype=Payment.ptype,
                                        datetime=timezone.now())

def check_customer(user):
    try:
        a = Customer.objects.get(username = user)
        return True
    except:
        return False
def register(request):
    if check_customer(request.POST['user']):
        return render(request, 'login.html', {'user': None, 'exist' : True})
    regis = Customer.objects.create(
        username=request.POST['user'],
        password=hash_password(request.POST['password']),
        email=request.POST['email'],
        name=request.POST['name'])
    return redirect('/login')


def compare_password(password, dbpass):
    hashpass = hash_password(password)
    if (hashpass == dbpass):
        return True
    return False


def hash_password(password):
    result = hashlib.md5(password.encode())
    return result.hexdigest()


def checkLogin(user, password):
    try:
        cus = Customer.objects.get(username=user)
    except:
        return False
    if compare_password(password, cus.password):
        return True
    return False


def get_name(user):
    try:
        username = Customer.objects.get(username=user)
        return username.name
    except:
        return ""

@never_cache
def add_product(request):
    if request.method == "POST":
        upload_file = request.FILES['productIMG']
        fs = FileSystemStorage(location='media/img/Featured')
        fs.save(upload_file.name, upload_file)
        name = request.POST['name']
        tag = request.POST['tag']
        price = request.POST['price']
        stock = request.POST['stock']
        desciption = request.POST['description']
        img_url = 'img/Featured/' + upload_file.name
        Product.objects.update_or_create(
            name = name,
            tag = tag,
            price = price,
            stock = stock,
            description = desciption,
            image_url = img_url
        )
        return redirect('/products')
    try:
        user = request.session.get('user')
        username = Customer.objects.get(username=user)
        return render(request, "add_product.html", {
            'user': user,
            'username': username.name
        })
    except:
        return render(request, "home.html", {'user': user})

@never_cache
def cart(request):
    if request.method == "POST":
        pname = request.POST['pname']
        price = request.POST['price']
        quantity = request.POST['quantity']
        user = request.session.get('user')
        

        if checkExistItem(pname, user):
            update_product(user, pname, int(quantity))
            return redirect('/cart')
        item = Cart.objects.create(
            user=user,
            price=price,
            item=pname,
            quantity=quantity,
            ordered=True,
            img_url = get_img_url(pname)
        )
        return redirect('/products')
    user = request.session.get('user')    
    carts = Cart.objects.filter(user=user)
    try:
        username = Customer.objects.get(username=user)
        return render(request, "shopcart.html", {
            'user': user,
            'carts': carts,
            'username': username.name
        })
    except:
        return redirect('/')


def checkExistItem(pname, user):
    try:
        a = Cart.objects.get(user=user, item=pname)
        print(a.item)
        return True
    except:
        return False

def get_img_url(pname):
    product = Product.objects.get(name = pname)
    return product.image_url
@never_cache
def profie(request):
    try:
        user = request.session.get('user')
        username = Customer.objects.get(username=user)
        if request.method == "POST":
            username.fullname = request.POST['fullname']
            username.birthday = request.POST['birthday']
            username.gender = request.POST['gender']
            username.email = request.POST['email']
            username.save()
            return redirect('/user')

        payments = Payment.objects.filter(username = user) 

        coupons = Offer.objects.all()

        return render(request, "profile.html", {
            'user': user,
            'username': username.name,
            'customer' : username,
            'payment' : payments,
            'coupons' : coupons,
        })
    except:
        return redirect("/")

# def update_customer():
#     try:
#         obj = Customer.objects.get(field=value)
#         obj.field = new_value
#         obj.save()
#     except Customer.DoesNotExist:
#         obj = Customer.objects.create(field=new_value)

def update_product(user, name, quantity):
    item = Cart.objects.get(user=user, item=name)
    quantity += int(item.quantity)
    item.quantity = quantity
    item.save()


def search(request):
    if request.method == "GET":
        user = request.session.get('user')
        search_product = request.GET['sname']
        products = search_all(search_product)
        count = search_count(search_product)
        try:
            username = Customer.objects.get(username=user)
            return render(request, 'products.html', {
                'user': user,
                'products': products,
                'username': username.name,
                'search' : search_product,
                'search_state': True,
                'count' : count
            })
        except:
            return render(request, 'products.html', {
                'user': user,
                'products': products,
                'search' : search_product,
                'search_state': True,
                'count' : count
            })


def search_all(search_product):
    try:
        products = Product.objects.get(name=search_product)
        return products
    except Exception:
        pass
    try:
        products = Product.objects.filter(tag=search_product)
        return products
    except:
        return Product.objects.all()

def search_count(search_product):
    try:
        products = Product.objects.get(name=search_product)
        return 1
    except Exception:
        print("Ok")
        pass
    try:
        products = Product.objects.filter(tag=search_product)
        return products.count()
    except:
        print("OK")
        return Product.objects.all()
@never_cache
def about(request):
    try:
        user = request.session.get('user')
        username = Customer.objects.get(username=user)
        return render(request, "about.html", {
            'user': user,
            'username': username.name
        })
    except:
        return render(request, "about.html", {'user': user})

def update(request):
    user = request.session.get('user')
    username = Customer.objects.get(username=user)
    if request.method == "POST":
        username.address = request.POST['adress']
        username.zipcode = request.POST['zipcode']
        username.phone = request.POST['phone']
        username.redeem_card = request.POST['redeem_card']
        username.save()
        return redirect('/user')
    return redirect("/user")

def check_out(request):
    if request.method == "POST":
        user = request.session.get('user')
        Payment.objects.create(
            total_price = request.POST['total_price'],
            username = user,
            datetime = timezone.now()
        )
        Cart.objects.filter(user = user).delete()
    return redirect('/')

def up_avatar(request):
    user = request.session.get('user')
    customer = Customer.objects.get(username = user)
    url = "img/avatar/"
    if request.method == "POST":
        upload_file = request.FILES['avatar']
        avatar_url = customer.avatar_url
        print(avatar_url)
        if avatar_url != "":
            delete_old_avatar(avatar_url)
        
        fs = FileSystemStorage(location='media/img/avatar')
        fs.save(upload_file.name, upload_file)
        customer.avatar_url = url + upload_file.name
        customer.save()
    return redirect('/user')

def delete_old_avatar(avatar_url):
    avatar = avatar_url.replace("img/avatar/","")
    fs = FileSystemStorage(location='media/img/avatar')
    fs.delete(avatar)
@never_cache
def translator(request):
    try:
        user = request.session.get('user')
        username = Customer.objects.get(username=user)
        return render(request, "translator.html", {
            'user': user,
            'username': username.name
        })
    except:
        return render(request, "translator.html", {'user': user})
@never_cache
def promote(request):
    try:
        user = request.session.get('user')
        username = Customer.objects.get(username=user)
        return render(request, "promote.html", {
            'user': user,
            'username': username.name
        })
    except:
        return render(request,"promote.html", {'user' : user})

def test(request):
    return render(request,"test.html")
@never_cache
def calculator(request):
    return render(request,"caculator.html")
@never_cache
def handle_404(request, exception):
    try:
        user = request.session.get('user')
        username = Customer.objects.get(username=user)
        return render(request, "404.html", {
            'user': user,
            'username': username.name
        })
    except:
        return render(request,"404.html", {'user' : user})