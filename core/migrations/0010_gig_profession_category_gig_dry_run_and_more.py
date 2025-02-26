# Generated by Django 5.0.1 on 2024-02-14 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_gig'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='Profession_category',
            field=models.CharField(choices=[('', 'Select one'), ('singer', 'Singer'), ('songwriter', 'Songwriter'), ('producer', 'Producer'), ('vocalist', 'Vocalist'), ('band', 'Band'), ('instrumentalist', 'Instrumentalist'), ('sound-engineer', 'Sound Engineer'), ('music-educator', 'Music Educator'), ('folk-traditional', 'Folk and Traditional'), ('dj', 'DJ'), ('cover-band', 'Cover Band')], default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gig',
            name='dry_run',
            field=models.CharField(choices=[('Yes', 'Yes (Paid Separate)'), ('No', 'Yes (No payment)'), ('Full-after-job', 'NO'), ('Negotiable', 'To Be Determined')], default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gig',
            name='payment_policy',
            field=models.CharField(choices=[('Full-before-job', '100%: Before Job'), ('Half-before-after', '50%: Before and After'), ('Full-after-job', '100%: After Job'), ('Negotiable', 'Negotiable')], default='', max_length=20),
            preserve_default=False,
        ),
    ]
