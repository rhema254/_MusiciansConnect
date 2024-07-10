from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.db.models import Q , Count
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .functions import client_required, musician_required 
from .forms import *
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django_daraja.mpesa.core import MpesaClient
import requests
from django.conf import settings
import json
from decimal import Decimal
from django.db.models import Avg
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect

# from .filters import ApplicationFilter


import re
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def base(request):
    return render(request, "base.html")


def baseprofiles(request):


    return render(request, "baseprofiles.html")

def LandingPage(request):
    return render(request, "accounts/LandingPage.html")


def about_us(request):
    return render(request, "accounts/AboutUs.html")


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = '/home'
    

@login_required
def account_setup(request):
    genres = Genre.objects.all()

    if request.method == "POST":
        selected_genres = request.POST.getlist("selected_genres")
        user = request.user  # Access user only if authenticated

        selected_genres = request.POST.getlist("selected_genres")
        for genre_id in selected_genres:
            genre = Genre.objects.get(id=genre_id)
        if user.is_client:
            user.genre.add(genre)
        elif user.is_musician:
            user.genre.add(genre)
        
        return redirect("home")

    context = {"genres": genres}

    return render(request, "accounts/AccountSetup2.html", context)

def accountdetails(request):
    if request.method == "POST":
        deletereq = request.POST.get('account_delete')
        if deletereq == "True":
            user = request.user
            user.delete()
            return redirect("landingpage")

    return render(request, "accounts/AccountDetails.html")

def restricted_page(request):
    return render(request, "accounts/RestrictedPage.html")

@login_required(login_url="Login")
def edit_profile(request):

    musician = request.user.musician    
    if request.method == 'POST':
       
            musician.title = request.POST.get('title')
            musician.bio = request.POST.get('bio')
            musician.phone_number = request.POST.get('phone_number')
            musician.location = request.POST.get('location')
            musician.instagram = request.POST.get('instagram')
            musician.facebook = request.POST.get('facebook')
            musician.youtube = request.POST.get('youtube')
            musician.skill_level = request.POST.get('skill_level')
            musician.charge_rate = request.POST.get('charge_rate')
            musician.charge_rate_type = request.POST.get('charge_rate_type')
            musician.profession_category = request.POST.get('profession_category')
            musician.experience = request.POST.get('experience')
        

            
            if request.FILES.get('sample1'):
                musician.sample1 = request.FILES.get('sample1') 

            if request.FILES.get('sample2'):
                musician.sample2 = request.FILES.get('sample2')

            # Handle file uploads
            if request.FILES.get('profile_picture'):
                musician.profile_picture = request.FILES.get('profile_picture')

            genre_names = request.POST.getlist('genres')
            print(genre_names)
            genres = Genre.objects.filter(name__in=genre_names)
            # Set the client's genres
            musician.genres.set(genres)
            musician.save()
            messages.success(request, 'Profile saved successfully! Now proceed to the gigspage and apply for a new gig!')
            return redirect('home')        
    
           
    return render(request, "accounts/EditProfiles.html")


@client_required
def edit_client_profile(request):

    client = request.user.client

    if request.method == 'POST':
        # Update client profile fields with data from the form
        client.location = request.POST.get('location')
        client.description = request.POST.get('description')
        client.phone = request.POST.get('phone')
        genre_names = request.POST.getlist('genres')
        # Convert genre names to Genre objects
        genres = Genre.objects.filter(name__in=genre_names)
        # Set the client's genres
        client.genres.set(genres)
        if request.FILES.get('profile_picture'):
            client.profile_picture = request.FILES.get('profile_picture')
        # Save the updated client profile
        client.save()
        return redirect('home')    

    return render(request, "accounts/EditClientProfile.html")

@login_required(login_url="Login")
def view_musician_profile(request, musician_id):
    musician = get_object_or_404(Musician, pk=musician_id)
    print(musician_id)
    user = musician.user
    print(user)

    successfulhires = SuccessfulHire.objects.filter(musician=musician_id)
    successfulhires_count = successfulhires.count()
    
    # Get all reviews for the musician
    ratings = Review.objects.filter(reviewee=user)

    # Calculate the average rating
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']


    genres = Genre.objects.filter(musicians=musician_id)
    print(genres)
    return render(request, "accounts/MusicianProfile.html",  {'musician': musician, 'user':user, 'genres':genres, 'successfulhires': successfulhires, 'successfulhires_count':successfulhires_count, 'avg_rating':avg_rating })

