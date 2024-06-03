from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Musician)
# admin.site.register(Gig)
#admin.site.register(Client)
admin.site.register(Genre)
#admin.site.register(SuccessfulHire)
# admin.site.register(Application)
# admin.site.register(Review) 
# admin.site.register(Payment)

@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'location', 'skill_level', 'charge_rate', 'charge_rate_type', 'dob')
    readonly_fields = ('dob',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('date_applied', 'client', 'musician', 'gig', 'status')
    readonly_fields = ('date_applied', 'client', 'musician', 'gig')

@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'date_created', 'event_date', 'status')
    readonly_fields = ('date_created',) 


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location', 'client_type', 'get_genres', 'dob')  # Assuming an 'available' field exists
    readonly_fields = ('dob',)

    def get_genres(self, obj):
        """
        This function retrieves a comma-separated string of genres associated with the Client object.
        """
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Genres'  # Set a descriptive name for the displayed genre list

@admin.register(SuccessfulHire)
class SuccessfulHireAdmin(admin.ModelAdmin):
  list_display = ('client', 'musician', 'gig', 'completion_status', 'date_created')
  readonly_fields = ('client', 'musician', 'gig', 'date_created')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
  list_display = ('reviewer', 'reviewee', 'rating', 'comment', 'date_posted')
  readonly_fields = ('reviewer', 'reviewee', 'rating', 'comment', 'date_posted')

  
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('client_username', 'amount', 'gig_title', 'musician_username')
    readonly_fields = ('client', 'amount', 'successfulhire')

    def client_username(self, obj):
        return obj.client.user.username
    client_username.short_description = 'Client'

    def gig_title(self, obj):
        return obj.successfulhire.gig.title
    gig_title.short_description = 'Gig'

    def musician_username(self, obj):
        return obj.successfulhire.musician.user.username
    musician_username.short_description = 'Musician'