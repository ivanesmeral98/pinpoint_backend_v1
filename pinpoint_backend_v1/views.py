from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from pinpoint_backend_v1.serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from pinpoint_backend_v1.models import Pin
from django.middleware import csrf
import json
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from collections import defaultdict
from django.shortcuts import render
import requests
from datetime import datetime
from django.utils import timezone

################# DASHBOARD FUNCTIONS ########################
@api_view(['GET'])
def send_data(request):
  if request.method == "GET":
    ### SETUP
    dashboard_dict = {}
    dashboard_dict['users_joined'] = users_joined()
    dashboard_dict['countries_graph'] = countries_graph()
    dashboard_dict['daily_active_users'] = daily_active_users()
    dashboard_dict['login_pins_ratio'] = login_pins_ratio()
    dashboard_dict['pins_by_day'] = pins_by_day()
    
    # USERS JOINED
    users_joined_counts = dashboard_dict['users_joined']['out_counts']
    users_joined_dates = dashboard_dict['users_joined']['out_dates']
    print('user join counts', users_joined_counts)
    print('user join dates', users_joined_dates)

    # COUNTRIES
    out_countries = dashboard_dict['countries_graph']['out_countries']
    out_countries_pin_count = dashboard_dict['countries_graph']['out_countries_pin_count']
  #  print(out_countries)
  #  print(out_countries_pin_count)

    # DAILY ACTIVE USERS
    out_dau_dates = dashboard_dict['daily_active_users']['out_dau_dates']
    out_unique_logins = dashboard_dict['daily_active_users']['out_unique_logins']
    print(out_dau_dates)
    print(out_unique_logins)

    # Login pin ratio
    out_user_count = dashboard_dict['login_pins_ratio']['user_count']
    out_pin_count = dashboard_dict['login_pins_ratio']['pin_count']

    # PINS BY DAY
    pins_counts = dashboard_dict['pins_by_day']['out_counts']
    pins_dates = dashboard_dict['pins_by_day']['out_dates']

    ### JSON SERIALIZE
   # json_users_joined_counts = json.dumps(users_joined_counts)
   # json_users_joined_dates = json.dumps(users_joined_dates)
   # json_out_countries = json.dumps(out_countries)
   # json_out_countries_pin_count = json.dumps(out_countries_pin_count)
   # json_out_dau_dates = json.dumps(out_dau_dates)
   # json_out_unique_logins = json.dumps(out_unique_logins)
   # json_out_ratio = json.dumps(out_ratio)

  return render(request, 'test.html', 
  { 
    "users_joined_counts": users_joined_counts,
    "users_joined_dates": users_joined_dates,
    "out_countries": out_countries,
    "out_countries_pin_count": out_countries_pin_count,
    "out_dau_dates": out_dau_dates,
    "out_unique_logins": out_unique_logins,
    "out_user_count": out_user_count,
    "out_pin_count": out_pin_count,
    "pins_counts": pins_counts,
    "pins_dates": pins_dates
  })

def pins_by_day():
  data = defaultdict(list)
  out_dates = []
  out_counts = []
  pins = list(Pin.objects.all().values())
  for pin in pins:
    data[str(pin['created_at']).split(' ')[0]].append(pin)
  for date in data:
    out_dates.append(date)
    out_counts.append(len(data[date]))
    # print(date)
    # print(len(data[date]))

  json_out_dates = json.dumps(out_dates)
  json_out_counts = json.dumps(out_counts)
  return {'out_dates': json_out_dates, 'out_counts': json_out_counts}

def users_joined():
  data = defaultdict(list)
  out_dates = []
  out_counts = []
  users = list(User.objects.all().values())
  for user in users:
    data[str(user['date_joined']).split(' ')[0]].append(user)
  for date in data:
    out_dates.append(date)
    out_counts.append(len(data[date]))
    # print(date)
    # print(len(data[date]))

  json_out_dates = json.dumps(out_dates)
  json_out_counts = json.dumps(out_counts)
  return {'out_dates': json_out_dates, 'out_counts': json_out_counts}

def countries_graph():
  data = {}
  out_countries = []
  out_countries_pin_count = []
  pins = list(Pin.objects.all().values())

  # produce dictionary with country as key and # of pins as value
  for pin in pins:
    access_key = '619d8b82bd322448069c1bf725239054'
    address = pin['address']
    # doing api call and getting country pin's address is from
    country_api_route = f'http://api.positionstack.com/v1/forward?access_key={access_key}&query={address}'
    
    while True:
      response = requests.get(country_api_route)
      if response.json()['data'][0]:
        break
    
    # print('result', response.json()['data'])

    if response.json()['data'][0]['country'] in data:
      data[response.json()['data'][0]['country']] = data.get(response.json()['data'][0]['country']) + 1
    else:
      data[response.json()['data'][0]['country']] = 1

  for country in data:
    out_countries.append(country)
    out_countries_pin_count.append(data[country])
    # print(country)
    # print(data[country])

    # print(response.json()['data'][0]['country'])
  return {'out_countries': out_countries, 'out_countries_pin_count': out_countries_pin_count}