def check_username(request):
    username = request.GET.get("username")
    if User.objects.filter(username=username).exists():
        return JsonResponse({"available": False})
    else:
        return JsonResponse({"available": True})


# Ile ya Kwanza... Original
def Register(request):
    if request.user.is_authenticated:  # This is a Guard Clause.
        return redirect("home") 


    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("uname")
        email = request.POST.get("email")
        password = request.POST.get("pass")
    
        cleaned_email = email.strip()
        cleaned_fname = fname.strip()
        cleaned_lname = lname.strip()
        cleaned_password = password.strip()

        print(cleaned_lname)
        print(cleaned_password)

        try:
            # Create the user
            user = User.objects.create_user(username=username, email=cleaned_email, password=cleaned_password, first_name=cleaned_fname, last_name=cleaned_lname)
            
            # Create associated Musician instance (if applicable)
            musician = Musician.objects.create(user=user)
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            # Log in the user
            auth_login(request, user)
            
            # Display success message
            messages.success(request, f"Welcome {user.username}")
            
            # Redirect to edit profile page
            return redirect("edit_profile")
        
        except Exception as e:
                # Handle any errors that occur during user creation
                messages.error(request, f"An error occurred: {str(e)}")
                # Redirect back to registration page or display appropriate error page
                return redirect("register")
        
    return render(request, "accounts/RegisterMusicians.html")

def Login(request):

    if request.user.is_authenticated:  # This is a Guard Clause.
        return redirect("home")
    

    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pass")
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)

        print(User.pk)
        if user is not None:

            auth_login(request, user)
            messages.success(request, f"Welcome Back {user.username}")
            return redirect("home")

        else:
            messages.error(request, "Error, wrong email or password")

    return render(request, "accounts/LoginMusicians.html")

def registerclients(request):

    if request.user.is_authenticated:  # This is a Guard Clause.
        return redirect("home")

    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("uname")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        

        cleaned_email = email.strip()
        cleaned_fname = fname.strip()
        cleaned_lname = lname.strip()
        cleaned_password = password.strip()

    
        try:
            # Create the user
            user = User.objects.create_user(username=username, email=cleaned_email, password=cleaned_password, first_name=cleaned_fname, last_name=cleaned_lname)
            
            # Create associated Musician instance (if applicable)
            client = Client.objects.create(user=user)
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            # Log in the user
            auth_login(request, user)
            
            # Display success message
            messages.success(request, f"Welcome {user.username}")
            
            # Redirect to edit profile page
            return redirect("edit_client_profile")
        
        except Exception as e:
                # Handle any errors that occur during user creation
                messages.error(request, f"An error occurred: {str(e)}")
                # Redirect back to registration page or display appropriate error page
                return redirect("registerclients")
        

    return render(request, "accounts/RegisterClients.html")


def loginclients(request):
    if request.user.is_authenticated:  # This is a Guard Clause.
        return redirect("home")
    

    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pass")
       
        user = authenticate(request, username=username, password=password)
      
        if user is not None:

            auth_login(request, user)
            messages.success(request, f"Welcome Back {user.username}")
            return redirect("home")

        else:
            messages.error(request, f"Error, wrong email or password")

    return render(request, "accounts/LoginClients.html")

@login_required
def save_selected_genres(request):
    if request.user.is_authenticated:
            user = request.user
            
    if not request.user.is_authenticated:
        return redirect("Login")

    if request.method == "POST":
                
        user = request.user.get("id")


        selected_genres = request.POST.getlist("selected_genres[]")

        # Assuming the selected genres are sent as a list

        # Check if the user is a musician or a client
        if hasattr(user, "musician"):
            musician = user.musician
            musician.genres.clear()  # Clear existing genres

            for genre_name in selected_genres:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                musician.genres.add(genre)
            return JsonResponse({"message": "Selected genres saved successfully for musician."})

        elif hasattr(user, "client"):
            client = user.client
            client.genres.clear()  # Clear existing genres
            for genre_name in selected_genres:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                client.genres.add(genre_name)
            return JsonResponse(
                {"message": "Selected genres saved successfully for client."}
            )

        else:
            return JsonResponse(
                {"error": "User is neither a musician nor a client."}, status=400
            )

    return JsonResponse({"error": "Invalid request method."}, status=405)


