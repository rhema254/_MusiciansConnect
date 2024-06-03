from django.shortcuts import render

from .models import *
from django.db.models import Q , Count
from core.views import *
from django.db.models import Sum, Aggregate
from django.contrib.auth.models import User


# Create your views here.

def admin_dashboard(request):

    #Admin Dashboard Page 
    users = User.objects.all().select_related('musician', 'client')

    user_roles = []
    for user in users:
        role = None
        phone_number = None

        try:
            musician = user.musician
            role = 'Musician'
            phone_number = musician.phone_number
            
        except Musician.DoesNotExist:
            pass

        if not role:
            try:
                client = user.client
                role = 'Client'
                phone_number = client.phone
            except Client.DoesNotExist:
                pass
        
       

        user_roles.append({'user': user, 'role': role, 'phone_number': phone_number})
   

    total_musicians = Musician.objects.count()
    total_clients = Client.objects.count()
    total_count = total_clients + total_musicians
    musician_percentage = round((total_musicians / total_count) * 100)
    client_percentage = round((total_clients / total_count) * 100)
    total_gigs = Gig.objects.count()
    successfulhires_count = SuccessfulHire.objects.count()
    applications_count = Application.objects.count() 
    successfulapplications_count = Application.objects.filter(status = 'Accepted').count()
    pending_applications_count = Application.objects.filter(status = 'Pending').count()
    rejected_applications_count = Application.objects.filter(status = 'Rejected').count()

    data = {'labels': ['Musicians', 'Clients'],'values': [total_musicians, total_clients]}

    # Users Page
    

    

    # Gigs Page
    gigs = Gig.objects.all()

    # Musicians Page

    # Clients Page

    # Genres Page


    # Applications Page


    # Payments Page

    total_amount_paid = Payment.objects.aggregate(total_amount=Sum('amount'))['total_amount']
    average_amount_paid = Payment.objects.aggregate(average_amount=Avg('amount'))['average_amount']
    
# Retrieve the total amount paid




    context = {
        'users': users,
        'user_roles': user_roles,
        'total_gigs': total_gigs,
        'total_musicians': total_musicians,
        'total_clients': total_clients,
        'total_count': total_count,
        'musician_percentage': musician_percentage,
        'client_percentage': client_percentage,
        'successfulhires_count': successfulhires_count,
        'applications_count': applications_count,
        'successfulapplications_count': successfulapplications_count,
        'pending_applications_count': pending_applications_count,
        'rejected_applications_count': rejected_applications_count, 
        'gigs':gigs,
        'total_amount_paid':total_amount_paid,
        'average_amount_paid':average_amount_paid,
    }


    


    return render(request, 'dashboard/AdminDashboard.html', context)
    

def dash_users(request):

   #Admin Dashboard Page 
    users = User.objects.all().select_related('musician', 'client')

    user_roles = []
    for user in users:
        role = None
        phone_number = None

        try:
            musician = user.musician
            role = 'Musician'
            phone_number = musician.phone_number
            
        except Musician.DoesNotExist:
            pass

        if not role:
            try:
                client = user.client
                role = 'Client'
                phone_number = client.phone
            except Client.DoesNotExist:
                pass


        user_roles.append({'user': user, 'role': role, 'phone_number': phone_number})

    total_musicians = Musician.objects.count()
    total_clients = Client.objects.count()
    data = {'labels': ['Musicians', 'Clients'],'values': [total_musicians, total_clients]}

        
    total_count = total_clients + total_musicians
    musician_percentage = round((total_musicians / total_count) * 100)
    client_percentage = round((total_clients / total_count) * 100)
    total_gigs = Gig.objects.count()
    successfulhires_count = SuccessfulHire.objects.count()
    applications_count = Application.objects.count() 
    successfulapplications_count = Application.objects.filter(status = 'Accepted').count()
    pending_applications_count = Application.objects.filter(status = 'Pending').count()
    rejected_applications_count = Application.objects.filter(status = 'Rejected').count()


    # Users Page
    
    
    

    # Gigs Page
    gigs = Gig.objects.all()

    # Musicians Page
    musicians = Musician.objects.all()

    # Clients Page

    # Genres Page


    # Applications Page
    applications = Application.objects.all()

    # Payments Page


    context = {
        'users': users,
        'user_roles': user_roles,
        'total_gigs': total_gigs,
        'total_musicians': total_musicians,
        'total_clients': total_clients,
        'total_count': total_count,
        'musician_percentage': musician_percentage,
        'client_percentage': client_percentage,
        'successfulhires_count': successfulhires_count,
        'applications_count': applications_count,
        'successfulapplications_count': successfulapplications_count,
        'pending_applications_count': pending_applications_count,
        'rejected_applications_count': rejected_applications_count, 
        'gigs':gigs,
    }



    return render(request, 'dashboard/Users.html', context)

def dash_musicians(request):

    return render(request, 'dashboard/Musicians.html')


def dash_clients(request):

    return render(request, 'dashboard/Clients.html')

def dash_applications(request):

    return render(request, 'dashboard/Applications.html')

def dash_gigs(request):

    return render(request, 'dashboard/Gigs.html')

def dash_payments(request):

    return render(request, 'dashboard/Payments.html')