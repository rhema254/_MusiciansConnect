from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from core.views import *


urlpatterns = [

    path('admin_dashboard/' , admin_dashboard, name='admin_dashboard'),
    path('users/' , dash_users, name='users'),
    path('musicians/' , dash_musicians, name='musicians'),
    path('clients/' , dash_clients, name='clients'),
    path('applications/', dash_applications, name='applications'),
    path('gigs/' , dash_gigs, name='gigs'),
    path('payments/' , dash_payments, name='payments'),
]