def user_logout(request):
    logout(request)
    return redirect("Login")


def home(request):
    available_jobs = Gig.objects.filter(status = 'Open')
    return render(request, "accounts/Homepage.html", { "available_jobs": available_jobs})


def musicianspage(request):
    musicians = Musician.objects.all().select_related('user')
    musicians_with_rating = musicians.annotate(avg_rating=Avg('user__received_reviews__rating'))
    
    return render(request, "accounts/Musicianspage.html", {"musicians": musicians_with_rating})

@csrf_protect
@musician_required
def dashboard(request):

        
        applications = Application.objects.filter(musician=request.user.musician).order_by('-date_applied')
        

        if request.method == 'POST' and request.POST.get('withdraw'):

            application_id = request.POST.get('applicationId')
            withdraw = request.POST.get('withdraw_application')
            
            if withdraw == 'True':
                application = Application.objects.get(id=application_id)
                application.delete()

        if applications.count() == 0:
            messages.info(request, "You have no application Yet.")

         
       # This list is in the Gig requests. 
        accepted_applications = applications.filter(status='Accepted').order_by('date_applied')
        musician = request.user.musician
        
        applications_without_successfulhire = []

        for application in accepted_applications:
            # Check if the application has a SuccessfulHire instance
            has_successfulhire = SuccessfulHire.objects.filter(
                Q(musician=application.musician) | Q(client=application.client),
                gig=application.gig
            ).exists()

            if not has_successfulhire:
                applications_without_successfulhire.append(application)



        # Access the musician on individual instances within the accepted_applications queryset
        
        #This is fed by "Accept Offer", to change the application status from accepted to Done. 
        #Ongoing  GIgs --- Move it to the Cgigs
        if request.method == 'POST' and request.POST.get('accept_gig'):
            accept_gig = request.POST.get('accept_gig')
            application_id = request.POST.get('applicationId')  
            application = Application.objects.get(id=application_id)
            musician = request.user.musician
            client = application.client
            print(musician)
            print(client)

            try:
                existing_hire = SuccessfulHire.objects.filter(application=application).exists()
                
                if not existing_hire:
                    successful_hire = SuccessfulHire.objects.create(application = application, musician = musician, client = client, gig=application.gig, completion_status = 'Ongoing')
                else:
                    # Handle the case where a SuccessfulHire instance already exists
                    messages.info(request, "You have already accepted this Offer. Reload the page to view changes.")
                    pass
            except IntegrityError:
                messages.success(request,"You have already accepted this offer. Reload your page to view changes.")
                pass


        ## After accepting the offer, the list of ongoing gigs is rendered through the queryset below.:
        ongoing_hires = SuccessfulHire.objects.filter(musician = request.user.musician, completion_status = 'Ongoing')
        
        ##  This code handles the "Mark as complete, request pay" btn,and  
        if request.method == 'POST' and request.POST.get('mark_complete'):
           
            successful_hireId = request.POST.get('successful_hireId')
            
           
                
        ### After a client has paid for the gig, the whole transaction is complete and the gig is done. 
        completed_gigs = SuccessfulHire.objects.filter(musician=musician, completion_status= 'Completed')
        completed_gigs_count = completed_gigs.count()

        return render(request, "accounts/Dashboard.html", {"applications": applications, 'accepted_applications': applications_without_successfulhire, 'ongoing_hires': ongoing_hires , 'completed_gigs_count':completed_gigs_count, 'completed_gigs':completed_gigs} )


@client_required
def application_review(request):
    applications = Application.objects.filter(client=request.user.client).order_by('-date_applied')
    gig_ids = [application.gig.id for application in applications]
    print(gig_ids)
    no_of_applications = Application.objects.filter().count()
    if applications.count() == 0:
        messages.info(request, "No applications found.")


    return render(request, "accounts/ApplicationReview.html", {"applications": applications, 'no_of_applications': no_of_applications})
# #

