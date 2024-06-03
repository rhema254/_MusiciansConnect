# Generated by Django 5.0.1 on 2024-02-15 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_gig_profession_category_gig_dry_run_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='dry_run',
            field=models.CharField(choices=[('', 'Select one'), ('Yes', 'Yes (Paid Separate)'), ('No', 'Yes (No payment)'), ('Full-after-job', 'NO'), ('Negotiable', 'To Be Determined')], max_length=20),
        ),
        migrations.AlterField(
            model_name='gig',
            name='genre',
            field=models.CharField(choices=[('Soul', 'Soul'), ('Jazz', 'Jazz'), ('Benga', 'Benga'), ('Pop', 'Pop'), ('R&B', 'R&B'), ('Bongo', 'Bongo'), ('Chakacha', 'Chakacha'), ('Mugithi', 'Mugithi'), ('Traditional songs', 'Traditional songs')], default='Jazz', max_length=20),
        ),
        migrations.AlterField(
            model_name='gig',
            name='payment_policy',
            field=models.CharField(choices=[('', 'Select one'), ('Full-before-job', '100%: Before Job'), ('Half-before-after', '50%: Before and After'), ('Full-after-job', '100%: After Job'), ('Negotiable', 'Negotiable')], max_length=20),
        ),
    ]
