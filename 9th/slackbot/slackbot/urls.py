
from django.contrib import admin
from django.urls import path
from app.views import slack_events

urlpatterns = [
    path('admin/', admin.site.urls),
    path('slack/events/', slack_events),
]