@client_required
def trial_application_review(request):
    applications = Application.objects.filter(client=request.user.client).order_by('-date_applied')
    
    if request.user.is_authenticated:
        client = request.user.client
        genres_list =  list(client.genres.values_list('name', flat=True))
        print(genres_list)

    if request.user.is_authenticated:
        client = request.user.client
        total_gigs = client.gigs.count()
        gigs_list = Gig.objects.filter(client=client)


    if applications.count() == 0:
        messages.info(request, "No applications found.")


    return render(request, "accounts/TrialApplicationReview.html", {"applications": applications, 'genres_list':genres_list, 'total_gigs':total_gigs, 'gigs_list':gigs_list })

@musician_required
def gigs(request):
    
    sum_gigs = Gig.objects.all().count()
    today = datetime.now().date()
    print(today)
    gigs = Gig.objects.filter(status='Open')
# Filter out the gigs with event dates less than today
    gigs = gigs.filter(event_date__gte=timezone.now().date())

    # Get the accepted applications for the client's gigs
    accepted_applications = Application.objects.filter(
        gig__in=gigs,
        status='Accepted'
    )

    # Get the gig IDs that have accepted applications
    accepted_gig_ids = accepted_applications.values_list('gig_id', flat=True)

    # Filter the gigs to exclude the ones that have accepted applications
    gigs = gigs.exclude(id__in=accepted_gig_ids)


    gig_count = gigs.count()
    
    closed_gigs_count = sum_gigs - gig_count

    if request.method == "POST":
        gig_id = request.POST.get("gig_id")
        gig = Gig.objects.get(id=gig_id)
        musician = request.user.musician
        
        print(gig)
        
        try:
            application = Application.objects.create(
                gig=gig,
                musician=musician,
                client=gig.client
            )
            messages.success(request, "Application submitted successfully.")
        except IntegrityError:
            messages.error(request, "You have already applied to this gig.")
            return redirect('gigspage')
            
        return redirect("dashboard")  # Redirect after successful application

    return render(request, "accounts/M-Gigs.html", {"gigs": gigs , "gig_count": gig_count, 'sum_gigs': sum_gigs, 'closed_gigs_count':closed_gigs_count})



