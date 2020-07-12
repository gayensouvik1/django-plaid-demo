from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, ItemForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from plaid import Client
from .models import Usertoken
import requests
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
import json

# Create your views here.

public_key = "4eb483032a74b84214ca77f08e427f"
client_id = "5f096140d056f40013f9edd2"
secret = "68a481eea52816de1c1f0805c57927"
public_token = ""
access_token = ""

def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        request.session['currentuser'] = username

        if user is not None:
            login(request, user)
            return redirect('bright:home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'bright/login.html', context)

def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('bright:home')
    # else:
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('bright:login')


    context = {'form':form}
    return render(request, 'bright/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def createItem(request):

    form = ItemForm()
    if request.session.has_key('currentuser'):
        currentUserName = request.session['currentuser']
    else:
        return redirect('bright:login')
    txt = ""
    if request.method == 'POST':

        form = ItemForm(request.POST)
        public_token = get_public_token(public_key, "ins_1")
        access_token = exchange_token(client_id, secret, public_token)
        user = Usertoken(name=currentUserName, access_token=access_token)
        request.session['access_token'] = access_token
        user.save()
        txt = "Account Linked successfully for user "+currentUserName
    return render(request, 'bright/createItem.html',{'form':form, 'hello':txt})

@login_required(login_url='login')
def homePage(request):
    sessiond = "default"
    if request.session.has_key('currentuser'):
        sessiond = request.session['currentuser']

    return render(request, 'bright/home.html', {'data':sessiond})

def accountPage(request):
    # all_user_tokens = Usertoken.objects
    # currentUser = request.session['currentuser']
    # filtered_user_tokens = all_user_tokens.filter(name=currentUser)
    # access_tokens = []
    accountList = []
    access_token = ""
    if request.session.has_key('access_token'):
        access_token = request.session['access_token']

    #
    # for i in filtered_user_tokens:
    #     access_tokens.append(i.access_token)
    accountList.append(getAccountList(client_id, secret, access_token))


    return render(request, 'bright/accounts.html', {'accountList':accountList})


def transactionsPage(request):
    # all_user_tokens = Usertoken.objects
    # currentUser = request.session['currentuser']
    # filtered_user_tokens = all_user_tokens.filter(name=currentUser)
    access_token = ""
    if request.session.has_key('access_token'):
        access_token = request.session['access_token']
    transactionList = getAllTranactions(client_id, secret, access_token)

    return render(request, 'bright/transactions.html', {'transactionList':transactionList})








def getAllTranactions(client_id, secret, access_token):
    url = "https://sandbox.plaid.com/transactions/get"

    payload = "{\n\t\"client_id\": \""+client_id+"\",\n\t\"secret\": \""+secret+"\",\n\t\"access_token\": \""+access_token+"\",\n\t\"start_date\": \"2019-11-10\",\n\t\"end_date\": \"2020-07-12\",\n\t\"options\": {\n\t\t\"count\": 250,\n\t\t\"offset\": 100\n\t}\n}"
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "Plaid Postman",
        'cache-control': "no-cache",
        'Postman-Token': "6269da03-8047-4141-b94d-bab9117ebf0c"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.json()



def get_public_token(public_key,institution_id):

    url = "https://sandbox.plaid.com/sandbox/public_token/create"
    payload = "{\n  \"public_key\": \""+public_key+"\",\n  \"institution_id\": \""+institution_id+"\",\n  \"initial_products\": [\"auth\"],\n  \"options\": {\n    \"webhook\": \"http://21192d63f0e1.ngrok.io/bright/webhook/\"\n  }\n}"
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "Plaid Postman",
        'cache-control': "no-cache",
        'Postman-Token': "6f2c108b-4af0-4fb6-b5e5-03da553e3d49"}


    response = requests.request("POST", url, data=payload, headers=headers)
    dict = response.json()
    return dict['public_token']

def exchange_token(client_id,secret,public_token):

    url = "https://sandbox.plaid.com/item/public_token/exchange"

    payload = "{\n\t\"client_id\": \""+client_id+"\",\n\t\"secret\": \""+secret+"\",\n\t\"public_token\": \""+public_token+"\"\n}"
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "Plaid Postman",
        'cache-control': "no-cache",
        'Postman-Token': "7f4a4374-7a6d-4923-8155-77109c595824"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    dict = response.json()
    return dict['access_token']

def getAccountList(client_id, secret, access_token):

    url = "https://sandbox.plaid.com/accounts/get"

    payload = "{\n\t\"client_id\": \""+client_id+"\",\n\t\"secret\": \""+secret+"\",\n\t\"access_token\": \""+access_token+"\"\n}"
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "Plaid Postman",
        'cache-control': "no-cache",
        'Postman-Token': "9bc90fd6-de92-45c6-87ed-fec11a9566a6"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    dict = response.json()
    ans = []
    for account in dict['accounts']:
        account_id = account['account_id']
        balance = account['balances']['current']
        usd = account['balances']['iso_currency_code']
        name = account['name']
        official_name = account['official_name']
        element = []
        element.append(name)
        element.append(official_name)
        element.append(balance)
        element.append(usd)
        element.append(account_id)
        ans.append(element)
    return ans


@csrf_exempt
@require_http_methods(["GET", "POST"])
def webhook(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if body['webhook_code'] == 'INITIAL_UPDATE':
        print ("Initial Update Done.")
    elif body['webhook_code'] == 'HISTORICAL_UPDATE':
        print ("Historical Update Done.")
    print ("Transaction History is available now")
    # return redirect('bright:transactions')
    return HttpResponse("success")
