from datetime import timedelta, timezone
from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Client(models.Model):
    
    
    CLIENT_TYPE_CHOICES = [
        ('Business', 'Business'),
        ('Individual', 'Individual'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    client_type = models.CharField(max_length=20, blank=True, choices=CLIENT_TYPE_CHOICES)
    phone = models.CharField(max_length=20)
    genres = models.ManyToManyField('Genre', related_name='clients')#ondelete set null/ do nothing.
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

class Musician(models.Model):
    PROFESSION_CHOICES = [
    ('singer', 'Singer'),
    ('songwriter', 'Songwriter'),
    ('producer', 'Producer'),
    ('vocalist', 'Vocalist'),
    ('band', 'Band'),
    ('instrumentalist', 'Instrumentalist'),
    ('sound-engineer', 'Sound Engineer'),
    ('music-educator', 'Music Educator'),
    ('folk-traditional', 'Folk and Traditional'),
    ('dj', 'DJ'),
    ('cover-band', 'Cover Band'),
]

    MUSICIAN_SKILL_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Pro', 'Pro'),
        ('Maestro', 'Maestro'),
    ]
    
    CHARGE_RATE_CHOICES = [
        ('hour', 'Per Hour'),
        ('session', 'Per Session'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genres = models.ManyToManyField('Genre', related_name='musicians')
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=20, choices=MUSICIAN_SKILL_LEVEL_CHOICES)
    charge_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0)#implement null functionality
    charge_rate_type = models.CharField(max_length=10, choices=CHARGE_RATE_CHOICES)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.CharField(max_length=255, blank=True)
    available = models.BooleanField(default=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    experience = models.TextField(blank=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    sample1 = models.FileField(upload_to='sample_videos/', blank=True, null=True)
    sample2 = models.FileField(upload_to='sample_videos/', blank=True, null=True)
    profession_category = models.CharField(max_length=25, choices=PROFESSION_CHOICES, blank=True)

    def __str__(self):
        return self.user.username


class Gig(models.Model):

    dry_run_choices = [
    ('', 'Select one'),  
    ('Yes', 'Yes (Paid Separate)'),
    ('No', 'Yes (No payment)'),
    ('Full-after-job', 'NO'),
    ('Negotiable', 'To Be Determined'),
    ]

    EVENT_POLICY_CHOICES=[
    ('', 'Select one'),
    ('Instruments-provided', '100%: Instruments-provided'),
    ('Come with yours', '50%: Come with yours'),
    ('Negotiable', 'Negotiable'),
    
    ]

    PROFESSION_CHOICES = [
    ('', 'Select one'),
    ('Singer', 'Singer'),
    ('Songwriter', 'Songwriter'),
    ('Producer', 'Producer'),
    ('Vocalist', 'Vocalist'),
    ('Band', 'Band'),
    ('Instrumentalist', 'Instrumentalist'),
    ('Sound-engineer', 'Sound Engineer'),
    ('Music-educator', 'Music Educator'),
    ('Folk-traditional', 'Folk and Traditional'),
    ('DJ', 'DJ'),
    ('Cover-band', 'Cover Band')
    ]

    STATUS_CHOICES =[
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Pending', 'Pending'),
    ]
    EVENT_TYPES = [
    ('Birthday', 'Birthday'),
    ('Corporate Event', 'Corporate Event'),
    ('Festival', 'Festival'),
    ('Graduation', 'Graduation'),
    ('Wedding', 'Wedding'),
    ('Concert', 'Concert'),
    ('Private Party', 'Private Party'),
    ('Club Event', 'Club Event'),
    ('Bar Mitzvah', 'Bar Mitzvah'),
    ('Bat Mitzvah', 'Bat Mitzvah'),
    ('Anniversary', 'Anniversary'),
    ('Charity Event', 'Charity Event'),
    ('Holiday Party', 'Holiday Party'),
    ('Awards Ceremony', 'Awards Ceremony'),
    ('Reception', 'Reception'),
    ('School Event', 'School Event'),
    ('Fundraiser', 'Fundraiser'),
    ('Fair', 'Fair'),
    ('Conference', 'Conference'),
    ('Community Event', 'Community Event'),
    ('Religious Event', 'Religious Event'),
    ('Cruise Ship Event', 'Cruise Ship Event'),
    ('Sporting Event', 'Sporting Event'),
    ('Art Gallery Opening', 'Art Gallery Opening'),
    ('Film Premiere', 'Film Premiere'),
    ('Book Launch', 'Book Launch'),
    ('Trade Show', 'Trade Show'),
    ('Political Rally', 'Political Rally'),
    ('Protest', 'Protest'),
    # Add more event types as ne    eded
]
   
    
    title = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='gigs', )
    genres = models.ManyToManyField('Genre', related_name='gigs')
    description = models.TextField()
    location = models.CharField(max_length=100, null=True)
    date_created = models.DateField(auto_now_add=True, auto_created=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Profession_category = models.CharField(max_length=25, choices=PROFESSION_CHOICES,  null=True)
    dry_run = models.CharField(max_length=20, choices = dry_run_choices,  null=True)
    event_policy = models.CharField(max_length=20, choices=EVENT_POLICY_CHOICES,  null=True)
    event_date = models.DateTimeField(auto_now_add=False, null=True)  
    event_type = models.CharField(max_length=20, null=True,  choices=EVENT_TYPES)
    

    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.description[:50]+'...'



class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    

class Application(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT) #Will probably raise integrity issues, How to handle them?
    musician = models.ForeignKey(Musician, on_delete=models.PROTECT) #Will probably raise integrity issues, How to handle them?
    date_applied = models.DateTimeField(auto_now_add=True)
    gig =  models.ForeignKey(Gig, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=(("Submitted", "Submitted"), ("Accepted", "Accepted"), ("Rejected", "Rejected")), default="Submitted")
    
    
    class Meta:
        unique_together = (("gig", "musician"),)

    def __str__(self):
        return f"Job by - {self.client} - {self.musician} applied for {self.gig.title} on {self.date_applied}"


class SuccessfulHire(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    musician = models.ForeignKey(Musician, on_delete=models.PROTECT)
    gig = models.ForeignKey(Gig, on_delete=models.PROTECT)
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name="successfulhire")
    completion_status = models.CharField(max_length=20, choices=(("Ongoing", "Ongoing"), ("Completed", "Completed"), ("Cancelled", "Cancelled")), default="Ongoing")    
    date_created = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.client} - hired {self.musician}  for {self.gig.title} on {self.gig.event_date}"
    



class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_reviews")
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    rating = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} on {self.reviewee.username}"


class Payment(models.Model):
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    successfulhire = models.ForeignKey(SuccessfulHire, on_delete=models.CASCADE, related_name="payments")
    date_paid = models.DateTimeField(default=timezone.now)
        
   
    def __str__(self) -> str:
        return f"{self.client.user.username} paid {self.amount} for {self.successfulhire.gig.title} to {self.successfulhire.musician.user.username}"
    