@client_required
def cGigs(request):
        
        ####### Creating A Gig code: Receive inputs from FrontEnd, Process and Save.  
        
        if request.method == "POST":
            
            try: 
                client = request.user.client
            
                # Retrieve data from the request
                title = request.POST.get("title")
                description = request.POST.get("description")
                location = request.POST.get("location")
                budget = request.POST.get("budget")
                Profession_category = request.POST.get("Profession_category")
                dry_run = request.POST.get("dry-run-requirement")
                event_policy = request.POST.get("event_policy")
                event_date = request.POST.get("event_date")
                event_type = request.POST.get("event_type")
                
                genre_names = request.POST.getlist('genres')
                # Convert genre names to Genre objects
                genres = Genre.objects.filter(name__in=genre_names)
                # et the client's genres
                
                
                # Create a new Gig object
                new_gig = Gig.objects.create(client=client,
                                            title=title,
                                            description=description,
                                            location=location,
                                            status="Open",
                                            budget=budget,
                                            Profession_category=Profession_category,
                                            dry_run=dry_run,
                                            event_policy=event_policy,
                                            event_date=event_date,
                                            event_type=event_type,
                                            )
                print(new_gig)

                new_gig.genres.set(genres),
                new_gig.save()  # Save the new Gig object
                print(new_gig)
                return redirect("gigspage")  # Redirect to a success page
            except Application.DoesNotExist:
                 messages.error(request, 'Application not found')
            except IntegrityError as e:
                messages.error(request, 'Integrity error occurred: {}'.format(e))

                

        ## NEW SECTION ####
        # This code retrieves a queryset of objects(gigs) that are associated with request.user. Presents all gigs of a client.
                # Get the gigs for the current client
        gigs = Gig.objects.filter(client=request.user.client)
        
        gig_id = [gig.id for gig in gigs]
        
        applications = Application.objects.filter(client=request.user.client, status = 'Submitted', gig__in=gig_id)
    
        applications_count = applications.count()


        
            # musicians = []
            # for application in applications:
            #     musician = application.musician
            #     musician_name = musician.user.username
            #     musician_email = musician.user.email
            #     musicians.append({
            #         'name': musician_name,
            #         'email': musician_email,
            #     })
            
        if gigs.count() == 0:
            messages.info(request, "No Gigs found.")
            
            # Accepted GIgs


        
        ########## Code for shortlisting or Immediate Rejection. Receives a decision from the 
        ## frontend, processes it and updates the status field.
            
        ###When you click one gig on My pending Gigs, whether to reject application or Accept it
        if request.method == 'POST' and request.POST.get('accept_applicant'):
            accept_applicant = request.POST.get('accept_applicant')
            application_id = request.POST.get('applicationId')
            print(application_id)
            try:    
                application = Application.objects.get(id=application_id)

                if accept_applicant == 'True':
                    application.status = 'Accepted'     
                    application.save()
                    
                elif accept_applicant == 'False':
                    application.status = 'Rejected'
                    application.save()
                    
                else:
                    messages.info('Invalid decision')    

            except Application.DoesNotExist:
                print('Application not found')
            
            return redirect('clientgigs')

        
        
        accepted_applications = Application.objects.filter(client=request.user.client, status='Accepted')
        Accepted_applications_no = accepted_applications.count()


        if request.method == 'POST' and request.POST.get('cancel_gig'):
            cancel_gig = request.POST.get('cancel_gig')
            application_id = request.POST.get('applicationId')
            application = Application.objects.get(id=application_id)

            if cancel_gig == 'True':
                application.status = 'Rejected'   
                messages.success(request, f'You have successfully rejected application by {application.musician.user.username} for job: {application.gig.title}d')  
                application.save()
        
        print(Accepted_applications_no)

        ongoing_hires = SuccessfulHire.objects.filter(client=request.user.client, completion_status='Ongoing')
        
        if request.method == 'POST' and request.POST.get('mark_complete'):
            successfulhire_Id = request.POST.get('successful_hireId')
            mark_complete = request.POST.get('mark_complete')
            print(successfulhire_Id)
            successfulhire = SuccessfulHire.objects.get(id=successfulhire_Id)

            if mark_complete == 'True':
                return redirect('servicespage', successfulhire_Id=successfulhire_Id)
                
        completed_gigs = SuccessfulHire.objects.filter(client=request.user.client, completion_status='Completed') 
        completed_gigs_count = completed_gigs.count()  
        #  return render(request, "accounts/C-Gigs.html", {'gigs': gigs, 'applications':applications, 'shortlisted_applicants':shortlisted_applicants, 'applications_count': applications_count})


        return render(request, "accounts/C-Gigs.html", {'gigs': gigs, 'applications':applications, 'applications_count': applications_count, 'accepted_applications': accepted_applications, 'Accepted_applications_no': Accepted_applications_no, 'ongoing_hires':ongoing_hires, 'completed_gigs':completed_gigs, 'completed_gigs_count':completed_gigs_count })


@login_required
def finalise_agreement(request, shortlisted_applicant_id):
    
    application = Application.objects.get(id=shortlisted_applicant_id)
    hire = request.POST.get('hire')
    
    
    if request.method == 'POST' and 'hire' in request.POST:
        
            signature = request.POST.get('signature')
            # application_id = request.POST.get('application_id')
            application = Application.objects.get(id=application.id)
            gig = Gig.objects.get(id=application.gig.id)
            musician= Musician.objects.get(id=application.musician.id)   
            client = Client.objects.get(id=request.user.client.id)
            clientId = client.id
            gig_id = application.gig.id

            if hire == 'True' and signature:
                if signature == f"{request.user.first_name} {request.user.last_name}":
                    try:

                        application.status = 'Accepted'
                        application.save()
                        successfulhire = SuccessfulHire.objects.create(client_id=clientId, musician=musician, gig=gig, application=application, completion_status = 'Ongoing')
                        
                    
                    except IntegrityError:
                        messages.error(request, "This gig is already ongoing!")

                    return redirect('clientgigs')    
                else:
                    messages.error(request, " Error ")   
            else:
                messages.info(request, "Enter the Full Names that you signed up with")  

    clientId = Client.objects.get(id=request.user.client.id)
    ongoing_hires = SuccessfulHire.objects.all()
    hires_count = ongoing_hires.count()  
    print(hires_count)
    print(ongoing_hires)

    return render(request, 'accounts/FinaliseAgreement.html', {'messages': messages, 'application':application, 'ongoing_hires': ongoing_hires, 'hires_count': hires_count} )



# ---------------AUXILIARY FUNCTIONS__-----------


# # Search Bar functionality on Gigs Page
# def search_gigs(request):

#     today = datetime.today()
    
#     if "q" in request.GET:
#         q = request.GET["q"]
        
