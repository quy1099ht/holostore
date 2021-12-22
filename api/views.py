from json.encoder import JSONEncoder
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.translation import to_language

from store.models import Comment, Customer, Cart, Offer, Product
from . import transtext
from django.core.files.storage import FileSystemStorage
import json
from store.views import compare_password,hash_password,checkLogin

# Create your views here.
def home(request):
    user = request.session.get('user')
    return render(request, "home.html", {'user' : user})


def translate(request):
    words = request.GET['words']
    try:
        language = "" + request.GET['language']
    except:
        language = "vi"
    response_data = {}
    response_data['result'] = transtext.transText(words,"en",language)
    print("Result = " + transtext.transText(words,"en",language))
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

def translator(request):
    words = request.GET['words']
    try:
        language = "" + request.GET['language']
    except:
        language = "en"

    try:
        to_language = "" + request.GET['toLang']
    except:
        to_language = "vi"
    
    response_data = {}
    response_data['result'] = transtext.transText(words,language,to_language)
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

def checkExistAccount(request):
    
    if request.method == "POST":
        cus = Customer.objects.all()
        for custom in cus:
            if custom.username == request.POST['username'] and custom.email == request.POST['email']:
                acc = {}
                acc['Existed'] = "True"
                return JsonResponse(acc,safe= False, json_dumps_params={'ensure_ascii' : False})  
            else:
                acc = {}
                acc['Existed'] = "False"
                return JsonResponse(acc,safe= False, json_dumps_params={'ensure_ascii' : False})  

def deleteFromCart(request):
    username = request.session.get('user')
    proname = request.GET['pname']

    item = Cart.objects.filter(user = username,item = proname)
    item.delete()
    response = {}
    response['response'] = "Deleted"
    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

def add_product(request):
    if request.method == "POST":
        upload_file = request.FILES['fileUP']
        print(upload_file.name)
        print(upload_file.size)
        fs = FileSystemStorage()
        fs.save(upload_file.name,upload_file)
    return render(request,"store/upfile.html")

def addComment(request):
    username = request.session.get('name')
    if request.method == "GET":
        comment = request.GET['comment']
        pname = request.GET['pname']
        Comment.objects.create(
            username = username,
            product_name = pname,
            comment = comment
        )
    response = {}
    response['response'] = "" + username
    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

def check_coupon(code):
    try:
        Offer.objects.get(code = code)
        return True
    except:
        return False

def get_coupon(request):
    code = request.GET['code']
    subtotal = float(request.GET['subtotal'])
    
    response = {}
    if check_coupon(code):
        offer = Offer.objects.get(code = code)
        discount = (offer.discount/100) * subtotal

        response['discount'] = discount
    else:
        response['discount'] = "0"
    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

def check_username(username):
    try:
        customer = Customer.objects.get(username = username)
        return True
    except:
        return False

def check_login(request):
    username = request.GET['username']
    password = request.GET['password']
    response = {}
    
    if check_username(username):
        response['user'] = "True"
        if check_login(username,password):
            response['password'] = "True"
        else:
            response['password'] = "False"
    else:    
        response['user'] = "False"
    print(response['user'])
    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})
    