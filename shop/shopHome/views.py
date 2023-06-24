from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.shortcuts import redirect
from .models import Users
from django.contrib.auth.decorators import login_required

# Create your views here.

username1="A"
agreementA="null"
username2="B"
AgreementB="null"
app_key="HIDDEN"
app_secret="HIDDEN"
bKashUsername="HIDDEN"
bKashPassword="HIDDEN"
baseURL="http://127.0.0.1:8000/"

@login_required(login_url='login')
def userlist(request):
  users=Users.objects.all()
  return render(request, "list.html", {'us':users})

@login_required(login_url='login')
def index(request):
    return render(request, "Home.html")

def cartView(request):
    return render(request, "cart.html")

def demo(request):
    exe = {"statusCode":"0000","statusMessage":"Successful","paymentID":"TR0011w3gHpuO1686476560265","payerReference":" ","customerMsisdn":"01619777283","trxID":"AFB10B8TRV","amount":"3","transactionStatus":"Completed","paymentExecuteTime":"2023-06-11T15:44:40:402 GMT+0600","currency":"BDT","intent":"sale","merchantInvoiceNumber":"Inv0124"}
    test = Users(name="Beatles Blog", agreementID="All the latest Beatles news.")
    test.save()
    return HttpResponse("done")

def refund(request):
    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/payment/refund"
    
    payload = {
      "paymentID": payinfo['paymentID'],
      "trxID": payinfo['trxID'],
      "amount": payinfo['amount'],
      "sku": "test",
      "reason": "hudai"
}

    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key,
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)

    return HttpResponse(response.text)

def execute(paymentID):
    
    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/execute"

    payload = {"paymentID": paymentID}
    
    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key,
        "content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)

    return(response.json())

def query(request, payment, ur):
    if ur=='a':
      user=request.user
      userID=Users.objects.get(name=user.username)
      agreementA=userID.agreementID
      url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/agreement/status"
      payload= {
        'agreementID': agreementA
      }
    else:
      url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status"
      payload= {
        'paymentID': payment
      }

    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key,
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

def pay(request):
    paymentID = request.GET['paymentID']
    exe=execute(paymentID)
    if exe==None:
      x=query(request, paymentID, 'p')
      return HttpResponse(x.text)
    global payinfo
    payinfo=exe
    statusCode=exe['statusCode']
    if (statusCode=='0000'):
      info={'transaction':'Successful',
          'trnx': payinfo['trxID'],
          'amount':payinfo['amount'],
          'status': statusCode
    }
    else:
      info={'transaction':'Failed',
          'status':statusCode,
          'trstat':exe['statusMessage']

      }
    return render(request, "paymentSuccess.html",info)
    #return HttpResponse(a)
    #return render(request, "paymentSuccess.html")

def agreeexe(request):
    paymentID = request.GET['paymentID']
    exe=execute(paymentID)
    if exe==None:
      x=query(request, paymentID, 'a')
      return HttpResponse(x)
    user=request.user
    userID=Users.objects.get(name=user.username)
    userID.agreementID=exe['agreementID']
    userID.phone=exe['customerMsisdn']
    userID.save()
    return render(request, "agreement.html")


def createAgreement(request):
    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create"

    payload = {
        "mode": "0000",
        "callbackURL": baseURL+"/agreeexe",
        "amount": "2",
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": "Inv0124",
        "payerReference": " "
    }
    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key,
        "content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    bkashUrls=response.json()["bkashURL"]
    return redirect(bkashUrls)


def agreementCheck(request):
    if request.user.is_authenticated:
        user=request.user
    else:
        return redirect('login')
    user=request.user
    userID=Users.objects.get(name=user.username)
    agreementA=userID.agreementID
    grant()
    bkashUrls=""
    if agreementA==None:
      return render(request, "decideAgreeCreate.html")
      decideToCreate()
      response=createAgreement()
    else:
      return render(request, "decideAgreeUse.html",{'phone':userID.phone})
      response=create(request)
    bkashUrls=response["bkashURL"]
    return redirect(bkashUrls)

def createUrl(request):
    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create"
    
    payload = {
        "mode": "0011",
        "callbackURL": baseURL+"/pay",
        "amount": "2",
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": "Inv0124",
        "payerReference": " "
    }
    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key,
        "content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    bkashUrls=response.json()["bkashURL"]
    return redirect(bkashUrls)

def create(request):
    user=request.user
    userID=Users.objects.get(name=user.username)
    agreementA=userID.agreementID
    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create"
    
    payload = {
        'agreementID': agreementA,
        "mode": "0001",
        "callbackURL": baseURL+"/pay",
        "amount": "2",
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": "Inv0124",
        "payerReference": " "
    }
    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key,
        "content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    bkashUrls=response.json()["bkashURL"]
    return redirect(bkashUrls)


def grant():
    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant"

    payload = {
        "app_key": app_key,
        "app_secret": app_secret
    }
    headers = {
        "accept": "application/json",
        "username": bKashUsername,
        "password": bKashPassword,
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    global authorization
    authorization = response.json()['id_token']
    return response
    #return HttpResponse(bkashUrls)

def cancelAgree(request):
    user=request.user
    userID=Users.objects.get(name=user.username)
    agreementA=userID.agreementID

    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/agreement/cancel"
    
    payload = {"agreementID":agreementA }
    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    userID.agreementID=None
    userID.phone=None
    userID.save()
    return HttpResponse(response.text)

def status(request):
    return render(request,"payStatus.html")

def paymentStatus(request):
    grant()
    paymentID=request.GET['payment']

    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status"

    payload = {"paymentID": paymentID}
    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return HttpResponse(response.text)

def searchTransaction(request):
    grant()
    trx=request.GET['trx']

    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/general/searchTransaction"

    payload = {"trxID": trx}
    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return HttpResponse(response.text)