#         gigs = Gig.objects.filter(title__icontains=q,  expiry_date__gte=today)
#         multiple_q = Q(
#             Q(title__icontains=q)
#             | Q(location__icontains=q)
#             | Q(status__icontains=q)
#             | Q(budget__icontains=q)
#             | Q(payment_policy__icontains=q)
#         )
       
#         # gigs = Gig.objects.filter(multiple_q,  today = datetime.today())
#         # gigs_list = []
#         # for gig in gigs:
#         #     for genre in gig.genres.all():
#         #         if genre.name.includes(q) and gig not in gigs_list:
#         #             gigs_list.append(gig)
#         return render(request, "accounts/M-Gigs.html", {"gigs": gigs})
#     else:
#         gigs = Gig.objects.all()

#         context = {"gigs": gigs}

#     return render(request, "accounts/M-Gigs.html", context)


# Search Bar functionality on Musicians Page
def search_musicians(request):
    if "mQ" in request.GET:
        q = request.GET["mQ"]
        # gigs = Gig.objects.filter(title__icontains=q)
        multiple_q = Q(
            Q(username__icontains=q)
            | Q(genre__icontains=q)
            | Q(fname__icontains=q)
            | Q(lname__icontains=q)
            | Q(skill_level__icontains=q)
            | Q(charge_rate__icontains=q)
            | Q(location__icontains=q)
        )
        musicians = Musician.objects.filter(multiple_q)
    else:
        gigs = Gig.objects.all()

    context = {"musicians": musicians}

    return render(request, "accounts/Musicianspage.html", context)


# Not COMPLETE>>> What's left is handling the results and then saving the payment details to the database.
@client_required
def services(request, successfulhire_Id):
    
    callback = settings.CALLBACK_URL  # Get the ngrok address from Django settings
    callback_url = callback
       
 
    if request.method == 'POST':
        successfulhire = SuccessfulHire.objects.get(id=successfulhire_Id)
        price = successfulhire.gig.budget
        amount = int(price)
        phone_number = request.POST.get('phone')
        cl = MpesaClient()
        account_reference = successfulhire.gig.id
        transaction_desc = 'Description'
        
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

        if response.status_code == 200:
            amount = amount
            client = successfulhire.client

            existing_payment = Payment.objects.filter(successfulhire=successfulhire).first()
            if existing_payment:
                # If a payment already exists, you can either update it or handle it accordingly
                messages.info(request, 'Payment already exists for this SuccessfulHire.')
            
            else:
                    
                payment = Payment.objects.create(amount=amount, client=client, successfulhire=successfulhire)
                payment.save()
                successfulhire.completion_status = 'Completed'
                successfulhire.save()
                return redirect('successmessage', successfulhire_Id)
        else:
            print('User is offline')
            error_message = 'User is offline'
            messages.error(request, 'accounts/ServicesPage.html', {'error_message': error_message})

    return render(request, 'accounts/ServicesPage.html')
@client_required
def successmessage(request, successfulhire_Id):

    successfulhire = SuccessfulHire.objects.get(id=successfulhire_Id)
    payment = Payment.objects.get(successfulhire=successfulhire)
    
    context = {
        'successfulhire': successfulhire,
        'payment':payment,
    }

    if request.method == 'POST' and request.POST.get('successfulhire_Id'):
         successfulhire_Id = request.POST.get('successfulhire_Id')
         return redirect('reviews_ratings', successfulhire_Id)
        

    return render(request, "accounts/SuccessMessage.html", context)




@login_required
def review_rating(request, successfulhire_id):
    
    successfulhire = get_object_or_404(SuccessfulHire, id=successfulhire_id)
    
    
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        rating = Decimal(rating_value)
        comment = request.POST.get('opinion')
       
        if request.user.client:
            # Client is rating the musician
            client = request.user.client
            musician = successfulhire.musician
            reviewer = client.user
            reviewee = musician.user 

            new_review = Review(rating=rating, comment=comment, reviewer=reviewer, reviewee=reviewee)
            new_review.save()

            # Perform any additional actions if needed

        elif request.user.musician:
            # Musician is rating the client
            musician = request.user.musician
            client = successfulhire.client
            reviewer = musician.user
            reviewee = client.user 

            new_review = Review(rating=rating, comment=comment, reviewer=reviewer, reviewee=reviewee)
            new_review.save()

            # Perform any additional actions if needed

        # Redirect or render a success page
        return redirect('home')
    
    
    return render(request, "accounts/ReviewPage.html", {'successfulhire': successfulhire})





