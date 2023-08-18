# Generated by Django 4.2.4 on 2023-08-18 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0006_watchlist_avg_rating_watchlist_number_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]