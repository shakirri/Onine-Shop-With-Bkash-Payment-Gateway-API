from django.urls import path

from . import views
from user import views as views2

urlpatterns = [
    path('in', views.index, name="index"),
    path('index', views.index, name="index"),
    path('cartView',views.cartView, name="cartView"),
    path('create',views.create,name="create"),
    path('pay',views.pay,name="pay"),
    path('demo',views.demo,name="demo"),
    path('refund',views.refund,name="refund"),
    path('userlist',views.userlist,name="userlist"),
    path('agreementCheck',views.agreementCheck,name="agreementCheck"),
    path('agreeexe',views.agreeexe,name="agreeexe"),
    path('createAgreement',views.createAgreement,name="createAgreement"),
    path('createUrl',views.createUrl,name="createUrl"),
    path('cancelAgree',views.cancelAgree,name="cancelAgree"),
    path('paymentStatus',views.paymentStatus,name="paymentStatus"),
    path('status',views.status,name="status"),
    path('searchTransaction',views.searchTransaction,name="searchTransaction"),
]