# Not COMPLETE>>> What's left is handling the results and then saving the payment details to the database.
# def process_payment(successfulhire, phone_number):
   
    

# def query_transaction_status(mpesa_client, checkout_request_id):
#     # Query the transaction status
#     response = mpesa_client.query_stk_push(checkout_request_id)

#     if response.status_code == 200:
#         # Get the transaction status
#         transaction_status = response.json()['ResponseDescription']
#         return transaction_status
#     else:
#         # Error occurred while querying transaction status
#         return response.text




def call_back_url(request):
           
    if request.method == 'POST':
        results = MpesaClient().parse_stk_result(request.body)
        result_code = results.get('ResultCode')
        transaction_date = results.get('TransactionDate')
        amount = results.get('Amount')
        receipt_number = results.get('MpesaReceiptNumber')

        if result_code == '0':
            print('Success')
    else:
        return HttpResponse("Invalid request method", status=405)

    
# def initiate_payment(request):
#     # M-Pesa API credentials
#     consumer_key = ''
#     consumer_secret = 'your_consumer_secret'
    
#     # Endpoint URLs
#     access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
#     lipa_na_mpesa_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
#     # Obtain OAuth access token
#     response = requests.get(access_token_url, auth=(consumer_key, consumer_secret))
#     access_token = response.json().get('access_token')
    
#     # Payload for Lipa Na M-Pesa Online Payment
#     payload = {
#         'BusinessShortCode': 'your_business_short_code',
#         'Password': 'your_encoded_password',
#         'Timestamp': 'your_timestamp',
#         'TransactionType': 'CustomerPayBillOnline',
#         'Amount': 'your_amount',
#         'PartyA': 'your_phone_number',
#         'PartyB': 'your_business_short_code',
#         'PhoneNumber': 'your_phone_number',
#         'CallBackURL': 'your_callback_url',
#         'AccountReference': 'your_account_reference',
#         'TransactionDesc': 'your_transaction_description'
#     }
    
#     # Headers for the request
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
    
#     # Make the request to initiate payment
#     response = requests.post(lipa_na_mpesa_url, json=payload, headers=headers)
    
#     # Return the response
#     return JsonResponse(response.json())


def job_count(request):
    jobs = Gig.objects.all()
    jobs_count = Gig.objects.count()
   
    return render(request, "accounts/M-Gigs.html",  {"job_count": job_count})






# PROBABLY MOVE THIS TO musiciansconnect app
def carousel_view(request):
    return render(request, 'CarouselSlider.html')



from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def generate_pdf_report(request):
    # Fetch data from your model or queryset
    data = Application.objects.all()

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Create the PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Prepare data for table
    table_data = [['application', 'gig', 'Field 3']]  # Headers
    for item in data:
        table_data.append([item.field1, item.field2, item.field3])

    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Add table to elements
    elements.append(table)

    # Build PDF
    pdf.build(elements)
    return response

# UNused view


@login_required(login_url="login")
def view_profile(request, musician_id):  #Current view: View_musician_profile 
    musician = Musician.objects.get(id=musician_id)
    
    if request.user.is_authenticated:
        user = request.user

    # I don't know what this does, I'll be back
    musicians = Musician.objects.all()
    genres_list = Genre.objects.filter(musicians=musician)

    return render(request, "accounts/MyProfile.html", {'musician': musician, 'musicians':musicians, 'genres_list    ':genres_list})





#  VIews that are no longer / redundant






# @musician_required
# def trial_dashboard(request):
#     applications = Application.objects.filter(musician=request.user.musician).order_by('-date_applied')
    

#     if applications.count() == 0:
#         messages.info(request, "No applications found.")
    
#     if request.user.is_authenticated:
#         musician = request.user.musician
#         genres_list =  list(musician.genres.values_list('name', flat=True))
#         print(genres_list)

#     # if request.user.is_authenticated:
#     #     client = request.user.client
#     #     total_gigs = client.gigs.count()
#     #     gigs_list = Gig.objects.filter(client=client)


#     return render(request, "accounts/TrialDashboard.html", {"applications": applications, 'genres_list':genres_list}