def daily_active_users():
  data = defaultdict(set)
  out_dau_dates = []
  out_unique_logins = []
  users = list(User.objects.all().values())
  for user in users:
    if str(user['last_login']).split(' ')[0] is not None:
      data[str(user['last_login']).split(' ')[0]].add(user['username'])
  for date in data:
    out_dau_dates.append(date)
    out_unique_logins.append(len(data[date]))
    # print(date)
    # print(len(data[date]))

  json_out_dau_dates = json.dumps(out_dau_dates)
  json_out_unique_logins = json.dumps(out_unique_logins)

  return {'out_dau_dates': json_out_dau_dates, 'out_unique_logins': json_out_unique_logins}

def login_pins_ratio():
  user_count = 0
  pin_count = 0
  users = list(User.objects.all().values())
  pins = list(Pin.objects.all().values())
  for user in users:
    user_count = user_count + 1
  for pin in pins:
    pin_count = pin_count + 1

  # ratio = user_count / pin_count
  
  json_out_user_count = json.dumps(user_count)
  json_out_pin_count = json.dumps(pin_count)
  return {'user_count': json_out_user_count, 'pin_count': json_out_pin_count}
  

################# DASHBOARD FUNCTIONS ########################


# SENDGRID email API
def send_email(username, email):
    print('entered')
    subject ='Pinpoint account successfully created'
    from_email = 'pinpoint.app.noreply@gmail.com'
    html_content =f'<strong>Congrats</strong> {username}! <br/><br/> Your Pinpoint account was successfully created'
  
    msg = EmailMessage(subject, html_content, from_email, [], [f'{email}'])
    msg.content_subtype = "html"
    msg.send()
    return

@api_view(['POST'])
def login_handler(request):
  if request.method == "POST":
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            content = {'Status': 'Login successful!'}
            return Response(content, status=status.HTTP_200_OK)
        content = {'Status': 'Login unsuccessful!'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)      

@api_view(['GET'])
def get_session_token(request):
  return Response({'SessionToken': csrf.get_token(request)})

@api_view(['POST'])
@authentication_classes([])
def signup_handler(request):
  if request.method == "POST":
    if User.objects.filter(username=request.data['username']).exists():
      content = {'Status': 'Username already exists!'}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif User.objects.filter(email=request.data['email']).exists():
      content = {'Status': 'Email already exists!'}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
      user = User.objects.create_user(username=request.data['username'], email=request.data['email'], password=request.data['password'])
      send_email(request.data['username'], request.data['email'])
      content = {'Status': 'User profile successfully created!'}

      return Response(content, status=status.HTTP_200_OK)
  
  content = {'Status': 'User was not created!'}
  return Response(content, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_pin_handler(request):
  if request.method == "POST":
    if not Pin.objects.filter(address=request.data['address'], user_id=request.user.id).exists():
      address = request.data["address"]
      new_pin = Pin(address=address, user_id=request.user.id, username=request.user.username)
      new_pin.save()
      content = {'Status': 'Pin successfully created!'}
      return Response(content, status=status.HTTP_200_OK)
    else:
      content = {'Status': 'Pin already exists!'}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
  else:
    content = {'Status': 'Unable to create pin!'}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_pins_handler(request):
  if request.method == "GET":
    addresses = list(Pin.objects.filter(user_id=request.user.id).values())
    content = {'Pins': addresses}
    return Response(content, status=status.HTTP_200_OK)
  else:
    content = {'Status': 'Unable to retrieve pins!'}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)

'''
@api_view(['POST'])
@authentication_classes([])
def logout_handler(request):
  if request.method == "POST":
    print('request', request)
    print('request.user', request.user.username)
    
   
    user = request.user.username
    print(request.user.username)
    last_logout = timezone.now()

    if LastLogout.objects.filter(user=user).values():
      # edit logout
      new_logout = 
    else:

    new_logout = LastLogout(user=user, last_logout=last_logout)
    print(list(LastLogout.objects.values()))
    new_logout.save()
    logout(request)
    content = {'Status': 'User successfully logged out!'}
  return Response(content, status=status.HTTP_200_OK)
'''