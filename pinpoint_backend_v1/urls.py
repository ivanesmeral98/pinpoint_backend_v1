"""pinpoint_backend_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from pinpoint_backend_v1 import views

router = routers.DefaultRouter()
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login', views.login_handler),
    path('signup', views.signup_handler),
    path('addpin', views.add_pin_handler),
    path('getpins', views.get_pins_handler),
    path('session-token', views.get_session_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('analytics', views.send_data),
    path('deletepin', views.delete_pin),
    path('followfriend', views.follow_friend),
    path('feed', views.feed_handler),
    path('getprofile', views.get_profile),
    path('updateprofile', views.update_profile),
    path('getcollabgroups', views.get_groups_handler),
    path('unfollowfriend', views.unfollow_handler)
]
