# Generated by Django 2.2 on 2021-03-24 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=180)),
                ('friend', models.CharField(max_length=180)),
            ],
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='namename', max_length=180)),
                ('last_name', models.CharField(default='lastname', max_length=180)),
                ('address', models.CharField(max_length=180)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, default=5, max_digits=9)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, default=5, max_digits=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('username', models.CharField(max_length=180)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, default=5, max_digits=1)),
            ],
        ),
    ]
