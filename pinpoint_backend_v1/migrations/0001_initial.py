# Generated by Django 2.2 on 2021-03-30 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CollabGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=180)),
                ('group_id', models.CharField(max_length=180)),
            ],
        ),
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
                ('name', models.CharField(max_length=180)),
                ('address', models.CharField(max_length=180)),
                ('latitude', models.DecimalField(blank=True, decimal_places=10, default=5, max_digits=19)),
                ('longitude', models.DecimalField(blank=True, decimal_places=10, default=5, max_digits=19)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=180)),
            ],
        ),
    ]
