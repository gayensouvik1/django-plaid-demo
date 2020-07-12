from django.urls import path

from . import views

app_name = 'bright'
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('home/', views.homePage, name='home'),
    path('create/item/', views.createItem, name='createItem'),
    path('accounts/', views.accountPage, name='accounts'),
    path('transactions/', views.transactionsPage, name='transactions'),
    path('webhook/', views.webhook, name='webhook'),

]